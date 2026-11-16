"""Validate local research QA citations and release gates without network access.

A successful structural check is NOT human review or legal/source approval.
The pilot and source excerpts stay in ignored local folders, not in Git.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(ledger: dict, questions: list[dict], spans: list[dict], root: Path) -> dict:
    sources = {s["source_id"]: s for s in ledger["sources"]}
    if len(sources) != len(ledger["sources"]):
        raise ValueError("Duplicate source_id")
    span_map = {s["span_id"]: s for s in spans}
    if len(span_map) != len(spans):
        raise ValueError("Duplicate span_id")
    texts = {}
    for source_id, source in sources.items():
        snapshot = (root / source["snapshot_path"]).resolve()
        if not snapshot.is_relative_to(root.resolve()):
            raise ValueError(f"Snapshot outside repository: {source_id}")
        raw = snapshot.read_bytes()
        if digest(raw) != source["snapshot_sha256"]:
            raise ValueError(f"Source snapshot hash mismatch: {source_id}")
        texts[source_id] = normalize(raw.decode("utf-8"))
    for policy in ledger.get("access_policies", []):
        snapshot = (root / policy["snapshot_path"]).resolve()
        if not snapshot.is_relative_to(root.resolve()):
            raise ValueError("Policy snapshot outside repository")
        if digest(snapshot.read_bytes()) != policy["snapshot_sha256"]:
            raise ValueError(f"Policy snapshot hash mismatch: {policy['policy_id']}")
    for span_id, span in span_map.items():
        source_id = span["source_id"]
        if source_id not in sources:
            raise ValueError(f"Unknown source for {span_id}")
        quote = span["quoted_text"]
        if not quote.strip() or normalize(quote) not in texts[source_id]:
            raise ValueError(f"Quote not present in source snapshot: {span_id}")
        if digest(quote.encode("utf-8")) != span["span_sha256"]:
            raise ValueError(f"Span hash mismatch: {span_id}")
        if not span.get("locator"):
            raise ValueError(f"Missing source locator: {span_id}")
    ids, questions_seen = set(), set()
    ready, human_reviewed = 0, 0
    for qa in questions:
        qa_id = qa["qa_id"]
        question = normalize(qa["question_text"]).casefold()
        if qa_id in ids or question in questions_seen or not question:
            raise ValueError(f"Duplicate ID/question or empty question: {qa_id}")
        ids.add(qa_id)
        questions_seen.add(question)
        if not qa["answer_text"].strip() or qa["question_origin"] != "authoring":
            raise ValueError(f"Invalid draft answer/origin: {qa_id}")
        if qa["provenance"]["author_type"] != "AI_assistant":
            raise ValueError(f"Pilot authorship not disclosed: {qa_id}")
        citations = qa["citation_span_ids"]
        if not citations or len(citations) != len(set(citations)):
            raise ValueError(f"Missing or repeated citations: {qa_id}")
        if any(s not in span_map for s in citations):
            raise ValueError(f"Unknown citation: {qa_id}")
        cited_sources = {span_map[s]["source_id"] for s in citations}
        if set(qa["source_version_ids"]) != cited_sources:
            raise ValueError(f"Source/citation version mismatch: {qa_id}")
        renderings = qa["citation_rendering"]
        if {r["span_id"] for r in renderings} != set(citations):
            raise ValueError(f"Citation rendering mismatch: {qa_id}")
        for rendering in renderings:
            span = span_map[rendering["span_id"]]
            if rendering["url"] != sources[span["source_id"]]["canonical_url"] or rendering["locator"] != span["locator"]:
                raise ValueError(f"Citation URL/locator mismatch: {qa_id}")
            if f"[{span['span_id']}]" not in qa["answer_text"]:
                raise ValueError(f"Answer lacks citation marker: {qa_id}")
        human = qa["human_review"]
        human_ok = human["status"] == "approved" and bool(human.get("reviewer_id")) and bool(human.get("reviewed_at_utc"))
        if human["status"] == "approved" and not human_ok:
            raise ValueError(f"Human approval lacks reviewer/time: {qa_id}")
        human_reviewed += int(human_ok)
        source_ok = all(sources[s].get("training_allowed") is True for s in cited_sources)
        eligible = human_ok and source_ok and qa["rights_status"] == "approved" and qa["label_status"] == "approved" and qa["split"] in {"train", "validation"} and not qa["quality_flags"]
        if qa.get("training_allowed") is True and not eligible:
            raise ValueError(f"Unsafe training release flag: {qa_id}")
        if qa.get("redistribution_allowed") is True and not all(sources[s].get("redistribution_allowed") is True for s in cited_sources):
            raise ValueError(f"Unsafe redistribution flag: {qa_id}")
        ready += int(eligible and qa.get("training_allowed") is True)
    # High lexical overlap is only a review candidate, never proof of independence.
    near_duplicates = []
    token_sets = [{" ".join(normalize(q["question_text"]).casefold().split()[i:i + 3]) for i in range(max(0, len(normalize(q["question_text"]).split()) - 2))} for q in questions]
    for i, left in enumerate(token_sets):
        for j in range(i + 1, len(token_sets)):
            right = token_sets[j]
            similarity = len(left & right) / len(left | right) if left | right else 0
            if similarity >= 0.85:
                near_duplicates.append({"left": questions[i]["qa_id"], "right": questions[j]["qa_id"], "trigram_jaccard": round(similarity, 4)})
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "check_origin": "agent_executed_structural_validation_not_human_review",
        "qa_count": len(questions), "span_count": len(spans), "source_count": len(sources),
        "procedure_family_counts": dict(Counter(q["procedure_family_id"] for q in questions)),
        "human_approved_qa_count": human_reviewed, "training_ready_qa_count": ready,
        "near_duplicate_candidates": near_duplicates,
        "all_snapshot_hashes_and_quote_locations_match": True,
        "release_status": "not_ready" if ready != len(questions) or not questions else "ready",
        "limits": ["Exact quote checks do not establish answer entailment, legal validity or copyright clearance.", "No real-user survey or DPO labeling is performed.", "Lexical duplicate screening cannot prove absence of semantic duplicates."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=ROOT / "docs/data/source-ledger.json")
    parser.add_argument("--pilot-dir", type=Path, default=ROOT / "data/review/admin-pilot-v1")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-training-ready", action="store_true")
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
        qa_bytes = (args.pilot_dir / "qa.jsonl").read_bytes()
        span_bytes = (args.pilot_dir / "source-spans.json").read_bytes()
        questions = [json.loads(line) for line in qa_bytes.decode("utf-8").splitlines() if line.strip()]
        report = validate(ledger, questions, json.loads(span_bytes), ROOT)
        report["input_sha256"] = {"qa.jsonl": digest(qa_bytes), "source-spans.json": digest(span_bytes)}
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Validation failed: {error}\n")
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if args.require_training_ready and report["release_status"] != "ready":
        parser.exit(2, "Training release blocked; inspect source/version/rights and human-review gates.\n")


if __name__ == "__main__":
    main()
