"""Nạp và kiểm tra corpus ký tự đã chuẩn bị theo manifest v2."""

from __future__ import annotations

import json
import unicodedata
from hashlib import sha256
from pathlib import Path
from typing import Any

import torch
from torch import Tensor

from scripts import prepare_char_corpus as prepared


class CorpusLoadError(RuntimeError):
    """Manifest hoặc artifact corpus không thỏa hợp đồng huấn luyện cục bộ."""


_ARTIFACT_FILES = {
    "corpus": "corpus.txt",
    "train": "train.txt",
    "validation": "validation.txt",
    "vocab": "vocab.json",
    "train_windows": "train_windows.jsonl",
    "validation_windows": "validation_windows.jsonl",
}


def _fail(message: str) -> None:
    raise CorpusLoadError(message)


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(f"{label} phải là JSON object.")
    return value


def _json_object(payload: bytes, label: str) -> dict[str, Any]:
    try:
        return _mapping(json.loads(payload.decode("utf-8")), label)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CorpusLoadError(f"{label} không phải JSON UTF-8 hợp lệ.") from error


def _canonical_json(payload: bytes, label: str) -> dict[str, Any]:
    data = _json_object(payload, label)
    if prepared.canonical_json(data) != payload:
        _fail(f"{label} phải dùng canonical JSON của script chuẩn bị.")
    return data


def _expect_equal(mapping: dict[str, Any], field: str, expected: Any, label: str) -> None:
    actual = mapping.get(field)
    if actual != expected or type(actual) is not type(expected):
        _fail(f"{label}.{field} không khớp giá trị ghim.")


def _expect_fields(mapping: dict[str, Any], expected: set[str], label: str) -> None:
    if set(mapping) != expected:
        _fail(f"{label} có trường khác schema chuẩn bị.")


def _is_hex_digest(value: Any, length: int) -> bool:
    return isinstance(value, str) and len(value) == length and all(char in "0123456789abcdef" for char in value)


def _read_manifest(manifest_path: Path) -> tuple[dict[str, Any], str]:
    try:
        payload = manifest_path.read_bytes()
    except OSError as error:
        raise CorpusLoadError(f"Không đọc được manifest: {manifest_path}") from error
    manifest = _canonical_json(payload, "manifest")
    _expect_fields(
        manifest,
        {"schema_version", "created_at_utc", "status", "source", "extraction", "split", "vocabulary", "windows", "artifacts"},
        "manifest",
    )
    _expect_equal(manifest, "schema_version", prepared.SCHEMA_VERSION, "manifest")
    _expect_equal(manifest, "status", "prepared_pending_training_review", "manifest")
    try:
        prepared.parse_utc(manifest.get("created_at_utc"), "created_at_utc")
    except prepared.PreparationError as error:
        raise CorpusLoadError(str(error)) from error
    return manifest, sha256(payload).hexdigest()


def _verify_attestation(path: Path, manifest_sha256: str, platform: str) -> None:
    try:
        attestation = _json_object(path.read_bytes(), "rights_attestation")
    except OSError as error:
        raise CorpusLoadError(f"Không đọc được rights_attestation: {path}") from error
    _expect_fields(
        attestation,
        {"status", "evaluated_for", "training_allowed", "manifest_sha256", "reviewer_id", "reviewed_at_utc"},
        "rights_attestation",
    )
    _expect_equal(attestation, "status", "approved", "rights_attestation")
    _expect_equal(attestation, "evaluated_for", f"a2-local-and-{platform}", "rights_attestation")
    _expect_equal(attestation, "training_allowed", True, "rights_attestation")
    _expect_equal(attestation, "manifest_sha256", manifest_sha256, "rights_attestation")
    reviewer = attestation["reviewer_id"]
    if not isinstance(reviewer, str) or not reviewer.strip():
        _fail("rights_attestation.reviewer_id phải là định danh người duyệt không rỗng.")
    try:
        prepared.parse_utc(attestation["reviewed_at_utc"], "reviewed_at_utc")
    except prepared.PreparationError as error:
        raise CorpusLoadError(str(error)) from error


def _verify_source(manifest: dict[str, Any]) -> None:
    source = _mapping(manifest.get("source"), "source")
    _expect_fields(source, set(prepared.SOURCE) | {"rendered_sha256"}, "source")
    for field, expected in prepared.SOURCE.items():
        _expect_equal(source, field, expected, "source")
    if not _is_hex_digest(source["rendered_sha256"], 64):
        _fail("source.rendered_sha256 không phải SHA-256 chữ thường hợp lệ.")


