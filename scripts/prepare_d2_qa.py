"""Build cited D.2 candidates from verified official snapshots; check before SFT release."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import unicodedata
from uuid import NAMESPACE_URL, uuid5
from xml.etree import ElementTree
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/data/source-ledger.json"
SEED = ROOT / "scripts/d2_seed_recipes.json"
NORMALIZATION = "NFC-whitespace-v1"
SFT = ("train", "validation")
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
VERSION = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}\Z")
REVIEWER = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,31}\Z")
REVIEW_COLUMNS = (
    "qa_review_id", "qa_id", "qa_record_version", "dataset_version", "split", "sampling_stratum",
    "sampling_seed", "sampled_at", "source_version_ids", "required_span_ids", "reviewer_id",
    "reviewed_at", "citation_span_ids_checked", "content_correctness", "completeness",
    "citation_verifiability", "scope_and_refusal", "hallucination_flag", "privacy_flag",
    "duplicate_or_leakage_flag", "decision", "reason_codes", "review_note", "follow_up_batch_key",
)
REVIEW_CONTENT = ("question_text", "answer_text", "sources_for_review")
SHORT_REVIEW_COLUMNS = ("qa_review_id", *REVIEW_CONTENT, "decision", "review_note", "reviewer_id", "reviewed_at")
SHORT_REVIEW_NAME = "manual-review-short.csv"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def signature(text: str) -> str:
    return " ".join(re.findall(r"[^\W_]+", normalize(text).casefold()))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def text_field(value, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: cần văn bản")
    return normalize(value)


def json_bytes(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def private_path(path: Path) -> Path:
    path = path.resolve()
    require(not path.is_relative_to(ROOT) or path.is_relative_to(ROOT / "data/review/d2"),
            "Output D.2 trong repo phải nằm dưới data/review/d2; không ghi vào data/samples")
    return path


def lexical_candidates(rows: list[dict]) -> list[dict]:
    """Generate review candidates, not decisions; trigram Jaccard >= 0.85."""
    tokens = [signature(row["question_text"]).split() for row in rows]
    shingles = [{tuple(words[i:i + 3]) for i in range(len(words) - 2)} for words in tokens]
    postings = defaultdict(list)
    candidates = []
    for index, grams in enumerate(shingles):
        overlap = Counter(prior for gram in grams for prior in postings[gram])
        for prior, intersection in sorted(overlap.items()):
            union = len(grams) + len(shingles[prior]) - intersection
            if 100 * intersection >= 85 * union:
                candidates.append({"left": rows[prior]["qa_id"], "right": rows[index]["qa_id"],
                                   "cross_split": rows[prior]["split"] != rows[index]["split"],
                                   "trigram_jaccard": round(intersection / union, 6)})
        for gram in grams:
            postings[gram].append(index)
    return candidates


class OfficialText:
    def __init__(self, ledger: dict):
        self.evidence = {row["evidence_id"]: row for row in ledger["d1_review"]["evidence"]}
        self.assets = {}
        self.regions = {}

    def locate(self, evidence_id: str, page: int | None, anchor: str, document_part: str = "default") -> tuple[str, str, dict, int, int]:
        require(evidence_id in self.evidence, f"{evidence_id}: không có trong bằng chứng D.1")
        source = self.evidence[evidence_id]
        key = (evidence_id, document_part)
        if key not in self.assets:
            selected = source if document_part == "default" else source.get(document_part)
            require(isinstance(selected, dict), f"{evidence_id}: không có phần {document_part}")
            if document_part == "default" and "appendix" in source:
                selected = source["appendix"]
            path = (ROOT / selected["snapshot_path"]).resolve()
            require(path.is_relative_to(ROOT / ".cache/admin-source-audit/d1"), f"{evidence_id}: snapshot ngoài kho D.1")
            digest = file_sha(path)
            require(digest == selected["snapshot_sha256"], f"{evidence_id}: hash snapshot không khớp")
            if path.suffix.lower() == ".pdf":
                try:
                    from pypdf import PdfReader
                except ImportError as error:
                    raise ValueError("Cần pypdf 6.21.4 để đọc PDF D.1; không cần GPU/PyTorch") from error
                reader = PdfReader(path)
            elif path.suffix.lower() == ".docx":
                with ZipFile(path) as archive:
                    document = ElementTree.fromstring(archive.read("word/document.xml"))
                reader = [normalize("".join(t.text or "" for t in paragraph.iter(W + "t")))
                          for paragraph in document.iter(W + "p")]
            else:
                raise ValueError(f"{evidence_id}: cần PDF có lớp chữ hoặc DOCX chính thức đã hash")
            self.assets[key] = (reader, digest, path.suffix.lower())
        reader, digest, suffix = self.assets[key]
        quote = text_field(anchor, f"{evidence_id}/anchor")
        region = (key, page)
        if region not in self.regions:
            if suffix == ".pdf":
                require(type(page) is int and 1 <= page <= len(reader.pages), f"{evidence_id}: page PDF phải đúng số trang")
                self.regions[region] = (normalize(reader.pages[page - 1].extract_text()),)
            else:
                require(page is None, f"{evidence_id}: DOCX định vị theo đoạn, không dùng page")
                self.regions[region] = reader
        matches = [(i, part.find(quote)) for i, part in enumerate(self.regions[region]) if quote in part]
        require(len(matches) == 1, f"{evidence_id}: cần đoạn trích duy nhất trong vùng đã chọn (page={page})")
        paragraph, offset = matches[0]
        require(self.regions[region][paragraph].find(quote, offset + 1) == -1,
                f"{evidence_id}: đoạn trích lặp trong cùng trang/đoạn")
        return quote, f"{evidence_id}@{digest}", source, page or paragraph + 1, offset


def build_candidates(recipes: dict, ledger: dict) -> tuple[list[dict], list[dict]]:
    required = {"dataset_version", "seed", "family_splits", "items"}
    require(required <= recipes.keys() <= required | {"author_type"}, "Sai schema recipe hoặc có trường ngoài luồng QA")
    author = recipes.get("author_type", "not_declared")
    require(author in {"AI_assistant", "human", "mixed", "not_declared"}, "author_type không hợp lệ")
    require(VERSION.fullmatch(recipes["dataset_version"]) is not None, "dataset_version không hợp lệ")
    require(type(recipes["seed"]) is int, "seed phải là số nguyên")
    approved_families = {row["id"]: row for row in ledger["procedure_families"]}
    assignments = recipes["family_splits"]
    require(isinstance(assignments, dict) and set(assignments) <= approved_families.keys()
            and set(assignments.values()) == {*SFT, "holdout"},
            "Khai báo họ thủ tục có trong sổ D.1, đủ train / validation / holdout trước khi soạn")
    require(isinstance(recipes["items"], list) and bool(recipes["items"]), "Không có recipe QA")
    source_text = OfficialText(ledger)
    rows, spans = [], {}
    keys, prompts, answer_signatures = set(), set(), set()
    quote_splits = {}
    offsets = defaultdict(list)
    for item in recipes["items"]:
        require(set(item) == {"key", "record_version", "procedure_family_id", "question_text", "claims"}, "Recipe QA có trường ngoài schema")
        key = item["key"]
        require(SLUG.fullmatch(key) is not None and key not in keys, f"Key QA không hợp lệ/trùng: {key}")
        keys.add(key)
        family = item["procedure_family_id"]
        split = assignments.get(family)
        require(split in SFT, f"{key}: không được soạn QA cho họ chưa chia hoặc holdout")
        family_meta = approved_families[family]
        allowed_evidence = set(family_meta.get("d1_evidence_ids", ()))
        question = text_field(item["question_text"], key)
        prompt_key = signature(question)
        require(prompt_key and prompt_key not in prompts, f"{key}: câu hỏi trùng sau chuẩn hóa")
        prompts.add(prompt_key)
        record_version = item["record_version"]
        require(VERSION.fullmatch(record_version) is not None, f"{key}: sai record_version")
        require(isinstance(item["claims"], list) and bool(item["claims"]), f"{key}: thiếu claim có dẫn nguồn")
        coverage, cited = [], {}
        for claim in item["claims"]:
            require({"text", "evidence_id", "locator", "anchor"} <= claim.keys()
                    and claim.keys() <= {"text", "evidence_id", "locator", "anchor", "page", "document_part"},
                    f"{key}: claim ngoài schema")
            evidence_id = claim["evidence_id"]
            require(evidence_id in allowed_evidence, f"{key}: {evidence_id} không được liên kết với họ này trong D.1")
            locator = text_field(claim["locator"], "locator")
            text = text_field(claim["text"], "claim")
            quote, source_version, evidence, region_number, start = source_text.locate(
                evidence_id, claim.get("page"), claim["anchor"], claim.get("document_part", "default"))
            stop = start + len(quote)
            location = (source_version, region_number)
            require(all(other_split == split or other_stop <= start or stop <= other_start
                        for other_split, other_start, other_stop in offsets[location]),
                    f"{key}: các đoạn dẫn chồng nhau giữa train và validation")
            offsets[location].append((split, start, stop))
            quote_hash = sha(quote.encode("utf-8"))
            require(quote_splits.setdefault(quote_hash, split) == split,
                    f"{key}: cùng đoạn dẫn xuất hiện ở nhiều split")
            span_id = "D2-SPAN-" + sha(f"{source_version}\x1f{region_number}:{start}:{stop}\x1f{locator}".encode("utf-8"))[:24]
            citation = {"span_id": span_id, "evidence_id": evidence_id, "source_version_id": source_version,
                        "url": evidence["url"], "locator": locator, "document_number": evidence["document_number"]}
            cited[span_id] = citation
            spans[span_id] = {**citation, "page": claim.get("page"),
                              "locator_type": "page" if claim.get("page") else "paragraph",
                              "region_number": region_number, "locator_start": start, "locator_end": stop,
                              "retrieved_at_utc": evidence["retrieved_at_utc"], "effective_from": evidence.get("effective_from"),
                              "quoted_text": quote, "span_sha256": quote_hash, "normalization_version": NORMALIZATION}
            coverage.append({"claim_text": text, "source_span_id": span_id, "status": "candidate_pending_manual_review"})
        answer_key = tuple(sorted(signature(c["claim_text"]) for c in coverage))
        require(answer_key and answer_key not in answer_signatures, f"{key}: tập mệnh đề đáp án trùng")
        answer_signatures.add(answer_key)
        qa_id = str(uuid5(NAMESPACE_URL, f"ml-transformer-d2/{family}/{key}"))
        rows.append({
            "qa_id": qa_id, "record_version": record_version, "dataset_version": recipes["dataset_version"],
            "split": split, "scope_group": "hanoi-ho-tich-chung-thuc", "procedure_family_id": family,
            "question_text": question, "question_origin": "authoring", "language": "vi",
            "answer_text": " ".join(f"{c['claim_text']} [{cited[c['source_span_id']]['document_number']}, "
                                    f"{cited[c['source_span_id']]['locator']}]" for c in coverage),
            "citation_span_ids": list(cited),
            "citation_rendering": "\n".join(f"{c['document_number']}, {c['locator']}: {c['url']}" for c in cited.values()),
            "source_version_ids": sorted({c["source_version_id"] for c in cited.values()}), "claim_coverage": coverage,
            "label_status": "draft",
            "provenance": {"method": "curated_claim_recipe", "recipe_key": key, "author_type": author},
        })
    require({row["split"] for row in rows} == set(SFT), "Cần QA thật ở cả train lẫn validation")
    return sorted(rows, key=lambda row: row["qa_id"]), [spans[key] for key in sorted(spans)]


def csv_write(path: Path, rows: list[dict], columns: tuple[str, ...]) -> None:
    with path.open("x", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, columns)
        writer.writeheader()
        writer.writerows(rows)


def sheet_value(text: str) -> str:
    return "'" + text if text.startswith(("=", "+", "-", "@")) else text


def review_content(qa: dict, spans: dict) -> dict:
    sources = "\n\n".join(
        f"{span_id}: {spans[span_id]['document_number']} · {spans[span_id]['locator']} · {spans[span_id]['url']}\n"
        f"{spans[span_id]['quoted_text']}" for span_id in qa["citation_span_ids"]
    )
    return {"question_text": sheet_value(qa["question_text"]),
            "answer_text": sheet_value(qa["answer_text"]), "sources_for_review": sheet_value(sources)}


def write_review_sheet(output: Path, sample: list[dict], rows: list[dict], spans: list[dict], *, compact: bool) -> None:
    qa_by_id = {row["qa_id"]: row for row in rows}
    span_by_id = {span["span_id"]: span for span in spans}
    name, columns = ((SHORT_REVIEW_NAME, SHORT_REVIEW_COLUMNS) if compact
                     else ("manual-review.csv", (*REVIEW_COLUMNS, *REVIEW_CONTENT)))
    review = []
    for spec in sample:
        row = {**spec, **review_content(qa_by_id[spec["qa_id"]], span_by_id)}
        review.append({column: row.get(column, "") for column in columns})
    csv_write(output / name, review, columns)


def sample_rows(rows: list[dict], stage: str, seed: int, sampled_at: str) -> list[dict]:
    grouped = defaultdict(list)
    for row in rows:
        stratum = "|".join([row["scope_group"], row["question_origin"], *row["source_version_ids"]])
        grouped[(row["split"], stratum)].append(row)
    rng = random.Random(seed)
    result = []
    for (split, stratum), group in sorted(grouped.items()):
        count = len(group) if stage == "pilot" else (len(group) + 4) // 5
        for row in sorted(rng.sample(group, count), key=lambda entry: entry["qa_id"]):
            qa_id = row["qa_id"]
            result.append({
                "qa_review_id": str(uuid5(NAMESPACE_URL, f"d2-review/{row['dataset_version']}/{qa_id}/{row['record_version']}")),
                "qa_id": qa_id, "qa_record_version": row["record_version"], "dataset_version": row["dataset_version"],
                "split": split, "sampling_stratum": stratum, "sampling_seed": str(seed), "sampled_at": sampled_at,
                "source_version_ids": ";".join(row["source_version_ids"]), "required_span_ids": ";".join(row["citation_span_ids"]),
            })
    return result


def prepare(args: argparse.Namespace) -> dict:
    output = private_path(args.output)
    ledger_bytes = args.ledger.read_bytes()
    recipe_bytes = args.recipes.read_bytes()
    recipes = json.loads(recipe_bytes)
    rows, spans = build_candidates(recipes, json.loads(ledger_bytes))
    require(args.stage != "pilot" or len(rows) <= 100, "Pilot tối đa 100 QA; dùng --stage main cho tập chính")
    sampled_at = now()
    sample = sample_rows(rows, args.stage, recipes["seed"], sampled_at)
    near = lexical_candidates(rows)
    payload = {"qa.jsonl": jsonl_bytes(rows), "source-spans.json": json_bytes(spans), "sample.json": json_bytes(sample),
               "near-duplicates.json": json_bytes(near)}
    manifest = {
        "dataset_version": recipes["dataset_version"], "stage": args.stage, "prepared_at": sampled_at,
        "normalization_version": NORMALIZATION, "seed": recipes["seed"], "family_splits": recipes["family_splits"],
        "source_ledger_sha256": sha(ledger_bytes), "recipes_sha256": sha(recipe_bytes),
        "builder_sha256": file_sha(Path(__file__)),
        "files": {name: sha(data) for name, data in payload.items()},
        "qa_per_split": dict(Counter(row["split"] for row in rows)),
        "review_required_per_split": dict(Counter(row["split"] for row in sample)),
        "near_duplicate_candidates": len(near),
        "status": "candidate_only",
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        (output / name).write_bytes(data)
    (output / "manifest.json").write_bytes(json_bytes(manifest))
    write_review_sheet(output, sample, rows, spans, compact=False)
    return manifest


def reviewer_ok(reviewer, reviewed_at, earliest: str) -> bool:
    if not isinstance(reviewer, str) or not REVIEWER.fullmatch(reviewer) or not isinstance(reviewed_at, str):
        return False
    try:
        reviewed = datetime.fromisoformat(reviewed_at)
        return reviewed.tzinfo is not None and datetime.fromisoformat(earliest) <= reviewed <= datetime.now(timezone.utc)
    except ValueError:
        return False


def completed_reviews(path: Path, sample: list[dict], rows: list[dict], spans: dict, *, allow_short: bool) -> list[str]:
    records = {row["qa_id"]: row for row in rows}
    seen, approved, issues = set(), Counter(), []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        short = reader.fieldnames == list(SHORT_REVIEW_COLUMNS)
        require(short or reader.fieldnames == [*REVIEW_COLUMNS, *REVIEW_CONTENT],
                "Cột CSV không khớp phiếu đầy đủ hoặc phiếu rút gọn do công cụ xuất")
        require(not short or allow_short, "Phiếu rút gọn chỉ áp dụng cho pilot; tập chính cần phiếu đầy đủ")
        key = "qa_review_id" if short else "qa_id"
        expected = {row[key]: row for row in sample}
        for row in reader:
            require(None not in row and all(value is not None for value in row.values()),
                    f"Dòng CSV sai số cột (kết thúc ở dòng {reader.line_num})")
            review_id = row[key]
            require(review_id in expected and review_id not in seen, "Phiếu chứa QA ngoài mẫu hoặc lặp dòng")
            seen.add(review_id)
            spec = expected[review_id]
            qa_id = spec["qa_id"]
            qa = records[qa_id]
            if not short:
                require(all(row[field] == value for field, value in spec.items()), f"Sai phiên bản/mẫu kiểm: {qa_id}")
            for field, value in review_content(qa, spans).items():
                require(normalize(row[field]) == normalize(value), f"Không sửa cột nội dung phiếu: {qa_id}/{field}")
            decision = row["decision"].strip()
            follow_up = not short and bool(row["follow_up_batch_key"].strip())
            if short:
                require(decision in {"", "approved", "rework", "rejected"}, f"Quyết định không hợp lệ: {qa_id}")
                require(decision not in {"rework", "rejected"} or row["review_note"].strip(),
                        f"Ghi lý do khi yêu cầu sửa/loại: {qa_id}")
                # Approved trên phiếu rút gọn là xác nhận của người kiểm cho toàn bộ rubric.
                passed = decision == "approved"
                if decision and not reviewer_ok(row["reviewer_id"].strip(), row["reviewed_at"].strip(), spec["sampled_at"]):
                    issues.append(f"Quyết định chưa có mã người kiểm hoặc thời điểm hợp lệ: {qa_id}")
                    continue
            else:
                cited = [entry.strip() for entry in row["citation_span_ids_checked"].split(";") if entry.strip()]
                passed = (
                    decision == "approved"
                    and len(cited) == len(qa["citation_span_ids"]) and set(cited) == set(qa["citation_span_ids"])
                    and row["content_correctness"] == row["citation_verifiability"] == "pass"
                    and all(row[field] in {"pass", "not_applicable"} for field in ("completeness", "scope_and_refusal"))
                    and all(row[field] == "false" for field in ("hallucination_flag", "privacy_flag", "duplicate_or_leakage_flag"))
                    and row["reason_codes"].strip() and row["review_note"].strip() and not follow_up
                )
            if passed:
                if short or reviewer_ok(row["reviewer_id"].strip(), row["reviewed_at"].strip(), spec["sampled_at"]):
                    approved[spec["split"]] += 1
                else:
                    issues.append(f"QA đã chọn approved nhưng thiếu/sai mã hoặc thời điểm kiểm: {qa_id}")
            elif decision in {"rework", "rejected"} or follow_up:
                issues.append(f"QA/batch cần sửa và tạo phiên bản mới: {qa_id}")
    for split, count in Counter(row["split"] for row in sample).items():
        if approved[split] != count:
            issues.append(f"{split}: {approved[split]}/{count} phiếu mẫu đạt")
    return issues


def read_candidate_files(path: Path, manifest: dict, names: tuple[str, ...]) -> dict[str, bytes]:
    payload = {}
    for name in names:
        data = (path / name).read_bytes()
        require(sha(data) == manifest["files"][name], f"Hiện vật đã thay đổi: {name}; tạo phiên bản mới")
        payload[name] = data
    return payload


def review_sheet(args: argparse.Namespace) -> dict:
    path = private_path(args.candidate)
    manifest = json.loads((path / "manifest.json").read_bytes())
    require(manifest["status"] == "candidate_only" and manifest["stage"] == "pilot",
            "Chỉ tạo phiếu rút gọn cho gói ứng viên pilot")
    payload = read_candidate_files(path, manifest, ("qa.jsonl", "source-spans.json", "sample.json"))
    sample = json.loads(payload["sample.json"])
    write_review_sheet(path, sample, [json.loads(line) for line in payload["qa.jsonl"].splitlines()],
                       json.loads(payload["source-spans.json"]), compact=True)
    return {"dataset_version": manifest["dataset_version"], "rows": len(sample), "file": str(path / SHORT_REVIEW_NAME)}


def review_gate(args: argparse.Namespace) -> tuple[dict, int]:
    path = args.candidate.resolve()
    manifest_bytes = (path / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest["status"] == "candidate_only", "Đầu vào phải là gói candidate")
    recipe_bytes = args.recipes.read_bytes()
    ledger_bytes = args.ledger.read_bytes()
    require(sha(recipe_bytes) == manifest["recipes_sha256"] and sha(ledger_bytes) == manifest["source_ledger_sha256"],
            "Recipe/sổ nguồn không khớp phiên bản của gói")
    recipes = json.loads(recipe_bytes)
    require(manifest["stage"] in {"pilot", "main"} and manifest["normalization_version"] == NORMALIZATION
            and all(manifest[key] == recipes[key] for key in ("dataset_version", "family_splits", "seed")),
            "Manifest không khớp cấu hình recipe")
    rows, source_spans = build_candidates(recipes, json.loads(ledger_bytes))
    require(manifest["stage"] != "pilot" or len(rows) <= 100, "Gói pilot vượt 100 QA")
    payload = read_candidate_files(path, manifest, ("qa.jsonl", "source-spans.json", "sample.json", "near-duplicates.json"))
    require(payload["qa.jsonl"] == jsonl_bytes(rows) and payload["source-spans.json"] == json_bytes(source_spans),
            "QA hoặc source span không tái lập từ recipe và snapshot")
    spans = {s["span_id"]: s for s in source_spans}
    sample = json.loads(payload["sample.json"])
    candidates = json.loads(payload["near-duplicates.json"])
    require(sample == sample_rows(rows, manifest["stage"], manifest["seed"], manifest["prepared_at"])
            and candidates == lexical_candidates(rows), "Mẫu kiểm hoặc danh sách gần trùng không tái lập")
    count = Counter(row["split"] for row in rows)
    require(dict(count) == manifest["qa_per_split"]
            and dict(Counter(row["split"] for row in sample)) == manifest["review_required_per_split"]
            and len(candidates) == manifest["near_duplicate_candidates"],
            "Số liệu manifest không khớp hiện vật")
    blockers = []
    if manifest["stage"] == "main" and count["train"] < 2000:
        blockers.append(f"Tập chính mới có {count['train']}/2000 QA train")
    if args.review:
        blockers.extend(completed_reviews(args.review, sample, rows, spans, allow_short=manifest["stage"] == "pilot"))
    else:
        blockers.append("Chưa nộp CSV kiểm thủ công")
    if args.audit:
        proof = json.loads(args.audit.read_bytes())
        expected = {"dataset_version", "candidate_manifest_sha256", "reviewer_id", "reviewed_at", "rights_scope",
                    "source_and_split_verified", "semantic_duplicate_audit", "distinct_near_pairs", "notes"}
        require(set(proof) == expected, "Biên bản rà tập chưa đúng schema")
        require(proof["dataset_version"] == manifest["dataset_version"] and proof["candidate_manifest_sha256"] == sha(manifest_bytes),
                "Biên bản rà tập không khớp gói candidate")
        actual_pairs = {(pair["left"], pair["right"]) for pair in candidates}
        reviews = proof["distinct_near_pairs"]
        require(isinstance(reviews, list), "distinct_near_pairs phải là danh sách")
        reviewed_pairs = set()
        for pair in reviews:
            require(set(pair) == {"left", "right", "reason"}, "Mỗi cặp gần trùng cần left/right và lý do")
            key = (pair["left"], pair["right"])
            require(key in actual_pairs and key not in reviewed_pairs, "Cặp gần trùng không khớp gói hoặc lặp")
            text_field(pair["reason"], "distinct_near_pairs/reason")
            reviewed_pairs.add(key)
        if not (reviewer_ok(proof["reviewer_id"], proof["reviewed_at"], manifest["prepared_at"])
                and proof["rights_scope"] == "internal_research_training"
                and proof["source_and_split_verified"] is True and proof["semantic_duplicate_audit"] == "no_unresolved"
                and reviewed_pairs == actual_pairs and text_field(proof["notes"], "audit/notes")):
            blockers.append("Biên bản quyền, phiên bản nguồn, split hoặc gần trùng chưa đạt")
    else:
        blockers.append("Chưa có biên bản nhóm rà quyền, hiệu lực, split và trùng nghĩa")
    status = "blocked" if blockers else f"{manifest['stage']}_sft_ready"
    summary = {"dataset_version": manifest["dataset_version"], "stage": manifest["stage"], "status": status,
               "qa_per_split": dict(count), "candidate_manifest_sha256": sha(manifest_bytes), "blockers": blockers,
               "survey_status": "separate_evaluator_workflow"}
    if blockers or args.output is None:
        return summary, 2 if blockers else 0
    output = private_path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    reviewed_ids = {row["qa_id"] for row in sample}
    approved_rows = []
    for row in rows:
        if row["qa_id"] in reviewed_ids:
            coverage = [{**claim, "status": "human_reviewed"} for claim in row["claim_coverage"]]
            row = {**row, "label_status": "approved", "claim_coverage": coverage}
        else:
            row = {**row, "label_status": "citation_checked"}
        approved_rows.append(row)
    overlap_fields = ("qa_id", "split", "procedure_family_id", "question_text")
    files = {"qa.jsonl": jsonl_bytes(approved_rows), "source-spans.json": payload["source-spans.json"],
             "overlap-qa.jsonl": jsonl_bytes([{field: row[field] for field in overlap_fields} for row in rows])}
    for split in SFT:
        files[f"{split}.jsonl"] = jsonl_bytes([row for row in approved_rows if row["split"] == split])
    for name, data in files.items():
        (output / name).write_bytes(data)
    (output / "manifest.json").write_bytes(json_bytes({
        **summary, "released_at": now(), "family_splits": manifest["family_splits"],
        "manual_review_per_split": manifest["review_required_per_split"],
        "files": {name: sha(data) for name, data in files.items()},
        "manual_review_sha256": file_sha(args.review), "batch_audit_sha256": file_sha(args.audit),
        "use_scope": "internal_research_training",
    }))
    return summary, 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("prepare", help="Tạo gói candidate, không phát hành train")
    build.add_argument("--recipes", type=Path, default=SEED)
    build.add_argument("--ledger", type=Path, default=LEDGER)
    build.add_argument("--stage", choices=("pilot", "main"), default="pilot")
    build.add_argument("--output", type=Path, required=True)
    sheet = commands.add_parser("review-sheet", help="Tạo phiếu rút gọn cho gói candidate đã có; không ghi đè")
    sheet.add_argument("--candidate", type=Path, required=True)
    check = commands.add_parser("check", help="Kiểm khóa dữ liệu; chỉ xuất SFT nếu có --output và đủ gate")
    check.add_argument("--candidate", type=Path, required=True)
    check.add_argument("--recipes", type=Path, default=SEED)
    check.add_argument("--ledger", type=Path, default=LEDGER)
    check.add_argument("--review", type=Path, help="CSV kiểm thủ công đã điền (pilot nhận cả phiếu rút gọn)")
    check.add_argument("--audit", type=Path, help="Biên bản rà tập dữ liệu, có hash khớp candidate manifest")
    check.add_argument("--output", type=Path, help="Thư mục thuần SFT mới, không chứa USER_TEST")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result, code = prepare(args), 0
        elif args.command == "review-sheet":
            result, code = review_sheet(args), 0
        else:
            result, code = review_gate(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code
    except (OSError, AttributeError, KeyError, TypeError, ValueError) as error:
        print(f"D.2: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
