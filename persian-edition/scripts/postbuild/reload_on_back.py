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

Remove this once the theme handles POP navigation.
"""

from client_bundle import patch_client_entry

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


if __name__ == "__main__":
    patch_client_entry(MARKER, SNIPPET, "back button workaround")