def _read_artifacts(artifact_dir: Path, artifacts: Any) -> dict[str, bytes]:
    metadata = _mapping(artifacts, "artifacts")
    if set(metadata) != set(_ARTIFACT_FILES):
        _fail("artifacts phải có đúng các artifact của preparation.")
    try:
        root = artifact_dir.resolve(strict=True)
    except OSError as error:
        raise CorpusLoadError(f"Không mở được artifact_dir: {artifact_dir}") from error
    if not root.is_dir():
        _fail("artifact_dir phải là thư mục.")

    payloads: dict[str, bytes] = {}
    for name, filename in _ARTIFACT_FILES.items():
        record = _mapping(metadata[name], f"artifacts.{name}")
        _expect_fields(record, {"path", "byte_count", "sha256"}, f"artifacts.{name}")
        if record["path"] != filename:
            _fail(f"artifacts.{name}.path không phải đường dẫn artifact chuẩn.")
        if not isinstance(record["byte_count"], int) or isinstance(record["byte_count"], bool) or record["byte_count"] < 0:
            _fail(f"artifacts.{name}.byte_count không hợp lệ.")
        if not _is_hex_digest(record["sha256"], 64):
            _fail(f"artifacts.{name}.sha256 không hợp lệ.")
        try:
            path = (root / filename).resolve(strict=True)
            path.relative_to(root)
            if not path.is_file():
                _fail(f"Artifact {name} không phải tệp thường.")
            payload = path.read_bytes()
        except (OSError, ValueError) as error:
            raise CorpusLoadError(f"Không đọc được artifact {name}.") from error
        if len(payload) != record["byte_count"] or sha256(payload).hexdigest() != record["sha256"]:
            _fail(f"Kiểm tra hash hoặc kích thước artifact {name} thất bại.")
        payloads[name] = payload
    return payloads


def _decode_text(payload: bytes, label: str) -> str:
    if payload.startswith(b"\xef\xbb\xbf"):
        _fail(f"{label} không được có UTF-8 BOM.")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CorpusLoadError(f"{label} không phải UTF-8.") from error


def _verify_text_and_split(manifest: dict[str, Any], payloads: dict[str, bytes]) -> tuple[str, str]:
    corpus_text = _decode_text(payloads["corpus"], "corpus.txt")
    train_text = _decode_text(payloads["train"], "train.txt")
    validation_text = _decode_text(payloads["validation"], "validation.txt")
    if (
        not corpus_text.endswith("\n")
        or "\r" in corpus_text
        or unicodedata.normalize("NFC", corpus_text) != corpus_text
    ):
        _fail("corpus.txt không tuân thủ chuẩn hoá text của preparation.")
    lines = corpus_text[:-1].split("\n")
    if not lines or any(not line or " ".join(line.split()) != line for line in lines):
        _fail("corpus.txt không gồm các câu thơ đã chuẩn hoá.")

    extraction = _mapping(manifest.get("extraction"), "extraction")
    _expect_fields(
        extraction,
        {"method", "normalization", "actual_verse_lines", "content_sha256", "content_codepoints"},
        "extraction",
    )
    content_sha256 = sha256(payloads["corpus"]).hexdigest()
    expected_extraction = {
        "method": prepared.EXTRACTION_METHOD,
        "normalization": prepared.NORMALIZATION,
        "actual_verse_lines": len(lines),
        "content_sha256": content_sha256,
        "content_codepoints": len(corpus_text),
    }
    if content_sha256 != prepared.CORPUS_SHA256:
        _fail("corpus.txt không khớp SHA-256 corpus đã khóa.")
    for field, expected in expected_extraction.items():
        _expect_equal(extraction, field, expected, "extraction")

    split = _mapping(manifest.get("split"), "split")
    _expect_fields(
        split,
        {"method", "train_fraction", "boundary_codepoint_offset", "train_codepoints", "validation_codepoints", "cross_split_overlap"},
        "split",
    )
    fraction = split["train_fraction"]
    if not isinstance(fraction, (int, float)) or isinstance(fraction, bool) or not 0 < fraction < 1:
        _fail("split.train_fraction phải nằm giữa 0 và 1.")
    expected_split = {
        "method": "single contiguous code-point boundary before windowing; train is the prefix and validation the suffix",
        "boundary_codepoint_offset": len(train_text),
        "train_codepoints": len(train_text),
        "validation_codepoints": len(validation_text),
        "cross_split_overlap": False,
    }
    for field, expected in expected_split.items():
        _expect_equal(split, field, expected, "split")
    if int(len(corpus_text) * fraction) != len(train_text) or train_text + validation_text != corpus_text:
        _fail("Các split không tái tạo corpus theo boundary code-point đã khai báo.")
    return train_text, validation_text


def _verify_vocab(manifest: dict[str, Any], payload: bytes, train_text: str) -> dict[str, int]:
    vocab = _canonical_json(payload, "vocab.json")
    expected_vocab = prepared.make_vocab(train_text)
    if vocab != expected_vocab:
        _fail("vocab.json không phải từ vựng chỉ học từ split train.")
    vocabulary = _mapping(manifest.get("vocabulary"), "vocabulary")
    _expect_fields(vocabulary, {"learned_from", "token_count", "unk_token", "unk_id", "unknown_character_policy"}, "vocabulary")
    expected_metadata = {
        "learned_from": "train only",
        "token_count": len(expected_vocab["token_to_id"]),
        "unk_token": prepared.UNK_TOKEN,
        "unk_id": 0,
        "unknown_character_policy": "validation-only characters encode as 0; vocabulary is not extended after the split",
    }
    for field, expected in expected_metadata.items():
        _expect_equal(vocabulary, field, expected, "vocabulary")
    return expected_vocab["token_to_id"]


