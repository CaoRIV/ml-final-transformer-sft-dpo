"""Load the minimized, review-gated D.2 release and build SFT examples."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from uuid import UUID

SYSTEM_PROMPT = (
    "Bạn là trợ lý hỗ trợ thủ tục hành chính hộ tịch và chứng thực tại Hà Nội. "
    "Trả lời chính xác, thận trọng, giữ nguyên trích dẫn trong câu trả lời "
    "và nêu rõ khi thông tin không đủ."
)
_SPLITS = frozenset(("train", "validation"))
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_RENDERED_CITATION = re.compile(r"^([^\n\[\],:][^\n\[\]]*), ([^\n\[\],:][^\n\[\]]*): (https?://\S+)$")
_FORBIDDEN_DELIMITERS = frozenset((
    "<|im_start|>", "<|im_end|>", "<|endoftext|>", "<|eot_id|>", "<|start_header_id|>", "<|end_header_id|>",
))


class ReleaseLoadError(ValueError):
    """The staged release is not a complete, approved D.2 SFT release."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseLoadError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseLoadError(f"Không đọc được {label}: {error}") from error
    _require(isinstance(value, dict), f"{label} phải là JSON object")
    return value


def _proof_hash(value: Any, label: str) -> None:
    _require(isinstance(value, str) and _SHA256.fullmatch(value) is not None, f"{label} phải là SHA-256 hex")


