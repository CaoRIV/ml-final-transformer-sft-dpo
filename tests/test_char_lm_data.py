"""Unit test cho loader v2; fixture chỉ là dữ liệu tổng hợp cục bộ."""

from __future__ import annotations

import tempfile
import unittest
from argparse import Namespace
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import torch

from scripts import prepare_char_corpus as prepared
from src.char_lm_data import (
    CorpusLoadError,
    load_prepared_corpus,
    validate_prepared_corpus,
    windows_from_ids,
)


class CharLMDataTest(unittest.TestCase):
    def _prepare_fixture(self, root: Path) -> Namespace:
        source_html = root / "synthetic-source.html"
        scan_pdf = root / "synthetic-scan.pdf"
        source_html.write_bytes(b"<html>synthetic fixture</html>")
        scan_bytes = b"synthetic scan fixture"
        scan_pdf.write_bytes(scan_bytes)
        lines = ["abab", "đbđa"]
        corpus = ("\n".join(lines) + "\n").encode("utf-8")
        args = Namespace(
            source_html=source_html,
            scan_pdf=scan_pdf,
            fetch=False,
            output_dir=root / "prepared",
            manifest=root / "manifest.json",
            train_fraction=0.5,
            sequence_length=2,
        )
        corpus_sha256 = sha256(corpus).hexdigest()
        with (
            patch.object(prepared, "SCAN_SHA256", sha256(scan_bytes).hexdigest()),
            patch.object(prepared, "CORPUS_SHA256", corpus_sha256),
            patch.object(prepared, "extract_verse_lines", return_value=lines),
        ):
            prepared.prepare(args)
        args.synthetic_corpus_sha256 = corpus_sha256
        return args

    def _write_synthetic_attestation(
        self, manifest_path: Path, path: Path, manifest_sha256: str | None = None, *, platform: str = "colab",
    ) -> None:
        # Đây là object test tạm thời, không phải phê duyệt của cá nhân hay tổ chức.
        path.write_bytes(
            prepared.canonical_json(
                {
                    "status": "approved",
                    "evaluated_for": f"a2-local-and-{platform}",
                    "training_allowed": True,
                    "manifest_sha256": manifest_sha256 or sha256(manifest_path.read_bytes()).hexdigest(),
                    "reviewer_id": "synthetic-test-fixture",
                    "reviewed_at_utc": "2000-01-01T00:00:00Z",
                }
            )
        )

    def test_windows_respect_split_boundary_and_stride(self):
        ids = torch.arange(8, dtype=torch.long)
        actual = windows_from_ids(ids, 3)
        expected = torch.tensor([[0, 1, 2, 3], [3, 4, 5, 6]], dtype=torch.long)
        torch.testing.assert_close(actual, expected)
        self.assertEqual(windows_from_ids(torch.tensor([1, 2, 3]), 3).shape, (0, 4))

    def test_v2_fixture_roundtrip_and_artifact_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self._prepare_fixture(root)
            attestation = root / "synthetic-test-attestation.json"
            self._write_synthetic_attestation(args.manifest, attestation)

            with patch.object(prepared, "CORPUS_SHA256", args.synthetic_corpus_sha256):
                train, valid, vocab, manifest_sha256 = validate_prepared_corpus(args.manifest, args.output_dir)
                loaded_train, loaded_valid, loaded_vocab, loaded_sha256 = load_prepared_corpus(
                    args.manifest, args.output_dir, attestation
                )
                self.assertEqual(manifest_sha256, sha256(args.manifest.read_bytes()).hexdigest())
                self.assertEqual(loaded_sha256, manifest_sha256)
                self.assertEqual(loaded_vocab, vocab)
                torch.testing.assert_close(loaded_train, train)
                torch.testing.assert_close(loaded_valid, valid)
                self.assertNotIn("đ", vocab)
                a, b, newline = vocab["a"], vocab["b"], vocab["\n"]
                self.assertEqual(train.tolist(), [[a, b, a], [a, b, newline]])
                self.assertEqual(valid.tolist(), [[0, b, 0], [0, a, newline]])

                (args.output_dir / "train.txt").write_bytes(b"damaged")
                with self.assertRaises(CorpusLoadError):
                    validate_prepared_corpus(args.manifest, args.output_dir)

    def test_missing_or_mismatched_approval_is_rejected_before_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self._prepare_fixture(root)
            missing = root / "absent-attestation.json"
            with self.assertRaisesRegex(CorpusLoadError, "rights_attestation"):
                load_prepared_corpus(args.manifest, root / "no-artifacts", missing)

            mismatched = root / "mismatched-attestation.json"
            self._write_synthetic_attestation(args.manifest, mismatched, "0" * 64)
            with self.assertRaisesRegex(CorpusLoadError, "manifest_sha256"):
                load_prepared_corpus(args.manifest, root / "no-artifacts", mismatched)

    def test_attestation_must_match_cloud_platform(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = self._prepare_fixture(root)
            attestation = root / "synthetic-test-attestation.json"
            self._write_synthetic_attestation(args.manifest, attestation)
            with self.assertRaisesRegex(CorpusLoadError, "evaluated_for"):
                load_prepared_corpus(args.manifest, args.output_dir, attestation, platform="kaggle")
            self._write_synthetic_attestation(args.manifest, attestation, platform="kaggle")
            with self.assertRaisesRegex(CorpusLoadError, "evaluated_for"):
                load_prepared_corpus(args.manifest, args.output_dir, attestation)
            with patch.object(prepared, "CORPUS_SHA256", args.synthetic_corpus_sha256):
                _, validation, _, _ = load_prepared_corpus(
                    args.manifest, args.output_dir, attestation, platform="kaggle",
                )
            self.assertEqual(validation.size(0), 2)


if __name__ == "__main__":
    unittest.main()
