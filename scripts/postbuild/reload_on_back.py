"""Reload the page when the reader goes back from a key takeaway, instead of crashing.

The MyST book theme (mystmd 1.10.1) does not survive the client side history POP that
follows a key takeaway card: the router ends up without loader data for the entry it
lands on, and the page route's `meta` function then reads `data.page.frontmatter` on it.
The reader gets a full page
"Application Error: Cannot read properties of undefined (reading 'frontmatter')"
instead of the chapter.

Upstream issue: https://github.com/jupyter-book/mystmd/issues/1178

There is no configuration for this and no server to fix it in, since releases are
published to GitHub Pages, so the workaround is appended to the theme's client entry
bundle: a `popstate` listener that turns a back navigation within a single page into a
normal document load. A key takeaway link only adds a fragment, so going back from one
stays on the same page and is reloaded; chapter to chapter back and forward changes the
path and is left as an in place transition.

Keying this off the path rather than off a remembered click on a card matters: a flag set
when the card is clicked is cleared by whatever the reader clicks next, which is easy to
do between following a takeaway and pressing back.

The listener deliberately goes into the JavaScript bundle rather than into a `<script>`
tag in the HTML. Remix hydrates `<head>` and `<body>`, so an injected tag is DOM React
did not render, which breaks hydration on every page — a worse bug than the one being
worked around.

Remove this once the theme handles POP navigation.
"""

import re
import sys
from pathlib import Path

MARKER = "myst-reload-on-back-workaround"

SNIPPET = f"""
/* {MARKER} */
;(function () {{
  if (typeof window === "undefined" || window.__mystReloadOnBack) return;
  window.__mystReloadOnBack = true;

  /* Which page the current history entry belongs to. A key takeaway link only adds a
     fragment, so a back navigation away from one stays on the same page, and that is the
     POP the theme cannot render. Chapter to chapter back and forward changes the path and
     is left as an in place transition. */
  var page = window.location.pathname;

  function remember() {{
    page = window.location.pathname;
  }}

  /* The router navigates with pushState, so follow it to keep `page` current. */
  ["pushState", "replaceState"].forEach(function (name) {{
    var original = window.history[name];
    if (typeof original !== "function") return;
    window.history[name] = function () {{
      var result = original.apply(this, arguments);
      remember();
      return result;
    }};
  }});

  window.addEventListener("popstate", function () {{
    var leaving = page;
    remember();
    if (leaving !== window.location.pathname) return;
    /* The URL is already the one being navigated to when popstate fires, so a plain
       reload lands on the right page. */
    window.location.reload();
  }});
}})();
"""

ENTRY_GLOB = "entry.client-*.js"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "jupyter-book/_build/html")
    if not root.is_dir():
        print(f"{root} does not exist, nothing to patch", file=sys.stderr)
        return 1

    entries = sorted((root / "build").glob(ENTRY_GLOB))
    if not entries:
        print(
            f"no {ENTRY_GLOB} under {root / 'build'}; the theme's bundle layout changed, "
            "so the back button workaround was not applied",
            file=sys.stderr,
        )
        return 1

    # Every page imports the same client entry, so patching it covers the whole site.
    # Guard against the entry being referenced but not actually loaded by checking that
    # at least one page imports it.
    pages = [p for p in root.rglob("*.html") if "/build/" not in p.as_posix()]
    referenced = {
        m.group(1)
        for page in pages
        for m in re.finditer(
            r'/build/(entry\.client-[^"\')]+\.js)', page.read_text(encoding="utf-8")
        )
    }
    if not referenced:
        print("no page imports a client entry bundle", file=sys.stderr)
        return 1

    patched = 0
    for entry in entries:
        if entry.name not in referenced:
            continue
        text = entry.read_text(encoding="utf-8")
        if MARKER in text:
            continue
        entry.write_text(text + SNIPPET, encoding="utf-8")
        patched += 1

    missing = referenced - {e.name for e in entries}
    if missing:
        print(f"pages import missing entry bundles: {sorted(missing)}", file=sys.stderr)
        return 1

    print(
        f"back button workaround applied to {patched} client entry bundle(s), "
        f"covering {len(pages)} pages"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