def _validate_manifest(manifest: dict[str, Any]) -> dict[str, str]:
    status = manifest.get("status")
    stage = manifest.get("stage")
    _require(stage in {"pilot", "main"} and status == f"{stage}_sft_ready", "Release chưa qua review gate")
    _require(manifest.get("use_scope") == "internal_research_training", "Release không có phạm vi huấn luyện nội bộ")
    _require(manifest.get("blockers") == [], "Release còn blocker")
    _require(isinstance(manifest.get("dataset_version"), str) and manifest["dataset_version"].strip(), "Thiếu dataset_version")
    _proof_hash(manifest.get("candidate_manifest_sha256"), "candidate_manifest_sha256")
    _proof_hash(manifest.get("manual_review_sha256"), "manual_review_sha256")
    _proof_hash(manifest.get("batch_audit_sha256"), "batch_audit_sha256")

    families = manifest.get("family_splits")
    _require(isinstance(families, dict) and families, "family_splits phải có ít nhất một họ thủ tục")
    _require(all(isinstance(key, str) and key and value in _SPLITS | {"holdout"} for key, value in families.items()),
             "family_splits không hợp lệ")

    expected_counts = manifest.get("qa_per_split")
    _require(isinstance(expected_counts, dict) and set(expected_counts) == _SPLITS
             and all(type(count) is int and count > 0 for count in expected_counts.values()),
             "qa_per_split phải có số dương cho train và validation")
    review_counts = manifest.get("manual_review_per_split")
    _require(isinstance(review_counts, dict) and set(review_counts) == _SPLITS
             and all(type(count) is int and 0 < count <= expected_counts[split] for split, count in review_counts.items()),
             "manual_review_per_split không khớp qa_per_split")
    if stage == "pilot":
        _require(sum(expected_counts.values()) <= 100, "Pilot vượt tối đa 100 QA")
        _require(review_counts == expected_counts, "Pilot phải review toàn bộ QA")
    else:
        _require(expected_counts["train"] >= 2000, "Tập chính cần tối thiểu 2000 QA train")
        _require(all(review_counts[split] >= (expected_counts[split] + 4) // 5 for split in _SPLITS),
                 "Tập chính phải review ít nhất ceil(20%) ở mỗi split")
    _require(manifest.get("survey_status") == "separate_evaluator_workflow",
             "Survey phải tách khỏi release SFT")

    files = manifest.get("files")
    expected_file_names = {"qa.jsonl", "source-spans.json", "overlap-qa.jsonl", "train.jsonl", "validation.jsonl"}
    _require(isinstance(files, dict) and set(files) == expected_file_names,
             "files không đúng manifest release D.2")
    for name, digest in files.items():
        _proof_hash(digest, f"files/{name}")
    return files


def _parse_jsonl(data: bytes, split: str) -> list[dict[str, Any]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReleaseLoadError(f"{split}.jsonl không phải UTF-8: {error}") from error
    _require(text.endswith("\n"), f"{split}.jsonl phải kết thúc bằng newline")
    lines = text.splitlines()
    _require(lines, f"{split}.jsonl rỗng")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(lines, 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ReleaseLoadError(f"{split}.jsonl dòng {number} không phải JSON: {error}") from error
        _require(isinstance(row, dict), f"{split}.jsonl dòng {number} phải là object")
        rows.append(row)
    return rows


def _nonempty_text(row: dict[str, Any], field: str, label: str) -> str:
    value = row.get(field)
    _require(isinstance(value, str) and value.strip(), f"{label}/{field} phải là văn bản không rỗng")
    return value


def _validate_row(row: dict[str, Any], split: str, families: dict[str, str], dataset_version: str, seen_ids: set[str]) -> str:
    label = f"{split}/{row.get('qa_id', '?')}"
    required = {
        "qa_id", "record_version", "dataset_version", "split", "scope_group", "procedure_family_id", "question_text",
        "question_origin", "language", "answer_text", "citation_span_ids", "citation_rendering", "source_version_ids",
        "claim_coverage", "label_status", "provenance",
    }
    _require(set(row) == required, f"{label} không đúng schema D.2; không nhận dữ liệu user/test")
    qa_id = _nonempty_text(row, "qa_id", label)
    try:
        UUID(qa_id)
    except ValueError as error:
        raise ReleaseLoadError(f"{label}/qa_id không phải UUID") from error
    _require(qa_id not in seen_ids, f"qa_id lặp giữa các split: {qa_id}")
    seen_ids.add(qa_id)
    _require(row["dataset_version"] == dataset_version, f"{label} khác dataset_version manifest")
    _require(row["split"] == split, f"{label} nằm sai split")
    family = _nonempty_text(row, "procedure_family_id", label)
    _require(families.get(family) == split, f"{label} vi phạm family_splits hoặc là holdout")
    _require(row.get("scope_group") == "hanoi-ho-tich-chung-thuc" and row.get("language") == "vi"
             and row.get("question_origin") == "authoring", f"{label} sai phạm vi D.2")
    _require(row.get("label_status") in {"approved", "citation_checked"}, f"{label} chưa được xác minh D.2")
    _nonempty_text(row, "record_version", label)
    question = _nonempty_text(row, "question_text", label)
    _require(not any(token in question for token in _FORBIDDEN_DELIMITERS), f"{label}/question_text chứa delimiter chat")
    answer = _nonempty_text(row, "answer_text", label)

    citation_ids = row.get("citation_span_ids")
    coverage = row.get("claim_coverage")
    _require(isinstance(citation_ids, list) and citation_ids and all(isinstance(item, str) and item for item in citation_ids)
             and len(citation_ids) == len(set(citation_ids)), f"{label}/citation_span_ids không hợp lệ")
    rendering = _nonempty_text(row, "citation_rendering", label).splitlines()
    _require(len(rendering) == len(citation_ids), f"{label}/citation_rendering không khớp citation")
    citations: dict[str, tuple[str, str]] = {}
    for span_id, rendered in zip(citation_ids, rendering, strict=True):
        match = _RENDERED_CITATION.fullmatch(rendered)
        _require(match is not None, f"{label}/citation_rendering không đúng dạng D.2")
        document, locator, _url = match.groups()
        citations[span_id] = (document, locator)

    _require(isinstance(coverage, list) and coverage, f"{label}/claim_coverage không hợp lệ")
    first_seen_ids: list[str] = []
    for claim in coverage:
        _require(isinstance(claim, dict) and set(claim) == {"claim_text", "source_span_id", "status"},
                 f"{label}/claim_coverage sai schema")
        claim_text = claim.get("claim_text")
        source_id = claim.get("source_span_id")
        _require(isinstance(claim_text, str) and claim_text.strip() and isinstance(source_id, str) and source_id in citations,
                 f"{label}/claim_coverage thiếu claim hoặc span")
        expected_claim_status = "human_reviewed" if row["label_status"] == "approved" else "candidate_pending_manual_review"
        _require(claim.get("status") == expected_claim_status,
                 f"{label}/claim_coverage không khớp label_status")
        if source_id not in first_seen_ids:
            first_seen_ids.append(source_id)
        document, locator = citations[source_id]
        _require(f"{claim_text} [{document}, {locator}]" in answer,
                 f"{label}/answer_text không giữ nguyên trích dẫn đã render")
    _require(first_seen_ids == citation_ids, f"{label}/claim_coverage không giữ thứ tự citation gốc")

    source_versions = row.get("source_version_ids")
    _require(isinstance(source_versions, list) and source_versions and all(isinstance(item, str) and item for item in source_versions)
             and len(source_versions) == len(set(source_versions)), f"{label}/source_version_ids không hợp lệ")
    provenance = row.get("provenance")
    _require(isinstance(provenance, dict)
             and set(provenance) == {"method", "recipe_key", "author_type"}
             and provenance.get("method") == "curated_claim_recipe"
             and isinstance(provenance.get("recipe_key"), str) and provenance["recipe_key"]
             and provenance.get("author_type") in {"AI_assistant", "human", "mixed", "not_declared"},
             f"{label}/provenance không phải D.2")
    return row["label_status"]


def load_release(path: Path) -> tuple[dict, dict[str, list[dict]]]:
    """Load exactly ``manifest.json``, ``train.jsonl`` and ``validation.jsonl`` from a gated release."""
    root = Path(path)
    manifest = _read_json(root / "manifest.json", "manifest.json")
    files = _validate_manifest(manifest)
    payload: dict[str, bytes] = {}
    for split in sorted(_SPLITS):
        name = f"{split}.jsonl"
        try:
            payload[split] = (root / name).read_bytes()
        except OSError as error:
            raise ReleaseLoadError(f"Không đọc được {name}: {error}") from error
        _require(_sha256(payload[split]) == files[name], f"{name} không khớp SHA-256 manifest")

    splits = {split: _parse_jsonl(payload[split], split) for split in _SPLITS}
    families = manifest["family_splits"]
    seen_ids: set[str] = set()
    approved = Counter()
    for split, rows in splits.items():
        for row in rows:
            if _validate_row(row, split, families, manifest["dataset_version"], seen_ids) == "approved":
                approved[split] += 1
    actual_counts = {split: len(splits[split]) for split in _SPLITS}
    _require(actual_counts == manifest["qa_per_split"], "qa_per_split không khớp số dòng release")
    _require(dict(approved) == manifest["manual_review_per_split"],
             "Số QA approved không khớp manual_review_per_split")
    return manifest, {"train": splits["train"], "validation": splits["validation"]}


def _chat_ids(tokenizer: Any, messages: list[dict[str, str]], *, add_generation_prompt: bool) -> list[int]:
    try:
        ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=add_generation_prompt)
    except Exception as error:
        raise ValueError(f"Không render được chat template: {error}") from error
    if isinstance(ids, dict):
        ids = ids.get("input_ids")
    if ids and isinstance(ids[0], list):
        _require(len(ids) == 1, "Chat template trả về batch thay vì một ví dụ")
        ids = ids[0]
    _require(isinstance(ids, list) and all(type(token) is int for token in ids), "Chat template phải trả về danh sách token")
    return ids


def encode_qa(row: dict, tokenizer: Any, max_length: int) -> dict[str, list[int]]:
    """Encode one verified record, masking the system/user prompt from causal-LM loss."""
    _require(type(max_length) is int and max_length > 0, "max_length phải là số nguyên dương")
    question = row.get("question_text")
    answer = row.get("answer_text")
    _require(isinstance(question, str) and question.strip() and isinstance(answer, str) and answer.strip(),
             "QA cần question_text và answer_text không rỗng")
    special_tokens = set(_FORBIDDEN_DELIMITERS)
    for value in getattr(tokenizer, "all_special_tokens", ()):
        if isinstance(value, str):
            special_tokens.add(value)
    _require(not any(token and (token in question or token in answer) for token in special_tokens),
             "question_text hoặc answer_text chứa delimiter hoặc special token chat")

    prompt_messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": question}]
    prompt_ids = _chat_ids(tokenizer, prompt_messages, add_generation_prompt=True)
    full_ids = _chat_ids(tokenizer, [*prompt_messages, {"role": "assistant", "content": answer}], add_generation_prompt=False)
    _require(full_ids[:len(prompt_ids)] == prompt_ids, "Chat template không giữ prompt-prefix khi thêm đáp án")
    assistant_ids = full_ids[len(prompt_ids):]
    _require(assistant_ids, "Chat template tạo target rỗng")
    eos_id = getattr(tokenizer, "eos_token_id", None)
    _require(type(eos_id) is int, "Tokenizer không có eos_token_id")
    eos_positions = [index for index, token in enumerate(assistant_ids) if token == eos_id]
    _require(len(eos_positions) <= 1, "Chat template tạo nhiều EOS trong target")
    if eos_positions:
        full_ids = full_ids[:len(prompt_ids) + eos_positions[0] + 1]
    else:
        full_ids = [*full_ids, eos_id]
    _require(len(full_ids) <= max_length,
             f"Ví dụ có {len(full_ids)} token vượt max_length={max_length}; tăng max_length, không được truncate")
    labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]
    _require(any(label != -100 for label in labels), "Target sau mask rỗng")
    return {"input_ids": full_ids, "attention_mask": [1] * len(full_ids), "labels": labels}
