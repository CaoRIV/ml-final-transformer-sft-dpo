"""Trích câu thơ từ bản Trương Vĩnh Ký 1911 đã ghim revision."""

from __future__ import annotations

from html.parser import HTMLParser
import re
import unicodedata


SOURCE_REVISION = 206466
SOURCE_PAGE_ID = 25612
SOURCE_URL = (
    "https://vi.wikisource.org/w/index.php?title="
    "Truy%E1%BB%87n_Ki%E1%BB%81u_(b%E1%BA%A3n_Tr%C6%B0%C6%A1ng_V%C4%A9nh_K%C3%BD_1911)"
    "/Kim,_V%C3%A2n,_Ki%E1%BB%81u_truy%E1%BB%87n&oldid=206466"
)
EXTRACTION_METHOD = (
    "stdlib HTMLParser: p lines in div.poem descendants of div.prp-pages-output; "
    "reference superscripts, figures, captions, headings, and out-of-poem markup excluded; "
    "only the three observed editorial parenthetical alternatives are removed"
)
NORMALIZATION = (
    "Unicode NFC; collapse whitespace within each verse line; remove only the observed "
    "editorial parenthetical alternatives '(hay là iêm-liềm)', '(oanh)', and '(đờn)'; "
    "caller joins retained lines with LF"
)

_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
})
_EXCLUDED_TAGS = frozenset({"sup", "figure", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6"})
_IDENTITY_RE = re.compile(r'"(?P<key>wgRevisionId|wgArticleId)"\s*:\s*(?P<value>\d+)')
_EDITORIAL_CHOICES = frozenset({"(hay là iêm-liềm)", "(oanh)", "(đờn)"})



def _class_tokens(attrs: list[tuple[str, str | None]]) -> set[str]:
    for name, value in attrs:
        if name == "class" and value:
            return set(value.split())
    return set()


def _validate_identity(html: str) -> None:
    identities: dict[str, set[int]] = {"wgRevisionId": set(), "wgArticleId": set()}
    for match in _IDENTITY_RE.finditer(html):
        identities[match["key"]].add(int(match["value"]))
    if identities != {
        "wgRevisionId": {SOURCE_REVISION},
        "wgArticleId": {SOURCE_PAGE_ID},
    }:
        raise ValueError("unexpected Wikisource snapshot identity")


def _remove_editorial_parentheses(text: str) -> str:
    """Bỏ đúng ba dị bản biên tập quan sát trong snapshot đã ghim."""
    for choice in _EDITORIAL_CHOICES:
        text = text.replace(choice, "")
    if "(" in text or ")" in text:
        raise ValueError("unexpected editorial parenthesis in verse line")
    return text


def _normalize_line(text: str) -> str:
    line = _remove_editorial_parentheses(text)
    line = " ".join(line.split())
    line = unicodedata.normalize("NFC", line)
    if not line:
        raise ValueError("empty verse line after normalization")
    return line


class _PoemParser(HTMLParser):
    """Parser hẹp cho cấu trúc rendered HTML cụ thể của snapshot này."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[tuple[str, int]] = []
        self._scope_depth: int | None = None
        self._scope_count = 0
        self._poem_depth: int | None = None
        self._poem_start = 0
        self._paragraph_depth: int | None = None
        self._paragraph_count = 0
        self._excluded_depths: list[int] = []
        self._line_parts: list[str] = []
        self.lines: list[str] = []

    @property
    def _in_paragraph(self) -> bool:
        return self._paragraph_depth is not None

    @property
    def _in_poem(self) -> bool:
        return self._poem_depth is not None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._start(tag, attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._start(tag, attrs)

    def _start(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            if self._in_paragraph and not self._excluded_depths:
                self._finish_line()
            return
        if tag in _VOID_TAGS:
            return

        self._stack.append((tag, self.getpos()[0]))
        depth = len(self._stack)
        classes = _class_tokens(attrs)

        if tag == "div" and "prp-pages-output" in classes:
            if self._scope_depth is not None or self._scope_count:
                raise ValueError("ambiguous prp-pages-output scope")
            self._scope_depth = depth
            self._scope_count += 1
            return

        if self._scope_depth is not None and tag == "div" and "poem" in classes:
            if self._in_poem:
                raise ValueError("nested poem block")
            if any(open_tag == "figure" for open_tag, _ in self._stack[:-1]):
                return
            self._poem_depth = depth
            self._poem_start = len(self.lines)
            self._paragraph_count = 0
            return

        if self._in_poem and tag == "p":
            if depth != self._poem_depth + 1 or self._in_paragraph or self._paragraph_count:
                raise ValueError("ambiguous paragraph structure in poem block")
            self._paragraph_depth = depth
            self._paragraph_count = 1
            return

        if self._in_paragraph and tag in _EXCLUDED_TAGS:
            self._excluded_depths.append(depth)

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID_TAGS:
            raise ValueError(f"unexpected closing tag </{tag}>")
        if not self._stack or self._stack[-1][0] != tag:
            raise ValueError(f"mismatched closing tag </{tag}>")

        depth = len(self._stack)
        if self._excluded_depths and self._excluded_depths[-1] == depth:
            self._excluded_depths.pop()

        if tag == "p" and self._paragraph_depth == depth:
            self._finish_line()
            self._paragraph_depth = None

        if tag == "div" and self._poem_depth == depth:
            if self._in_paragraph or self._excluded_depths or not self._paragraph_count:
                raise ValueError("unclosed content in poem block")
            if len(self.lines) == self._poem_start:
                raise ValueError("empty poem block")
            self._poem_depth = None

        if tag == "div" and self._scope_depth == depth:
            if self._in_poem:
                raise ValueError("unclosed poem in prp-pages-output scope")
            self._scope_depth = None

        self._stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_paragraph:
            if not self._excluded_depths:
                self._line_parts.append(data)
        elif self._in_poem and data.strip():
            raise ValueError("text outside paragraph in poem block")

    def _finish_line(self) -> None:
        raw_line = "".join(self._line_parts)
        self._line_parts.clear()
        if raw_line.strip():
            self.lines.append(_normalize_line(raw_line))

    def finish(self) -> list[str]:
        if self._stack:
            raise ValueError("unclosed HTML structure")
        if self._scope_depth is not None or self._in_poem or self._in_paragraph:
            raise ValueError("unclosed extraction scope")
        if self._scope_count != 1 or not self.lines:
            raise ValueError("no verse lines in prp-pages-output scope")
        return self.lines


def extract_verse_lines(html: str) -> list[str]:
    """Trả về các câu thơ đã chuẩn hoá từ snapshot HTML xác định duy nhất."""
    _validate_identity(html)
    parser = _PoemParser()
    parser.feed(html)
    parser.close()
    return parser.finish()
