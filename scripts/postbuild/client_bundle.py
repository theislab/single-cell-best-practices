"""Append a client side workaround to the JavaScript bundle of a built site.

The theme is a Remix application that hydrates `<head>` and `<body>`, so a `<script>` tag injected into the built HTML breaks hydration on every page.
"""

import re
import sys
from pathlib import Path

ENTRY_GLOB = "entry.client-*.js"
DEFAULT_ROOT = Path("jupyter-book/_build/html")


def patch_client_entry(marker: str, snippet: str, description: str) -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT)
    if not root.is_dir():
        raise SystemExit(f"{root} does not exist, nothing to patch")

    entries = sorted((root / "build").glob(ENTRY_GLOB))
    if not entries:
        raise SystemExit(
            f"no {ENTRY_GLOB} under {root / 'build'}; the theme's bundle layout changed, so {description} was not applied"
        )

    # Every page imports the same client entry, so patch the ones a page actually loads.
    pages = [p for p in root.rglob("*.html") if "/build/" not in p.as_posix()]
    referenced = {
        m.group(1)
        for page in pages
        for m in re.finditer(
            r'/build/(entry\.client-[^"\')]+\.js)', page.read_text(encoding="utf-8")
        )
    }
    if not referenced:
        raise SystemExit("no page imports a client entry bundle")

    for entry in entries:
        if entry.name not in referenced:
            continue
        text = entry.read_text(encoding="utf-8")
        if marker in text:
            continue
        entry.write_text(text + snippet, encoding="utf-8")

    missing = referenced - {e.name for e in entries}
    if missing:
        raise SystemExit(f"pages import missing entry bundles: {sorted(missing)}")
