"""Write the table of contents of the PDF export.

MyST treats the first entry of a table of contents as the project root and leaves it out of every multi-page export, so the PDF built from the book's table of contents has no preamble.
This writes the same table of contents in the Jupyter Book v1 format with the preamble as both the root and the first chapter.
"""

import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG = Path("jupyter-book/myst.yml")
DEFAULT_OUTPUT = Path("jupyter-book/_build/pdf_toc.yml")


def to_chapters(
    entries: Sequence[Mapping[str, Any]], prefix: str
) -> list[dict[str, Any]]:
    chapters = []
    for entry in entries:
        if "file" in entry:
            chapters.append({"file": f"{prefix}{entry['file']}"})
        else:
            chapters.append(
                {
                    "title": entry["title"],
                    "sections": to_chapters(entry["children"], prefix),
                }
            )
    return chapters


def main(config: Path = DEFAULT_CONFIG, output: Path = DEFAULT_OUTPUT) -> None:
    toc = yaml.safe_load(config.read_text())["project"]["toc"]
    prefix = (
        Path(*[".."] * len(output.parent.relative_to(config.parent).parts)).as_posix()
        + "/"
    )
    chapters = to_chapters(toc, prefix)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(
            {"format": "jb-book", "root": chapters[0]["file"], "chapters": chapters},
            sort_keys=False,
        )
    )


if __name__ == "__main__":
    main(*map(Path, sys.argv[1:]))
