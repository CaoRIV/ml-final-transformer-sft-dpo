"""Prepare an auditable Truyện Kiều character corpus from a pinned revision.

``--audit-rendered`` checks robots and fetches exactly one permitted rendered
``/wiki/`` revision into ``.cache`` with a research-only manifest. It never
approves training or distribution. ``--source-wikitext`` is offline and needs
the exact raw revision plus a human rights attestation before local preparation.
Both modes validate boundaries, then produce NFC splits, train-only vocabulary,
windows, and an actual manifest.
"""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any
import unicodedata
from urllib import robotparser
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SCHEMA_VERSION = "char-corpus-manifest/v1"
SOURCE_TITLE = "Truyện Kiều"
SOURCE_AUTHOR = "Nguyễn Du"
SOURCE_PAGE_ID = 7350
SOURCE_REVISION = 206607
SOURCE_REVISION_TIMESTAMP = "2026-11-07T14:26:11Z"
SOURCE_PERMALINK = (
    "https://vi.wikisource.org/w/index.php?title=Truy%E1%BB%87n_Ki%E1%BB%81u&oldid=206607"
)
SOURCE_RAW_URL = SOURCE_PERMALINK + "&action=raw"
SOURCE_API_URL = (
    "https://vi.wikisource.org/w/api.php?action=query&prop=revisions"
    "&titles=Truy%E1%BB%87n_Ki%E1%BB%81u&rvstartid=206607&rvendid=206607"
    "&rvprop=ids%7Ctimestamp%7Csha1&format=json&formatversion=2"
)
# The immutable MediaWiki revision fingerprint reported by the source API.
EXPECTED_WIKITEXT_SHA1 = "9910643b961054303306d3ace187dcd8dbbd4f3b"
EXPECTED_FIRST_LINE = "Trăm năm trong cõi người ta,"
EXPECTED_LAST_LINE = "Mua vui cũng được một vài trống canh."
EXPECTED_VERSE_LINES = 3254
UNK_TOKEN = "<UNK>"

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_CACHE = ROOT / ".cache" / "char-corpus"
USER_AGENT = "ml-final-transformer-sft-dpo-char-corpus/1.0 (research-only; repository maintainer)"
ROBOTS_URL = "https://vi.wikisource.org/robots.txt"
AUDIT_RENDERED_URL = "https://vi.wikisource.org/wiki/Truy%E1%BB%87n_Ki%E1%BB%81u?oldid=206607"


class PreparationError(RuntimeError):
    """Raised when a corpus prerequisite or invariant is not satisfied."""



