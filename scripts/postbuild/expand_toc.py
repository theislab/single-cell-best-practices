"""Open every section of the sidebar table of contents, not just the current one.

The theme has no option for this, and the sections are Radix collapsibles that do not render their children while closed, so CSS cannot reveal them either.
"""

from client_bundle import patch_client_entry

MARKER = "myst-expand-toc"

SNIPPET = f"""
/* {MARKER} */
;(function () {{
  if (typeof window === "undefined" || window.__mystExpandToc) return;
  window.__mystExpandToc = true;

  var COLLAPSED = '.myst-toc button[aria-label="Open Folder"][aria-expanded="false"]';
  var ACTIVE = '.myst-toc [aria-current="page"]';
  var SCROLLER = ".myst-primary-sidebar-nav";
  var WINDOW_MS = 2000;
  var QUIET_FRAMES = 10;

  var deadline = 0;
  var running = false;

  /* Retried rather than done once: React mounts the sidebar after this runs, and the theme collapses the other sections again on every navigation.
     Outside the window a reader can collapse a section and have it stay collapsed. */
  function expand() {{
    deadline = Date.now() + WINDOW_MS;
    if (running) return;
    running = true;
    var opened = false;
    var quiet = 0;

    (function pass() {{
      var collapsed = document.querySelectorAll(COLLAPSED);
      collapsed.forEach(function (button) {{
        button.click();
      }});
      opened = opened || collapsed.length > 0;
      quiet = collapsed.length > 0 ? 0 : quiet + 1;
      if (Date.now() < deadline && !(opened && quiet > QUIET_FRAMES)) {{
        window.requestAnimationFrame(pass);
        return;
      }}
      running = false;
      reveal();
    }})();
  }}

  /* The expanded tree is taller than the sidebar, so scroll it, and only it, to the chapter being read. */
  function reveal() {{
    var active = document.querySelector(ACTIVE);
    var scroller = active && active.closest(SCROLLER);
    if (!scroller) return;
    var entry = active.getBoundingClientRect();
    var view = scroller.getBoundingClientRect();
    if (entry.top >= view.top && entry.bottom <= view.bottom) return;
    scroller.scrollTop += entry.top - view.top - view.height / 3;
  }}

  ["pushState", "replaceState"].forEach(function (name) {{
    var original = window.history[name];
    if (typeof original !== "function") return;
    window.history[name] = function () {{
      var result = original.apply(this, arguments);
      expand();
      return result;
    }};
  }});
  window.addEventListener("popstate", expand);

  expand();
}})();
"""


if __name__ == "__main__":
    raise SystemExit(patch_client_entry(MARKER, SNIPPET, "expanded table of contents"))
