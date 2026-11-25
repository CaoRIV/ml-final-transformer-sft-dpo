"""Kiểm thử bộ trích thơ bản Trương Vĩnh Ký 1911 đã ghim revision."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import unittest

from scripts import kieu_1911


IDENTITY = (
    '<script>mw.config.set({"wgRevisionId":206466,"wgArticleId":25612});</script>'
)
SNAPSHOT = Path(".cache/char-corpus/source-1911-206466.html")


def snapshot_fragment(body: str) -> str:
    return IDENTITY + '<div class="prp-pages-output">' + body + "</div>"


class Kieu1911ExtractionTest(unittest.TestCase):
    def test_scoped_poems_exclude_editorial_markup_and_normalize(self):
        html = snapshot_fragment(
            "<h2>Đề mục ngoài thơ</h2>"
            "<figure><figcaption>Chú thích ảnh ngoài thơ</figcaption>"
            '<div class="poem"><p>Thơ nằm trong ảnh</p></div></figure>'
            '<div class="poem"><p> Câu que\u0301 <sup class="reference">[1]</sup> cuối. <br />'
            "Ym-niềm (<i>hay là</i> iêm-liềm) trướng xủ màn che,<br />"
            "Con anh (oanh) học nói.<br />"
            "Vưng lời đàn. (đờn)</p></div>"
            "<p>Nội dung ngoài thơ</p>"
        )

        self.assertEqual(
            kieu_1911.extract_verse_lines(html),
            [
                "Câu qué cuối.",
                "Ym-niềm trướng xủ màn che,",
                "Con anh học nói.",
                "Vưng lời đàn.",
            ],
        )

    def test_rejects_wrong_identity_and_ambiguous_markup(self):
        wrong_identity = IDENTITY.replace("206466", "206467") + (
            '<div class="prp-pages-output"><div class="poem"><p>Câu thơ</p></div></div>'
        )
        ambiguous_paragraphs = snapshot_fragment(
            '<div class="poem"><p>Câu một</p><p>Câu hai</p></div>'
        )
        unknown_parenthesis = snapshot_fragment(
            '<div class="poem"><p>Câu (dị bản lạ)</p></div>'
        )

        with self.assertRaisesRegex(ValueError, "identity"):
            kieu_1911.extract_verse_lines(wrong_identity)
        with self.assertRaisesRegex(ValueError, "paragraph structure"):
            kieu_1911.extract_verse_lines(ambiguous_paragraphs)
        with self.assertRaisesRegex(ValueError, "parenthesis"):
            kieu_1911.extract_verse_lines(unknown_parenthesis)

    @unittest.skipUnless(SNAPSHOT.exists(), "cần snapshot HTML A.2 cục bộ")
    def test_pinned_snapshot_fingerprint_and_caption_boundary(self):
        lines = kieu_1911.extract_verse_lines(SNAPSHOT.read_text(encoding="utf-8"))
        corpus = "\n".join(lines) + "\n"

        self.assertEqual(len(lines), 3254)
        self.assertEqual(lines[0], "Trăm năm, trong cõi người-ta,")
        self.assertEqual(lines[-1], "mua vui cũng được một vài trống canh.")
        self.assertIn("xuất thần dây-phút chưa tàng nén hương.", lines)
        self.assertNotIn("Đạo nhơn phục trước tỉnh đàn, xuất thần dây-phút chưa tàn nén-hương.", lines)
        self.assertEqual(
            sha256(corpus.encode("utf-8")).hexdigest(),
            "eddbb40a3f4ad421d8b089f95ad139a372b20c4ec8621a929ba6aa6f9c63abcb",
        )


if __name__ == "__main__":
    unittest.main()
