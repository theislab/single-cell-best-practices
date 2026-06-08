#!/usr/bin/env python3
"""
Adds `numbering:\n  offset: 0` to the frontmatter of all content .md and .ipynb files,
so that nested TOC children are numbered as top-level (1, 2, 3 instead of 0.1, 0.2).

Also sets numbering: false on files listed in UNNUMBERED.

Usage:
    python add_offset.py [root_dir]
"""

import sys
import re
import json
from pathlib import Path

# Files that should NOT be numbered (relative to root)
UNNUMBERED = {
    "preamble.md",
    "outlook.md",
    "acknowledgements.md",
    "glossary.md",
    "CHANGELOG.md",
}

def is_excluded(path: Path) -> bool:
    return "_build" in path.parts


def inject_into_yaml(text: str, key: str, value: str) -> str:
    """Insert key: value into an existing --- frontmatter block."""
    return re.sub(r"^---\n", f"---\n{key}: {value}\n", text, count=1)


def process_md(path: Path, unnumbered: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    numbering_value = "false" if unnumbered else "offset: 0\n  "

    if unnumbered:
        new_key_block = "numbering: false\n"
    else:
        new_key_block = "numbering:\n  offset: 0\n"

    # Check if numbering key already present
    if re.search(r"^numbering:", text, re.MULTILINE):
        print(f"  SKIP (numbering already set): {path}")
        return False

    if text.lstrip().startswith("---"):
        new_text = re.sub(r"^---\n", f"---\n{new_key_block}", text, count=1)
    else:
        new_text = f"---\n{new_key_block}---\n\n" + text

    path.write_text(new_text, encoding="utf-8")
    label = "UNNUMBERED" if unnumbered else "OFFSET"
    print(f"  [{label}] {path}")
    return True


def process_ipynb(path: Path, unnumbered: bool) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    if not cells:
        return False

    first = cells[0]
    if first.get("cell_type") != "markdown":
        print(f"  SKIP (first cell not markdown): {path}")
        return False

    source = first.get("source", "")
    if isinstance(source, list):
        source = "".join(source)

    if not source.lstrip().startswith("---"):
        print(f"  SKIP (no frontmatter in first cell): {path}")
        return False

    if re.search(r"^numbering:", source, re.MULTILINE):
        print(f"  SKIP (numbering already set): {path}")
        return False

    if unnumbered:
        new_key_block = "numbering: false\n"
    else:
        new_key_block = "numbering:\n  offset: 0\n"

    new_source = re.sub(r"^---\n", f"---\n{new_key_block}", source, count=1)
    first["source"] = new_source
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    label = "UNNUMBERED" if unnumbered else "OFFSET"
    print(f"  [{label}] {path}")
    return True


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

    md_files    = [p for p in root.rglob("*.md")    if not is_excluded(p)]
    ipynb_files = [p for p in root.rglob("*.ipynb") if not is_excluded(p)]

    print(f"Found {len(md_files)} .md and {len(ipynb_files)} .ipynb files\n")

    updated = 0
    for path in sorted(md_files):
        unnumbered = path.name in UNNUMBERED
        if process_md(path, unnumbered):
            updated += 1
    for path in sorted(ipynb_files):
        if process_ipynb(path, unnumbered=False):
            updated += 1

    print(f"\nDone. {updated} file(s) updated.")

if __name__ == "__main__":
    main()