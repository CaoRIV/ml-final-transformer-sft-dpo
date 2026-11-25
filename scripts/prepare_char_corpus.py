"""Chuẩn bị corpus A.2 từ bản Quốc ngữ Trương Vĩnh Ký 1911.

Đọc snapshot và scan đã lưu, hoặc lấy đúng hai URL nguồn sau khi kiểm robots.
Manifest v2 mô tả dữ liệu; không thể hiện phê duyệt huấn luyện của nhóm.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import shutil
import tempfile
from typing import Any
import unicodedata
from urllib import robotparser
from urllib.parse import urlsplit
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .kieu_1911 import EXTRACTION_METHOD, NORMALIZATION, SOURCE_PAGE_ID, SOURCE_REVISION, SOURCE_URL, extract_verse_lines


SCHEMA_VERSION = "char-corpus-manifest/v2"
SCAN_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf"
SCAN_RECORD_URL = "https://commons.wikimedia.org/wiki/File:Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf"
SCAN_SHA256 = "d60d1b9620300aa0e31dfdf12a3499e3eb72f2236191dd5a9f70cc696711e5d8"
# Khóa phần thơ đã đối chiếu mẫu; oldid không khóa nội dung các trang con được nhúng.
CORPUS_SHA256 = "eddbb40a3f4ad421d8b089f95ad139a372b20c4ec8621a929ba6aa6f9c63abcb"
SOURCE = {
    "kind": "wikisource_rendered_1911",
    "title": "Kim, Vân, Kiều truyện",
    "author": "Nguyễn Du",
    "transcriber": "Trương Vĩnh Ký",
    "edition": "F.-H. Schneider, Sài Gòn, ấn bản thứ ba, 1911",
    "page_id": SOURCE_PAGE_ID,
    "revision": SOURCE_REVISION,
    "rendered_url": SOURCE_URL,
    "scan_url": SCAN_URL,
    "scan_record_url": SCAN_RECORD_URL,
    "scan_sha256": SCAN_SHA256,
}
UNK_TOKEN = "<UNK>"

USER_AGENT = "ml-final-transformer-sft-dpo-char-corpus/1.1 (university coursework; one edition snapshot)"


class PreparationError(RuntimeError):
    """Raised when a corpus prerequisite or invariant is not satisfied."""



class RejectRedirects(HTTPRedirectHandler):
    """Refuse before contacting a target not covered by the robots check."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise PreparationError(f"Refusing redirect from {req.full_url} to {newurl}")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise PreparationError(f"Rights attestation field {field_name!r} must be a non-empty UTC timestamp.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise PreparationError(f"Rights attestation field {field_name!r} is not ISO-8601: {value!r}") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise PreparationError(f"Rights attestation field {field_name!r} must be an explicit UTC timestamp: {value!r}")
    return value


def fetch_snapshot(url: str, expected_content_type: str) -> bytes:
    """Kiểm robots của từng host, không gọi API hoặc tự theo redirect."""
    location = urlsplit(url)
    robots_url = f"{location.scheme}://{location.netloc}/robots.txt"
    opener = build_opener(RejectRedirects())
    headers = {"User-Agent": USER_AGENT}
    rules = robotparser.RobotFileParser()
    try:
        with opener.open(Request(robots_url, headers=headers), timeout=30) as response:
            rules.parse(response.read().decode("utf-8").splitlines())
    except HTTPError as error:
        if error.code not in (404, 410):
            raise
        rules.allow_all = True
    if not rules.can_fetch(USER_AGENT, url):
        raise PreparationError(f"robots.txt chặn URL: {url}")
    with opener.open(Request(url, headers=headers), timeout=30) as response:
        if response.headers.get_content_type() != expected_content_type:
            raise PreparationError(f"Kiểu nội dung không khớp tại {url}")
        return response.read()


def source_bytes(path: Path, *, fetch: bool, url: str, content_type: str) -> bytes:
    if path.exists() or not fetch:
        return path.read_bytes()
    data = fetch_snapshot(url, content_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)
    return data


