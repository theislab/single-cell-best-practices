"""Open every section of the sidebar table of contents, not just the current one.

The theme has no option for this, so the bundles it ships are patched before the site is built.
Both of them have to change: the bundle that prerenders a page decides what the sidebar looks like in the initial payload, and the bundle that hydrates it in the browser decides what happens to the sidebar afterwards.
Patching only the browser side is what a reader sees as the sidebar expanding itself, section by section, once the page is already up.

The same patch drops the effect that puts the sections back the way the theme wants them whenever a navigation settles, so a section a reader collapses stays collapsed.
"""

import re
import subprocess
import sys
from pathlib import Path

DEFAULT_PROJECT = Path("jupyter-book")
THEME = Path("_build/templates/site/myst/book-theme")
SERVER_BUNDLE = Path("build/index.js")
CLIENT_BUNDLES = "public/build/**/*.js"

MARKER = "myst-expand-toc"

# The minified form of `useState(isCurrentSection)` for the open state of a section, together with the effect that restores that state after every navigation.
# Both go: a section starts open and stays as the reader leaves it.
SECTION_STATE = re.compile(
    r"\.default\.useState\((?P<current>\w+)\);"
    r'\(0,[\w$.]+\.useEffect\)\(\(\)=>\{(?P<navigation>\w+)\.state==="idle"'
    r"&&\w+\((?P=current)\)\},\[(?P=navigation)\.state\]\);"
)
OPEN = f".default.useState(true);/* {MARKER} */"


def download(project: Path) -> None:
    """Fetch the theme.

    The build fetches it too, but only once it is about to render with it, which is too late for a patch.
    """
    subprocess.run(
        ["jupyter", "book", "templates", "download", "book-theme", "--site"],
        cwd=project,
        check=True,
    )


def expand(bundle: Path) -> bool:
    """Patch one bundle, reporting whether it renders the sections open afterwards."""
    text = bundle.read_text(encoding="utf-8")
    if MARKER in text:
        return True
    patched, count = SECTION_STATE.subn(OPEN, text)
    if count == 0:
        return False
    bundle.write_text(patched, encoding="utf-8")
    return True


def main() -> None:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROJECT)
    theme = project / THEME
    if not theme.is_dir():
        download(project)
    if not theme.is_dir():
        raise SystemExit(f"{theme} does not exist, nothing to patch")

    server = theme / SERVER_BUNDLE
    if not server.is_file() or not expand(server):
        raise SystemExit(
            f"{server} does not build the sidebar the way it used to; the theme changed, so the table of contents was not expanded"
        )

    clients = [
        bundle for bundle in sorted(theme.glob(CLIENT_BUNDLES)) if expand(bundle)
    ]
    if len(clients) != 1:
        raise SystemExit(
            f"expected one client bundle building the sidebar, patched {len(clients)}; the theme changed, so the table of contents was not expanded"
        )


if __name__ == "__main__":
    main()