class RejectRedirects(HTTPRedirectHandler):
    """Refuse before contacting a target not covered by the robots check."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise PreparationError(f"Refusing redirect from {req.full_url} to {newurl}")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


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


def load_rights_attestation(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise PreparationError(f"Rights attestation does not exist: {path}") from error
    except json.JSONDecodeError as error:
        raise PreparationError(f"Rights attestation is not valid JSON: {path}: {error}") from error

    if not isinstance(parsed, dict):
        raise PreparationError("Rights attestation must be a JSON object.")
    required_equal = {
        "status": "approved",
        "source_title": SOURCE_TITLE,
        "source_revision": SOURCE_REVISION,
        "source_wikitext_sha1": EXPECTED_WIKITEXT_SHA1,
    }
    for key, expected in required_equal.items():
        if parsed.get(key) != expected:
            raise PreparationError(
                f"Rights attestation field {key!r} must equal {expected!r}; got {parsed.get(key)!r}."
            )
    if not isinstance(parsed.get("reviewer_id"), str) or not parsed["reviewer_id"].strip():
        raise PreparationError("Rights attestation must contain a non-empty reviewer_id, not a personal name.")
    parse_utc(parsed.get("reviewed_at_utc"), "reviewed_at_utc")
    parse_utc(parsed.get("retrieved_at_utc"), "retrieved_at_utc")
    if not isinstance(parsed.get("digitization_provenance"), str) or not parsed["digitization_provenance"].strip():
        raise PreparationError("Rights attestation must record digitization_provenance; a bare public-domain claim is insufficient.")
    basis_urls = parsed.get("basis_urls")
    if not isinstance(basis_urls, list) or not basis_urls or not all(isinstance(url, str) and url.startswith("https://") for url in basis_urls):
        raise PreparationError("Rights attestation must contain one or more HTTPS basis_urls.")
    return parsed


def remove_templates(text: str) -> str:
    """Remove balanced MediaWiki templates, including nested templates.

    The pinned poem uses templates for line numbers. Keeping arbitrary template
    output would make a raw-wikitext extraction depend on MediaWiki expansion,
    so any template is excluded rather than guessed at.
    """

    output: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        pair = text[index : index + 2]
        if pair == "{{":
            depth += 1
            index += 2
            continue
        if pair == "}}":
            if depth == 0:
                raise PreparationError("Encountered an unmatched closing template delimiter in the poem body.")
            depth -= 1
            index += 2
            continue
        if depth == 0:
            output.append(text[index])
        index += 1
    if depth:
        raise PreparationError("Encountered an unmatched opening template delimiter in the poem body.")
    return "".join(output)

class RenderedPoemParser(HTMLParser):
    """Extract verse lines from the rendered MediaWiki ``div.poem`` element."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.poem_depth = 0
        self.skip_depth = 0
        self.poem_blocks = 0
        self.current: list[str] = []
        self.lines: list[str] = []

    def flush_line(self) -> None:
        line = unicodedata.normalize("NFC", " ".join("".join(self.current).strip().split()))
        self.current.clear()
        if line:
            self.lines.append(line)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "div" and self.poem_depth == 0 and "poem" in classes:
            self.poem_blocks += 1
            self.poem_depth = 1
            return
        if not self.poem_depth:
            return
        if self.skip_depth:
            self.skip_depth += 1
            return
        if tag == "span" and "OptionText" in classes:
            self.skip_depth = 1
        elif tag == "br":
            self.flush_line()
        elif tag == "div":
            self.poem_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if not self.poem_depth:
            return
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag == "div":
            self.poem_depth -= 1
            if self.poem_depth == 0:
                self.flush_line()

    def handle_data(self, data: str) -> None:
        if self.poem_depth and not self.skip_depth:
            self.current.append(data)


def validate_poem_lines(lines: list[str]) -> list[str]:
    if not lines:
        raise PreparationError("The poem extraction produced no non-empty verse lines.")
    if lines[0] != EXPECTED_FIRST_LINE:
        raise PreparationError(f"First poem line mismatch: {lines[0]!r}")
    if lines[-1] != EXPECTED_LAST_LINE:
        raise PreparationError(f"Last poem line mismatch: {lines[-1]!r}")
    if len(lines) != EXPECTED_VERSE_LINES:
        raise PreparationError(f"Verse-line count mismatch: expected {EXPECTED_VERSE_LINES}, got {len(lines)}.")
    return lines


def extract_rendered_poem_lines(html: str) -> list[str]:
    parser = RenderedPoemParser()
    parser.feed(html)
    parser.close()
    if parser.poem_blocks != 1 or parser.poem_depth:
        raise PreparationError(f"Expected exactly one closed rendered div.poem, found {parser.poem_blocks}.")
    return validate_poem_lines(parser.lines)