def make_vocab(train_text: str) -> dict[str, Any]:
    characters = sorted(set(train_text))
    if UNK_TOKEN in characters:
        raise PreparationError(f"Reserved token {UNK_TOKEN!r} unexpectedly occurs as one character.")
    token_to_id = {UNK_TOKEN: 0}
    token_to_id.update({character: index for index, character in enumerate(characters, start=1)})
    return {
        "schema_version": "char-vocab/v1",
        "normalization": "Unicode NFC; LF line endings; no leading/trailing whitespace per verse line",
        "learned_from_split": "train",
        "unk_token": UNK_TOKEN,
        "unk_id": 0,
        "unknown_character_policy": "Encode a character absent from the train vocabulary as unk_id (0); never extend the vocabulary from validation.",
        "token_to_id": token_to_id,
    }


def encode(text: str, token_to_id: dict[str, int]) -> list[int]:
    return [token_to_id.get(character, 0) for character in text]


def window_records(text: str, token_to_id: dict[str, int], sequence_length: int) -> tuple[bytes, int, int]:
    """Build stride-length next-character windows wholly inside one split."""

    if sequence_length < 1:
        raise PreparationError("sequence_length must be at least 1.")
    last_start = len(text) - sequence_length - 1
    records: list[str] = []
    for start in range(0, max(last_start + 1, 0), sequence_length):
        source = text[start : start + sequence_length + 1]
        if len(source) != sequence_length + 1:
            continue
        ids = encode(source, token_to_id)
        records.append(json.dumps({"input_ids": ids[:-1], "target_ids": ids[1:]}, ensure_ascii=False, separators=(",", ":")))
    discarded_tail = len(text) - (len(records) * sequence_length + (1 if records else 0))
    payload = (("\n".join(records) + "\n") if records else "").encode("utf-8")
    return payload, len(records), discarded_tail


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def artifact_metadata(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "byte_count": len(data),
        "sha256": sha256_bytes(data),
    }


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = args.output_dir.resolve()
    manifest_path = args.manifest.resolve()
    if output_dir.exists() or manifest_path.exists():
        raise PreparationError("Thư mục hiện vật và manifest phải là đường dẫn mới.")

    scan = source_bytes(args.scan_pdf, fetch=args.fetch, url=SCAN_URL, content_type="application/pdf")
    if sha256_bytes(scan) != SCAN_SHA256:
        raise PreparationError("SHA-256 bản quét không khớp ấn bản Commons đã đối chiếu.")
    html = source_bytes(args.source_html, fetch=args.fetch, url=SOURCE_URL, content_type="text/html")
    lines = extract_verse_lines(html.decode("utf-8"))

    corpus_text = "\n".join(lines) + "\n"
    content_sha256 = sha256_bytes(corpus_text.encode("utf-8"))
    if content_sha256 != CORPUS_SHA256:
        raise PreparationError(f"Phần thơ không khớp SHA-256 đã khóa: {content_sha256}. Kiểm lại thay đổi từ trang nhúng.")
    if unicodedata.normalize("NFC", corpus_text) != corpus_text:
        raise PreparationError("Internal error: corpus is not NFC after normalization.")

    boundary = int(len(corpus_text) * args.train_fraction)
    train_text, validation_text = corpus_text[:boundary], corpus_text[boundary:]
    if not train_text or not validation_text:
        raise PreparationError("The requested train_fraction leaves an empty split.")
    if len(train_text) < args.sequence_length + 1 or len(validation_text) < args.sequence_length + 1:
        raise PreparationError("A split is too short for one next-character window at the requested sequence length.")
    if train_text + validation_text != corpus_text:
        raise PreparationError("Internal error: contiguous split does not reconstruct the corpus.")

    vocab = make_vocab(train_text)
    token_to_id = vocab["token_to_id"]
    train_windows, train_window_count, train_discarded_tail = window_records(train_text, token_to_id, args.sequence_length)
    validation_windows, validation_window_count, validation_discarded_tail = window_records(
        validation_text, token_to_id, args.sequence_length
    )
    if not train_window_count or not validation_window_count:
        raise PreparationError("At least one window is required in both splits.")

    output_dir.parent.mkdir(parents=True, exist_ok=True)

    staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent))
    try:
        corpus_path = staging / "corpus.txt"
        train_path = staging / "train.txt"
        validation_path = staging / "validation.txt"
        vocab_path = staging / "vocab.json"
        train_windows_path = staging / "train_windows.jsonl"
        validation_windows_path = staging / "validation_windows.jsonl"
        paths = {
            "corpus": corpus_path,
            "train": train_path,
            "validation": validation_path,
            "vocab": vocab_path,
            "train_windows": train_windows_path,
            "validation_windows": validation_windows_path,
        }
        write_bytes(corpus_path, corpus_text.encode("utf-8"))
        write_bytes(train_path, train_text.encode("utf-8"))
        write_bytes(validation_path, validation_text.encode("utf-8"))
        write_bytes(vocab_path, canonical_json(vocab))
        write_bytes(train_windows_path, train_windows)
        write_bytes(validation_windows_path, validation_windows)
        artifacts = {name: artifact_metadata(path, staging) for name, path in paths.items()}
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "created_at_utc": utc_now(),
            "status": "prepared_pending_training_review",
            "source": {**SOURCE, "rendered_sha256": sha256_bytes(html)},
            "extraction": {
                "method": EXTRACTION_METHOD,
                "normalization": NORMALIZATION,
                "actual_verse_lines": len(lines),
                "content_sha256": content_sha256,
                "content_codepoints": len(corpus_text),
            },
            "split": {
                "method": "single contiguous code-point boundary before windowing; train is the prefix and validation the suffix",
                "train_fraction": args.train_fraction,
                "boundary_codepoint_offset": boundary,
                "train_codepoints": len(train_text),
                "validation_codepoints": len(validation_text),
                "cross_split_overlap": False,
            },
            "vocabulary": {
                "learned_from": "train only",
                "token_count": len(token_to_id),
                "unk_token": UNK_TOKEN,
                "unk_id": 0,
                "unknown_character_policy": "validation-only characters encode as 0; vocabulary is not extended after the split",
            },
            "windows": {
                "sequence_length": args.sequence_length,
                "stride": args.sequence_length,
                "construction": "input and next-character target are emitted only when all sequence_length + 1 code points belong to the same split",
                "train_count": train_window_count,
                "validation_count": validation_window_count,
                "train_discarded_tail_codepoints": train_discarded_tail,
                "validation_discarded_tail_codepoints": validation_discarded_tail,
            },
            "artifacts": artifacts,
        }
        os.replace(staging, output_dir)
        staging = None  # Ownership transferred to output_dir.
        write_bytes(manifest_path, canonical_json(manifest))
    finally:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-html", type=Path, required=True, help="Snapshot HTML của trang thơ revision 206466.")
    parser.add_argument("--scan-pdf", type=Path, required=True, help="Bản scan Commons đã khóa SHA-256.")
    parser.add_argument("--fetch", action="store_true", help="Chỉ tải file nguồn còn thiếu, sau khi kiểm robots; không ghi đè.")
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory for corpus artifacts; it must not already exist.")
    parser.add_argument("--manifest", type=Path, required=True, help="New path for the actual run manifest; it must not already exist.")
    parser.add_argument("--train-fraction", type=float, default=0.9, help="Contiguous prefix fraction for train (default: 0.9).")
    parser.add_argument("--sequence-length", type=int, default=128, help="Stride-length next-character window length (default: 128).")
    args = parser.parse_args()
    if not 0.0 < args.train_fraction < 1.0:
        parser.error("--train-fraction must be strictly between 0 and 1.")
    if args.sequence_length < 1:
        parser.error("--sequence-length must be at least 1.")
    return args


def main() -> None:
    try:
        manifest = prepare(parse_args())
    except (OSError, ValueError, PreparationError) as error:
        raise SystemExit(f"prepare_char_corpus: {error}") from error
    print(
        f"{manifest['status']}: revision {manifest['source']['revision']} "
        f"with {manifest['extraction']['actual_verse_lines']} verse lines.",
        flush=True,
    )


if __name__ == "__main__":
    main()
