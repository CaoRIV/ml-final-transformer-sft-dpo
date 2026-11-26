#!/usr/bin/env python3
"""Khóa USER_TEST từ khảo sát thật đã redaction, hoàn toàn ngoài repository.

Công cụ này không thu thập khảo sát, không tạo câu hỏi/nhãn test và không chứng minh
consent. Nó chỉ kiểm tra một export L3 đã có consent/redaction cùng attestation do
operator cung cấp, audit rò rỉ với QA SFT, rồi tạo release heldout cho evaluator.
Mọi lỗi cố ý chỉ nêu dòng và loại lỗi: không in question_text_redacted, ID hay hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


SPECIAL_SCOPE_GROUPS = frozenset({"out_of_scope", "uncertain"})
FAMILY_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SURVEY_FIELDS = frozenset(
    {
        "survey_question_id",
        "respondent_cluster_id",
        "consent_version",
        "consent_status",
        "consented_at",
        "withdrawn_at",
        "question_text_redacted",
        "hanoi_relation",
        "scope_group",
        "survey_channel",
        "redaction_status",
        "redaction_reviewer_id",
        "test_split_status",
        "dataset_version",
        "created_at",
    }
)
QA_FIELDS = frozenset({"question_text", "split", "qa_id", "procedure_family_id"})
GATES = tuple(f"G-{number:02d}" for number in range(1, 7))
VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
ROLE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$")
CONSENT_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EMAIL_RE = re.compile(r"\b[^\s@]{1,64}@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)[ .-]?\d(?:[ .-]?\d){8,9}(?!\d)")
ID_NUMBER_RE = re.compile(r"(?<!\d)\d{9,12}(?!\d)")
ADDRESS_RE = re.compile(
    r"\b(?:địa\s*chỉ|số\s*nhà|ngõ|hẻm|phường|xã|quận|huyện|tỉnh|thành\s*phố)\b",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


class SurveyError(Exception):
    """Lỗi validation an toàn để hiển thị mà không tiết lộ nội dung khảo sát."""


def fail(message: str) -> None:
    raise SurveyError(message)


def safe_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def require_external_path(path: Path, repo_root: Path, label: str, *, must_exist: bool) -> Path:
    """Không bao giờ đọc/ghi hiện vật nghiên cứu ở trong tree repository."""
    resolved = path.resolve(strict=must_exist)
    if safe_is_relative_to(resolved, repo_root):
        fail(f"{label} phải ở ngoài repository")
    return resolved


def parse_iso_time(value: Any, label: str) -> str:
    if not isinstance(value, str) or "T" not in value:
        fail(f"{label} phải là thời điểm ISO-8601 có timezone")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        fail(f"{label} phải là thời điểm ISO-8601 có timezone")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail(f"{label} phải là thời điểm ISO-8601 có timezone")
    return value


def require_uuid4(value: Any, label: str) -> str:
    if not isinstance(value, str):
        fail(f"{label} phải là UUIDv4")
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        fail(f"{label} phải là UUIDv4")
    if parsed.version != 4 or str(parsed) != value.lower():
        fail(f"{label} phải là UUIDv4 canonical")
    return value


def require_safe_string(value: Any, label: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        fail(f"{label} không hợp lệ")
    return value


def contains_basic_pii(text: str) -> bool:
    """Chỉ là lưới an toàn thô; reviewer redaction vẫn là quyết định bắt buộc."""
    return bool(
        EMAIL_RE.search(text)
        or PHONE_RE.search(text)
        or ID_NUMBER_RE.search(text)
        or ADDRESS_RE.search(text)
    )


def normalized_question(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def trigrams(words: tuple[str, ...]) -> set[tuple[str, ...]]:
    return {words[i:i + 3] for i in range(len(words) - 2)}


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            parsed = json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        fail(f"{label} không đọc được JSON hợp lệ")
    if not isinstance(parsed, dict):
        fail(f"{label} phải là JSON object")
    return parsed

def load_scope_groups(ledger_path: Path) -> frozenset[str]:
    """Lấy họ thủ tục hiện hành từ D.1; không khóa USER_TEST vào năm họ ban đầu."""
    ledger = read_json_object(ledger_path, "ledger")
    families = ledger.get("procedure_families")
    if not isinstance(families, list) or not families:
        fail("ledger không có procedure_families")
    family_ids: set[str] = set()
    for family in families:
        if not isinstance(family, dict) or set(family) < {"id"}:
            fail("ledger có procedure_family không hợp lệ")
        family_id = family["id"]
        if not isinstance(family_id, str) or not FAMILY_ID_RE.fullmatch(family_id):
            fail("ledger có procedure_family id không hợp lệ")
        if family_id in family_ids:
            fail("ledger có procedure_family id lặp")
        family_ids.add(family_id)
    return frozenset(family_ids) | SPECIAL_SCOPE_GROUPS


def iter_jsonl(path: Path, label: str) -> Iterable[tuple[int, dict[str, Any]]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    fail(f"{label} có dòng trống tại dòng {line_number}")
                try:
                    parsed = json.loads(line)
                except json.JSONDecodeError:
                    fail(f"{label} có JSONL lỗi tại dòng {line_number}")
                if not isinstance(parsed, dict):
                    fail(f"{label} phải có object tại dòng {line_number}")
                yield line_number, parsed
    except OSError:
        fail(f"{label} không đọc được")


def validate_survey_record(
    record: dict[str, Any], line_number: int, version: str, scope_groups: frozenset[str]
) -> dict[str, Any]:
    if set(record) != SURVEY_FIELDS:
        fail(f"survey sai allowlist §4.1 tại dòng {line_number}")
    require_uuid4(record["survey_question_id"], "survey_question_id")
    require_uuid4(record["respondent_cluster_id"], "respondent_cluster_id")
    require_safe_string(record["consent_version"], "consent_version", CONSENT_VERSION_RE)
    if record["consent_status"] != "granted":
        fail(f"survey không có consent granted tại dòng {line_number}")
    parse_iso_time(record["consented_at"], "consented_at")
    if record["withdrawn_at"] is not None:
        # Một record đã rút phải được loại từ L3, kể cả consent_status vẫn còn granted.
        fail(f"survey đã withdrawn tại dòng {line_number}")
    question = record["question_text_redacted"]
    if not isinstance(question, str) or not question.strip() or len(question) > 4000:
        fail(f"survey có question_text_redacted không hợp lệ tại dòng {line_number}")
    if contains_basic_pii(question):
        fail(f"survey có dấu hiệu PII cần human review tại dòng {line_number}")
    if record["hanoi_relation"] not in {"yes", "no", "unknown", "not_answered"}:
        fail(f"survey có hanoi_relation không hợp lệ tại dòng {line_number}")
    if record["scope_group"] not in scope_groups:
        fail(f"survey có scope_group ngoài allowlist tại dòng {line_number}")
    if record["survey_channel"] not in {"paper_in_person", "interview_in_person"}:
        fail(f"survey có survey_channel không hợp lệ tại dòng {line_number}")
    if record["redaction_status"] != "approved":
        fail(f"survey chưa được redaction review tại dòng {line_number}")
    require_safe_string(record["redaction_reviewer_id"], "redaction_reviewer_id", ROLE_ID_RE)
    if record["test_split_status"] not in {"eligible", "heldout"}:
        fail(f"survey không eligible cho final lock tại dòng {line_number}")
    if record["dataset_version"] != version:
        fail(f"survey có dataset_version khác --version tại dòng {line_number}")
    parse_iso_time(record["created_at"], "created_at")
    return record


def load_survey(path: Path, version: str, scope_groups: frozenset[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    survey_ids: set[str] = set()
    clusters: Counter[str] = Counter()
    for line_number, raw in iter_jsonl(path, "survey"):
        record = validate_survey_record(raw, line_number, version, scope_groups)
        survey_id = record["survey_question_id"]
        if survey_id in survey_ids:
            fail(f"survey có survey_question_id lặp tại dòng {line_number}")
        survey_ids.add(survey_id)
        clusters[record["respondent_cluster_id"]] += 1
        if clusters[record["respondent_cluster_id"]] > 3:
            fail(f"survey vượt tối đa 3 câu mỗi respondent tại dòng {line_number}")
        records.append(record)
    if not records:
        fail("survey không có record")
    return records


def validate_qa_record(record: dict[str, Any], line_number: int) -> dict[str, Any]:
    if set(record) != QA_FIELDS:
        fail(f"qa phải là export QA-only tại dòng {line_number}")
    try:
        qa_id = uuid.UUID(record["qa_id"])
    except (ValueError, TypeError, AttributeError):
        fail(f"qa_id không hợp lệ tại dòng {line_number}")
    if qa_id.version not in {4, 5} or str(qa_id) != record["qa_id"]:
        fail(f"qa_id phải là UUIDv4/v5 canonical tại dòng {line_number}")
    if record["split"] not in {"train", "validation"}:
        fail(f"qa có split không hợp lệ tại dòng {line_number}")
    if not isinstance(record["question_text"], str) or not record["question_text"].strip():
        fail(f"qa có question_text không hợp lệ tại dòng {line_number}")
    if not isinstance(record["procedure_family_id"], str) or not record["procedure_family_id"].strip():
        fail(f"qa có procedure_family_id không hợp lệ tại dòng {line_number}")
    return record


def load_qa(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    qa_ids: set[str] = set()
    for line_number, raw in iter_jsonl(path, "qa"):
        record = validate_qa_record(raw, line_number)
        if record["qa_id"] in qa_ids:
            fail(f"qa có qa_id lặp tại dòng {line_number}")
        qa_ids.add(record["qa_id"])
        records.append(record)
    if not records:
        fail("qa không có record train/validation")
    return records


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        fail("không thể tạo audit fingerprint cho qa")
    return digest.hexdigest()


def validate_attestation(path: Path, qa_digest: str) -> dict[str, Any]:
    """Chấp nhận khai báo operator, không biến code thành bằng chứng consent thực tế."""
    document = read_json_object(path, "attestation")
    required = {"attestation_version", "attested_at", "gates", "semantic_overlap_clearance"}
    if set(document) != required:
        fail("attestation sai schema")
    require_safe_string(document["attestation_version"], "attestation_version", VERSION_RE)
    parse_iso_time(document["attested_at"], "attested_at")

    gates = document["gates"]
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        fail("attestation phải có đủ G-01 đến G-06")
    for gate in GATES:
        entry = gates[gate]
        if not isinstance(entry, dict) or set(entry) != {"status", "evidence_source"}:
            fail(f"attestation {gate} sai schema")
        if entry["status"] != "pass" or entry["evidence_source"] != "operator_provided":
            fail(f"attestation {gate} chưa pass bằng evidence operator_provided")

    clearance = document["semantic_overlap_clearance"]
    expected_clearance = {
        "status",
        "evaluator_role_id",
        "cleared_at",
        "qa_file_sha256",
        "survey_records_reviewed",
    }
    if not isinstance(clearance, dict) or set(clearance) != expected_clearance:
        fail("semantic_overlap_clearance sai schema")
    if clearance["status"] != "cleared" or clearance["survey_records_reviewed"] is not True:
        fail("chưa có evaluator clearance semantic overlap")
    require_safe_string(clearance["evaluator_role_id"], "evaluator_role_id", ROLE_ID_RE)
    parse_iso_time(clearance["cleared_at"], "cleared_at")
    if not isinstance(clearance["qa_file_sha256"], str) or not SHA256_RE.fullmatch(clearance["qa_file_sha256"]):
        fail("semantic_overlap_clearance thiếu qa_file_sha256 hợp lệ")
    if clearance["qa_file_sha256"] != qa_digest:
        fail("semantic_overlap_clearance không khớp qa audit hiện tại")
    return document


def audit_overlap(survey: list[dict[str, Any]], qa: list[dict[str, Any]]) -> tuple[int, int, int]:
    """Chặn family split trước; kể cả out_of_scope/uncertain vẫn audit prompt."""
    qa_families = {record["procedure_family_id"] for record in qa}
    family_overlap = sum(record["scope_group"] in qa_families for record in survey)
    if family_overlap:
        fail("phát hiện procedure family overlap giữa USER_TEST và SFT train/validation")

    qa_normalized = {tuple(WORD_RE.findall(normalized_question(record["question_text"]))) for record in qa}
    qa_shingles = [trigrams(words) for words in qa_normalized if len(words) >= 3]
    exact_matches = 0
    near_matches = 0
    for survey_record in survey:
        question = survey_record["question_text_redacted"]
        normalized = tuple(WORD_RE.findall(normalized_question(question)))
        if normalized in qa_normalized:
            exact_matches += 1
            continue
        shingles = trigrams(normalized)
        if shingles and any(
            5 * len(shingles & other) >= 4 * len(shingles | other) for other in qa_shingles
        ):
            near_matches += 1
    if exact_matches or near_matches:
        fail("phát hiện lexical prompt overlap giữa USER_TEST và SFT train/validation")
    return family_overlap, exact_matches, near_matches


def canonical_json_bytes(document: Any) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_release(
    output_root: Path,
    version: str,
    survey: list[dict[str, Any]],
    attestation: dict[str, Any],
    qa_digest: str,
    overlap_counts: tuple[int, int, int],
) -> tuple[int, int]:
    """Tạo duy nhất một thư mục version mới; không ghi đè release đã khóa."""
    output_root.mkdir(parents=True, exist_ok=True)
    if not output_root.is_dir():
        fail("--output không phải thư mục")
    version_dir = output_root / version
    try:
        version_dir.mkdir(mode=0o700)
    except FileExistsError:
        fail("version output đã tồn tại; release khóa không được ghi đè")
    except OSError:
        fail("không thể tạo version output")

    try:
        locked_records = [{**record, "test_split_status": "heldout"} for record in survey]
        test_path = version_dir / "user_test.jsonl"
        with test_path.open("x", encoding="utf-8", newline="\n") as handle:
            for record in locked_records:
                handle.write(canonical_json_bytes(record).decode("utf-8"))

        scope_counts = dict(sorted(Counter(record["scope_group"] for record in survey).items()))
        family_overlap, exact_matches, near_matches = overlap_counts
        manifest = {
            "manifest_kind": "private_user_test_lock",
            "dataset_version": version,
            "created_at_utc": datetime.now().astimezone().isoformat(),
            "files": [{"name": "user_test.jsonl", "sha256": sha256_file(test_path)}],
            "counts": {
                "records": len(locked_records),
                "respondent_clusters": len({record["respondent_cluster_id"] for record in survey}),
                "scope_groups": scope_counts,
            },
            "lock_checks": {
                "privacy_workflow_allowlist": "passed",
                "attestations": {gate: "operator_provided" for gate in GATES},
                "semantic_overlap_clearance": {
                    "status": "cleared",
                    "evaluator_role_id": attestation["semantic_overlap_clearance"]["evaluator_role_id"],
                    "cleared_at": attestation["semantic_overlap_clearance"]["cleared_at"],
                    "qa_file_sha256": qa_digest,
                    "survey_records_reviewed": True,
                },
                "sft_family_overlap": family_overlap,
                "lexical_normalized_exact_matches": exact_matches,
                "lexical_near_matches": near_matches,
                "near_method": "token_3gram_jaccard_gte_0.80",
            },
            "limitations": [
                "G-01_den_G-06_va_semantic_clearance_la_khai_bao_operator/evaluator; code_khong_chung_minh_consent_thuc_te.",
                "PII_sanity_chi_la_luoi_co_ban_va_khong_thay_the_human_redaction_review.",
                "QA_input_chi_la_hien_vat_audit_SFT_hien_tai; USER_TEST_lock_khong_xac_nhan_SFT_release_hoac_hoan_thanh_D.2.",
            ],
        }
        manifest_path = version_dir / "manifest.private.json"
        with manifest_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(canonical_json_bytes(manifest).decode("utf-8"))
    except Exception:
        # Chỉ xóa cây thư mục mà invocation này vừa tạo, để không lưu release nửa vời.
        shutil.rmtree(version_dir, ignore_errors=True)
        raise
    return len(locked_records), len({record["respondent_cluster_id"] for record in survey})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Khóa USER_TEST thật đã redaction cho evaluator. Không tạo test/nhãn, không thu thập "
            "khảo sát và không xác minh consent; mọi hiện vật khảo sát/QA/output phải ngoài repo. "
            "Khóa này không xác nhận SFT release hay D.2 đã hoàn thành."
        ),
        epilog=(
            "--survey là JSONL L3 có đúng allowlist privacy-workflow §4.1; bắt buộc granted, approved, "
            "eligible/heldout. scope_group lấy từ procedure_families[].id của --ledger, cộng out_of_scope "
            "và uncertain. --qa là JSONL QA-only ngoài repo, đúng question_text, split, qa_id, "
            "procedure_family_id; chỉ train/validation. --attestation ngoài repo có đúng các key "
            "attestation_version, attested_at, gates, semantic_overlap_clearance. gates có đủ G-01..G-06, "
            "mỗi gate đúng {status: pass, evidence_source: operator_provided}. semantic_overlap_clearance "
            "đúng {status: cleared, evaluator_role_id, cleared_at, qa_file_sha256, "
            "survey_records_reviewed: true}; qa_file_sha256 phải khớp byte SHA-256 của --qa. "
            "Script chặn family/prompt overlap, khóa test_split_status=heldout và chỉ in proof tổng hợp."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--survey", required=True, type=Path, help="JSONL khảo sát đã redaction, ngoài repo")
    parser.add_argument("--attestation", required=True, type=Path, help="JSON attestation ngoài repo")
    parser.add_argument("--qa", required=True, type=Path, help="JSONL QA train/validation-only ngoài repo")
    parser.add_argument("--output", required=True, type=Path, help="thư mục gốc release ngoài repo")
    parser.add_argument("--version", required=True, help="version an toàn tạo đúng một thư mục release mới")
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs" / "data" / "source-ledger.json",
        help="ledger D.1; mặc định docs/data/source-ledger.json để lấy procedure_families[].id",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not VERSION_RE.fullmatch(args.version):
        print("ERROR: --version không hợp lệ", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    try:
        survey_path = require_external_path(args.survey, repo_root, "--survey", must_exist=True)
        attestation_path = require_external_path(args.attestation, repo_root, "--attestation", must_exist=True)
        qa_path = require_external_path(args.qa, repo_root, "--qa", must_exist=True)
        output_root = require_external_path(args.output, repo_root, "--output", must_exist=False)
        ledger_path = args.ledger.resolve(strict=True)
        scope_groups = load_scope_groups(ledger_path)
        survey = load_survey(survey_path, args.version, scope_groups)
        qa = load_qa(qa_path)
        qa_digest = sha256_file(qa_path)
        attestation = validate_attestation(attestation_path, qa_digest)
        overlap_counts = audit_overlap(survey, qa)
        record_count, cluster_count = write_release(
            output_root, args.version, survey, attestation, qa_digest, overlap_counts
        )
    except SurveyError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except OSError:
        print("ERROR: không thể xử lý hiện vật khảo sát; không có release bị khóa", file=sys.stderr)
        return 2

    # Proof aggregate duy nhất: không có question, ID, đường dẫn hay hash test trên console.
    print(
        "LOCKED_USER_TEST "
        f"version={args.version} records={record_count} respondent_clusters={cluster_count} "
        "gates=G-01..G-06:operator_provided "
        "semantic_clearance=cleared family_overlap=0 lexical_exact=0 lexical_near=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