def fetch_rendered_audit_html() -> bytes:
    """Fetch only the robots-permitted, immutable rendered revision for research."""

    opener = build_opener(RejectRedirects())
    robots_request = Request(ROBOTS_URL, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"})
    with opener.open(robots_request, timeout=30) as response:
        robots_text = response.read().decode("utf-8")
    rules = robotparser.RobotFileParser()
    rules.parse(robots_text.splitlines())
    if not rules.can_fetch(USER_AGENT, AUDIT_RENDERED_URL):
        raise PreparationError(f"robots.txt disallows the sole audit URL: {AUDIT_RENDERED_URL}")

    request = Request(AUDIT_RENDERED_URL, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with opener.open(request, timeout=30) as response:
        final_url = response.geturl()
        content_type = response.headers.get_content_type()
        payload = response.read()
    expected = urlsplit(AUDIT_RENDERED_URL)
    actual = urlsplit(final_url)
    if (actual.scheme, actual.netloc, actual.path, actual.query) != (
        expected.scheme,
        expected.netloc,
        expected.path,
        expected.query,
    ):
        raise PreparationError(f"Audit fetch redirected away from the pinned rendered revision: {final_url}")
    if content_type != "text/html":
        raise PreparationError(f"Audit fetch returned {content_type!r}, not rendered HTML.")
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PreparationError("Rendered audit response is not UTF-8.") from error
    if not re.search(r'"wgRevisionId"\s*:\s*206607\b', html) or not re.search(r'"wgArticleId"\s*:\s*7350\b', html):
        raise PreparationError("Rendered audit response does not identify the pinned revision/page ID.")
    return payload


def extract_poem_lines(wikitext: str) -> list[str]:
    """Extract exactly the sole ``<poem>`` body, excluding UI and line numbers."""

    poem_blocks = re.findall(r"<poem(?:\s[^>]*)?>(.*?)</poem\s*>", wikitext, flags=re.IGNORECASE | re.DOTALL)
    if len(poem_blocks) != 1:
        raise PreparationError(f"Expected exactly one <poem> block, found {len(poem_blocks)}.")

    poem = re.sub(r"<!--.*?-->", "", poem_blocks[0], flags=re.DOTALL)
    poem = remove_templates(poem)
    if "{{" in poem or "}}" in poem or "[[" in poem or "]]" in poem:
        raise PreparationError("Unexpected MediaWiki markup remains inside the poem body; extraction is intentionally fail-closed.")
    if re.search(r"</?[A-Za-z][^>]*>", poem):
        raise PreparationError("Unexpected HTML markup remains inside the poem body; extraction is intentionally fail-closed.")

    lines: list[str] = []
    for raw_line in poem.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = unicodedata.normalize("NFC", " ".join(raw_line.strip().split()))
        if line:
            lines.append(line)

    if not lines:
        raise PreparationError("The <poem> block produced no non-empty verse lines.")
    if lines[0] != EXPECTED_FIRST_LINE:
        raise PreparationError(f"First poem line mismatch: {lines[0]!r}")
    if lines[-1] != EXPECTED_LAST_LINE:
        raise PreparationError(f"Last poem line mismatch: {lines[-1]!r}")
    if len(lines) != EXPECTED_VERSE_LINES:
        raise PreparationError(f"Verse-line count mismatch: expected {EXPECTED_VERSE_LINES}, got {len(lines)}.")
    return lines


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


def ensure_research_cache(path: Path, label: str) -> None:
    try:
        path.relative_to(RESEARCH_CACHE)
    except ValueError as error:
        raise PreparationError(f"Research-only {label} must remain below {RESEARCH_CACHE}: {path}") from error


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    source_snapshot: tuple[str, bytes] | None = None
    if args.audit_rendered:
        rendered_html = fetch_rendered_audit_html()
        lines = extract_rendered_poem_lines(rendered_html.decode("utf-8"))
        source = {
            "kind": "rendered_html_research_audit",
            "title": SOURCE_TITLE,
            "author": SOURCE_AUTHOR,
            "page_id": SOURCE_PAGE_ID,
            "revision": SOURCE_REVISION,
            "revision_timestamp_utc": SOURCE_REVISION_TIMESTAMP,
            "rendered_url": AUDIT_RENDERED_URL,
            "robots_url": ROBOTS_URL,
            "html_sha256": sha256_bytes(rendered_html),
        }
        status = "research_only_not_approved_for_training_or_distribution"
        rights_attestation = None
        source_snapshot = ("source-rendered-206607.html", rendered_html)
    else:
        source_path = args.source_wikitext.resolve()
        raw_bytes = source_path.read_bytes()
        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            raise PreparationError("Source wikitext has a UTF-8 BOM; save exact UTF-8 bytes from the pinned raw revision.")
        actual_sha1 = sha1_bytes(raw_bytes)
        if actual_sha1 != EXPECTED_WIKITEXT_SHA1:
            raise PreparationError(
                "Pinned-source SHA-1 mismatch: expected "
                f"{EXPECTED_WIKITEXT_SHA1}, got {actual_sha1}. Do not continue with a changed or re-saved source."
            )
        try:
            wikitext = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise PreparationError("Source wikitext is not UTF-8.") from error
        if args.rights_attestation is None:
            raise PreparationError("--rights-attestation is required for local preparation from raw wikitext.")
        lines = extract_poem_lines(wikitext)
        source = {
            "kind": "pinned_raw_wikitext",
            "title": SOURCE_TITLE,
            "author": SOURCE_AUTHOR,
            "page_id": SOURCE_PAGE_ID,
            "revision": SOURCE_REVISION,
            "revision_timestamp_utc": SOURCE_REVISION_TIMESTAMP,
            "permalink": SOURCE_PERMALINK,
            "raw_url": SOURCE_RAW_URL,
            "revision_api_url": SOURCE_API_URL,
            "wikitext_sha1": actual_sha1,
            "wikitext_sha256": sha256_bytes(raw_bytes),
            "local_source_path": str(source_path),
        }
        status = "approved_for_local_preparation"
        rights_attestation = load_rights_attestation(args.rights_attestation.resolve())

    corpus_text = "\n".join(lines) + "\n"
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

    output_dir = args.output_dir.resolve()
    manifest_path = args.manifest.resolve()
    if args.audit_rendered:
        ensure_research_cache(output_dir, "output directory")
        ensure_research_cache(manifest_path, "manifest")
    if output_dir.exists():
        raise PreparationError(f"Refusing to overwrite existing output directory: {output_dir}")
    if manifest_path.exists():
        raise PreparationError(f"Refusing to overwrite existing manifest: {manifest_path}")
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
        if source_snapshot is not None:
            snapshot_path = staging / source_snapshot[0]
            write_bytes(snapshot_path, source_snapshot[1])
            paths["rendered_html"] = snapshot_path

        artifacts = {name: artifact_metadata(path, staging) for name, path in paths.items()}
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "created_at_utc": utc_now(),
            "status": status,
            "source": source,
            "rights_attestation": rights_attestation,
            "extraction": {
                "method": (
                    "rendered div.poem from the pinned page; OptionText line-number spans and surrounding page chrome excluded"
                    if args.audit_rendered
                    else "sole <poem> block from pinned raw wikitext; balanced templates, comments, blank lines, indentation, and surrounding page markup excluded"
                ),
                "normalization": "Unicode NFC; CRLF/CR converted to LF; whitespace collapsed within each verse line; exactly one LF after every retained verse line",
                "expected_first_line": EXPECTED_FIRST_LINE,
                "expected_last_line": EXPECTED_LAST_LINE,
                "expected_verse_lines": EXPECTED_VERSE_LINES,
                "actual_verse_lines": len(lines),
                "content_sha256": sha256_bytes(corpus_text.encode("utf-8")),
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
    source_mode = parser.add_mutually_exclusive_group(required=True)
    source_mode.add_argument("--source-wikitext", type=Path, help="Exact UTF-8 raw wikitext saved from the pinned revision.")
    source_mode.add_argument(
        "--audit-rendered",
        action="store_true",
        help="Fetch only the robots-permitted pinned /wiki rendered page into .cache for research; never approves training or release.",
    )
    parser.add_argument("--rights-attestation", type=Path, help="Human-reviewed JSON approval, required only with --source-wikitext.")
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory for corpus artifacts; it must not already exist.")
    parser.add_argument("--manifest", type=Path, required=True, help="New path for the actual run manifest; it must not already exist.")
    parser.add_argument("--train-fraction", type=float, default=0.9, help="Contiguous prefix fraction for train (default: 0.9).")
    parser.add_argument("--sequence-length", type=int, default=128, help="Stride-length next-character window length (default: 128).")
    args = parser.parse_args()
    if args.audit_rendered and args.rights_attestation is not None:
        parser.error("--rights-attestation only applies to --source-wikitext; research audit has no approval bypass.")
    if not 0.0 < args.train_fraction < 1.0:
        parser.error("--train-fraction must be strictly between 0 and 1.")
    if args.sequence_length < 1:
        parser.error("--sequence-length must be at least 1.")
    return args


def main() -> None:
    try:
        manifest = prepare(parse_args())
    except (OSError, PreparationError) as error:
        raise SystemExit(f"prepare_char_corpus: {error}") from error
    print(
        f"{manifest['status']}: revision {manifest['source']['revision']} "
        f"with {manifest['extraction']['actual_verse_lines']} verse lines.",
        flush=True,
    )


if __name__ == "__main__":
    main()
