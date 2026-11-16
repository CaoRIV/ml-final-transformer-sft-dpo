"""Generate complete standalone LaTeX and compile both week-one PDFs.

Requires Pandoc and Tectonic on PATH, or explicit executable paths.
Does not install packages or modify the ML environment.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ROOT / "docs" / "proposal"
TITLES = {"proposal": "Đề cương tuần 1", "data-plan": "Kế hoạch dữ liệu tuần 1"}


def executable(value: str) -> str:
    found = shutil.which(value)
    if found is None:
        raise SystemExit(f"Executable not found: {value}. Supply its path with --pandoc or --tectonic.")
    return str(Path(found).resolve())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pandoc", default="pandoc")
    parser.add_argument("--tectonic", default="tectonic")
    args = parser.parse_args()
    pandoc, tectonic = executable(args.pandoc), executable(args.tectonic)
    build = ROOT / ".cache" / "week1-build"
    build.mkdir(parents=True, exist_ok=True)
    for stem, title in TITLES.items():
        markdown = DOCUMENTS / f"{stem}.md"
        source = DOCUMENTS / f"{stem}.tex"
        subprocess.run(
            [
                pandoc, markdown.name,
                "--from=markdown+tex_math_dollars", "--to=latex", "--standalone",
                "--template=week1-template.tex", "--lua-filter=week1-format.lua",
                "--top-level-division=section", "--metadata", f"title={title}",
                "--output", str(source),
            ],
            cwd=DOCUMENTS, check=True,
        )
        digest = hashlib.sha256(markdown.read_bytes()).hexdigest()
        source.write_text(
            f"% Generated from {markdown.name}; edit the Markdown, then rebuild.\n"
            f"% Markdown SHA256: {digest}\n" + source.read_text(encoding="utf-8"),
            encoding="utf-8", newline="\n",
        )
        subprocess.run(
            [tectonic, "--keep-logs", "--outdir", str(build), source.name],
            cwd=DOCUMENTS, check=True,
        )
        shutil.copyfile(build / f"{stem}.pdf", DOCUMENTS / f"{stem}.pdf")
        print(f"Built docs/proposal/{stem}.tex and docs/proposal/{stem}.pdf", flush=True)


if __name__ == "__main__":
    main()