def windows_from_ids(ids: Tensor, length: int) -> Tensor:
    """Tạo các cửa sổ ``[N, length + 1]`` stride ``length`` trong một split."""

    if not isinstance(ids, Tensor) or ids.ndim != 1 or ids.dtype != torch.long:
        raise ValueError("ids phải là LongTensor một chiều.")
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length phải là số nguyên dương.")
    if ids.numel() < length + 1:
        return ids.new_empty((0, length + 1))
    return ids.unfold(0, length + 1, length)


def _windows_for_split(text: str, token_to_id: dict[str, int], length: int) -> Tensor:
    ids = torch.tensor(prepared.encode(text, token_to_id), dtype=torch.long)
    return windows_from_ids(ids, length)


def _verify_windows(
    manifest: dict[str, Any], payloads: dict[str, bytes], train_text: str, validation_text: str, token_to_id: dict[str, int]
) -> tuple[Tensor, Tensor]:
    metadata = _mapping(manifest.get("windows"), "windows")
    _expect_fields(
        metadata,
        {
            "sequence_length", "stride", "construction", "train_count", "validation_count",
            "train_discarded_tail_codepoints", "validation_discarded_tail_codepoints",
        },
        "windows",
    )
    length = metadata["sequence_length"]
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        _fail("windows.sequence_length phải là số nguyên dương.")
    _expect_equal(metadata, "stride", length, "windows")
    _expect_equal(
        metadata,
        "construction",
        "input and next-character target are emitted only when all sequence_length + 1 code points belong to the same split",
        "windows",
    )
    expected_train_jsonl, expected_train_count, expected_train_tail = prepared.window_records(train_text, token_to_id, length)
    expected_validation_jsonl, expected_validation_count, expected_validation_tail = prepared.window_records(
        validation_text, token_to_id, length
    )
    if payloads["train_windows"] != expected_train_jsonl or payloads["validation_windows"] != expected_validation_jsonl:
        _fail("Artifact JSONL windows không khớp next-token windows tái dựng từ split đã kiểm tra.")
    expected_metadata = {
        "train_count": expected_train_count,
        "validation_count": expected_validation_count,
        "train_discarded_tail_codepoints": expected_train_tail,
        "validation_discarded_tail_codepoints": expected_validation_tail,
    }
    for field, expected in expected_metadata.items():
        _expect_equal(metadata, field, expected, "windows")
    train_windows = _windows_for_split(train_text, token_to_id, length)
    validation_windows = _windows_for_split(validation_text, token_to_id, length)
    if train_windows.size(0) != expected_train_count or validation_windows.size(0) != expected_validation_count:
        _fail("Cửa sổ tensor tái dựng không khớp metadata.")
    return train_windows, validation_windows


def _validate_manifest(
    manifest: dict[str, Any], artifact_dir: Path, manifest_sha256: str
) -> tuple[Tensor, Tensor, dict[str, int], str]:
    _verify_source(manifest)
    payloads = _read_artifacts(artifact_dir, manifest.get("artifacts"))
    train_text, validation_text = _verify_text_and_split(manifest, payloads)
    token_to_id = _verify_vocab(manifest, payloads["vocab"], train_text)
    train_windows, validation_windows = _verify_windows(manifest, payloads, train_text, validation_text, token_to_id)
    return train_windows, validation_windows, token_to_id, manifest_sha256


def validate_prepared_corpus(manifest_path: Path, artifact_dir: Path) -> tuple[Tensor, Tensor, dict[str, int], str]:
    """Kiểm tra output chuẩn bị v2, không quyết định quyền huấn luyện."""

    manifest, manifest_sha256 = _read_manifest(manifest_path)
    return _validate_manifest(manifest, artifact_dir, manifest_sha256)


def load_prepared_corpus(
    manifest_path: Path, artifact_dir: Path, rights_attestation: Path, *, platform: str = "colab",
) -> tuple[Tensor, Tensor, dict[str, int], str]:
    """Nạp corpus khi xác nhận khớp manifest và nền tảng chạy đã chọn."""
    if platform not in ("colab", "kaggle"):
        raise CorpusLoadError(f"Nền tảng A.2 không được hỗ trợ: {platform}")

    manifest, manifest_sha256 = _read_manifest(manifest_path)
    _verify_attestation(rights_attestation, manifest_sha256, platform)
    return _validate_manifest(manifest, artifact_dir, manifest_sha256)
