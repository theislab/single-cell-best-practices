#!/usr/bin/env python3
"""
Parses the ## Contributors section at the end of .md and .ipynb files,
then prepends a YAML frontmatter block with authors and reviewers to the top.

Usage:
    python add_contributors_frontmatter.py [root_dir]

    root_dir defaults to the current directory if not provided.

The script skips any path whose parts include '_build'.
"""

import sys
import json
import re
from pathlib import Path


# ── Debugging helper ──────────────────────────────────────────────────────────

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv


def debug_parse(path: Path, text: str):
    """Print the raw contributors section so we can see why parsing failed."""
    # Look for any heading that contains 'contributor' (case-insensitive)
    match = re.search(r"(#{1,4}\s*[Cc]ontributor.{0,50})", text)
    if match:
        start = match.start()
        snippet = text[start : start + 400]
        print(f"  [DEBUG] Contributors block in {path}:\n{repr(snippet)}\n")
    else:
        print(f"  [DEBUG] No contributors heading found at all in {path}")


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_contributors(text: str, path: Path = None) -> tuple[list[str], list[str]]:
    """
    Extract authors and reviewers from a Contributors section in markdown text.
    Returns (authors, reviewers).

    Handles:
    - Any number of # before 'Contributors' (## or ###, etc.)
    - Windows-style line endings (\r\n)
    - Notebook source stored as a list of strings (joined before calling this)
    - Names that may have trailing whitespace
    """
    authors, reviewers = [], []

    # Normalise line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Find the contributors section — tolerant of leading #s and spacing
    contrib_match = re.search(r"#{1,4}\s*Contributors\b", text, re.IGNORECASE)
    if not contrib_match:
        if VERBOSE and path:
            debug_parse(path, text)
        return authors, reviewers

    section = text[contrib_match.start():]

    # Authors sub-section
    authors_match = re.search(
        r"#{1,4}\s*Authors\b[^\n]*\n[\s\n]*((?:\s*[-*]\s*.+\n?)+)",
        section, re.IGNORECASE
    )
    if authors_match:
        authors = re.findall(r"[-*]\s*(.+)", authors_match.group(1))

    # Reviewers sub-section
    reviewers_match = re.search(
        r"#{1,4}\s*Reviewers\b[^\n]*\n[\s\n]*((?:\s*[-*]\s*.+\n?)+)",
        section, re.IGNORECASE
    )
    if reviewers_match:
        reviewers = re.findall(r"[-*]\s*(.+)", reviewers_match.group(1))

    authors   = [a.strip() for a in authors   if a.strip()]
    reviewers = [r.strip() for r in reviewers if r.strip()]

    if not authors and not reviewers and VERBOSE and path:
        debug_parse(path, section)

    return authors, reviewers


def build_frontmatter(authors: list[str], reviewers: list[str]) -> str:
    """Build the YAML frontmatter string."""
    lines = ["---", "authors:"]
    for author in authors:
        lines.append(f"  - name: {author}")
    for reviewer in reviewers:
        lines.append(f"  - name: {reviewer}")
        lines.append(f"    roles:")
        lines.append(f"      - reviewer")
    lines.append("---")
    return "\n".join(lines) + "\n"


def already_has_frontmatter(text: str) -> bool:
    return text.lstrip().startswith("---")


def is_excluded(path: Path) -> bool:
    """Skip anything inside a _build directory."""
    return "_build" in path.parts


# ── Markdown files ────────────────────────────────────────────────────────────

def process_md(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    authors, reviewers = parse_contributors(text, path)
    if not authors and not reviewers:
        print(f"  SKIP (no contributors found): {path}")
        return False
    if already_has_frontmatter(text):
        print(f"  SKIP (frontmatter already present): {path}")
        return False
    frontmatter = build_frontmatter(authors, reviewers)
    path.write_text(frontmatter + "\n" + text, encoding="utf-8")
    print(f"  UPDATED: {path}")
    return True


# ── Jupyter notebook files ────────────────────────────────────────────────────

def get_notebook_text(nb: dict) -> str:
    """Concatenate all markdown cell sources into one string for parsing."""
    parts = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = cell.get("source", [])
            if isinstance(source, list):
                parts.append("".join(source))
            else:
                parts.append(source)
    return "\n".join(parts)


def process_ipynb(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        nb = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  ERROR (invalid JSON): {path} — {e}")
        return False

    notebook_text = get_notebook_text(nb)
    authors, reviewers = parse_contributors(notebook_text, path)
    if not authors and not reviewers:
        print(f"  SKIP (no contributors found): {path}")
        return False

    cells = nb.get("cells", [])
    if cells:
        first_source = cells[0].get("source", "")
        if isinstance(first_source, list):
            first_source = "".join(first_source)
        if already_has_frontmatter(first_source):
            print(f"  SKIP (frontmatter already present): {path}")
            return False

    frontmatter = build_frontmatter(authors, reviewers)
    frontmatter_cell = {
        "cell_type": "raw",
        "id": "frontmatter",
        "metadata": {"raw_mimetype": "text/restructuredtext"},
        "source": frontmatter,
    }
    nb["cells"].insert(0, frontmatter_cell)

    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  UPDATED: {path}")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    root = Path(args[0]) if args else Path(".")
    if not root.exists():
        print(f"Error: directory '{root}' does not exist.")
        sys.exit(1)

    md_files    = [p for p in root.rglob("*.md")    if not is_excluded(p)]
    ipynb_files = [p for p in root.rglob("*.ipynb") if not is_excluded(p)]

    print(f"Found {len(md_files)} .md and {len(ipynb_files)} .ipynb files under '{root}' (excluding _build/)\n")
    if VERBOSE:
        print("Verbose mode ON — will print Contributors snippets for skipped files.\n")

    updated = 0
    for path in sorted(md_files):
        if process_md(path):
            updated += 1
    for path in sorted(ipynb_files):
        if process_ipynb(path):
            updated += 1

    print(f"\nDone. {updated} file(s) updated.")


if __name__ == "__main__":
    main()