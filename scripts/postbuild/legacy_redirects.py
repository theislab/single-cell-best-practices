"""Keep the pre Jupyter Book v2 URLs of the book reachable.

The Sphinx era site served every chapter as `<source path>.html`, so a reader arrived at `/preprocessing_visualization/quality_control.html`.
Jupyter Book v2 serves the same chapter at `/preprocessing-visualization/quality-control`: no extension, and hyphens where the source path has underscores.
Publishing the v2 build therefore turned every link into the book, including the ones in the papers that cite it, into a 404.

GitHub Pages has no server side redirects, so each old path is answered with a small HTML file carrying a meta refresh and a canonical link.
A generated 404 page catches everything the table of contents does not describe: chapters the v2 book dropped, `genindex.html`, `search.html`, and any other stale `.html` URL still in circulation.
"""

import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path("jupyter-book/_build/html")
DEFAULT_TOC = Path("jupyter-book/myst.yml")

MARKER = "myst-legacy-redirect"

TOC_ENTRY = re.compile(r"^\s*-\s+file:\s*(\S+)\s*$")
SOURCE_SUFFIX = re.compile(r"\.(md|ipynb)$")

# Every URL here is site root relative, never absolute: the same files are served from www.sc-best-practices.org, from the Netlify deploy previews, and from a local preview, and a redirect that hardcoded one of those hosts would send readers off the other two.
STUB = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="generator" content="{marker}" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <link rel="canonical" href="{target}" />
    <title>Redirecting to {target}</title>
  </head>
  <body>
    <p>This page moved to <a href="{target}">{target}</a>.</p>
  </body>
</html>
"""

NOT_FOUND = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="generator" content="{marker}" />
    <title>Page not found</title>
    <script>
      /* The book moved from "/some_chapter/some_page.html" to "/some-chapter/some-page".
         Every path the table of contents knows about is answered by a redirect file, so whatever reaches this page is a chapter the v2 book dropped or a URL that never existed.
         Rewrite it the same way, and send the reader to the chapter if that route is real and to the front page if it is not.
         Rewriting only paths that end in ".html" is what keeps this from looping: a rewritten path never does. */
      (function () {{
        var path = window.location.pathname;
        if (!/\\.html$/.test(path)) return;
        var routes = {routes};
        var rewritten = path.replace(/\\.html$/, "").toLowerCase().replace(/_/g, "-");
        window.location.replace(routes.indexOf(rewritten) === -1 ? "/" : rewritten + "/");
      }})();
    </script>
  </head>
  <body>
    <p>This page does not exist. Continue to the <a href="/">book</a>.</p>
  </body>
</html>
"""


def toc_files(toc_path: Path) -> list[str]:
    return [
        match.group(1)
        for line in toc_path.read_text(encoding="utf-8").splitlines()
        if (match := TOC_ENTRY.match(line))
    ]


def route_for(source: str) -> str:
    """The route Jupyter Book v2 serves the given table of contents entry at."""
    stem = SOURCE_SUFFIX.sub("", source)
    return "/" + "/".join(
        segment.replace("_", "-").lower() for segment in stem.split("/")
    )


def writable(path: Path) -> bool:
    """Whether the path is free, or holds nothing but an earlier run of this script."""
    return not path.exists() or MARKER in path.read_text(encoding="utf-8")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT)
    toc_path = Path(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TOC)
    if not root.is_dir():
        print(f"{root} does not exist, nothing to redirect to", file=sys.stderr)
        return 1
    if not toc_path.is_file():
        print(
            f"{toc_path} does not exist, cannot read the table of contents",
            file=sys.stderr,
        )
        return 1

    sources = toc_files(toc_path)
    if not sources:
        print(f"no 'file:' entries in {toc_path}", file=sys.stderr)
        return 1

    # The first entry is the front page, which v2 serves at the site root rather than under its own slug.
    routes = ["/"] + [route_for(source) for source in sources[1:]]

    missing = [
        route
        for route in routes
        if not (root / route.lstrip("/") / "index.html").is_file()
    ]
    if missing:
        print(
            f"the build has no page at {', '.join(missing)}; the v2 route layout changed, "
            f"so the redirects were not written",
            file=sys.stderr,
        )
        return 1

    written = 0
    for source, route in zip(sources, routes, strict=False):
        legacy = root / SOURCE_SUFFIX.sub(".html", source)
        # Rebuilding into a directory that already holds a previous run has to stay harmless, while a path the book itself now occupies has to stay untouched.
        if not writable(legacy):
            print(f"{legacy} is a real page, not overwriting it", file=sys.stderr)
            return 1
        target = route if route == "/" else route + "/"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        legacy.write_text(STUB.format(target=target, marker=MARKER), encoding="utf-8")
        written += 1

    not_found = root / "404.html"
    if not writable(not_found):
        print(f"{not_found} is a real page, not overwriting it", file=sys.stderr)
        return 1
    known = "[" + ", ".join(f'"{route}"' for route in routes if route != "/") + "]"
    not_found.write_text(
        NOT_FOUND.format(routes=known, marker=MARKER), encoding="utf-8"
    )

    print(f"{written} legacy URL(s) redirected, and a 404 page catches the rest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
