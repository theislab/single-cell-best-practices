"""
Run this against one of your skipped notebooks to see what the script actually sees.

Usage:
    python diagnose.py path/to/skipped.ipynb
"""
import sys, json, re
from pathlib import Path

path = Path(sys.argv[1])
nb = json.loads(path.read_text(encoding="utf-8"))

for i, cell in enumerate(nb.get("cells", [])):
    if cell.get("cell_type") != "markdown":
        continue
    source = cell.get("source", [])
    joined = "".join(source) if isinstance(source, list) else source
    if re.search(r"contributor", joined, re.IGNORECASE):
        print(f"=== Cell {i} (markdown) — raw source field ===")
        print(repr(source))
        print("\n=== Joined text ===")
        print(repr(joined))
        break
else:
    print("No markdown cell containing 'contributor' found.")
    print("Cell types present:", [c.get("cell_type") for c in nb.get("cells", [])])