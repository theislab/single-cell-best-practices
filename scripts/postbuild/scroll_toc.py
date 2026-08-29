"""Scroll the sidebar to the chapter being read.

Every section of the table of contents is open (see scripts/prebuild/expand_toc.py), so the tree is taller than the sidebar and a chapter far down the book starts out below its fold.
"""

from client_bundle import patch_client_entry

MARKER = "myst-scroll-toc"

SNIPPET = f"""
/* {MARKER} */
;(function () {{
  if (typeof window === "undefined" || window.__mystScrollToc) return;
  window.__mystScrollToc = true;

  var ACTIVE = '.myst-toc [aria-current="page"]';
  var SCROLLER = ".myst-primary-sidebar-nav";
  var WINDOW_MS = 2000;

  var deadline = Date.now() + WINDOW_MS;
  var reading = false;

  /* The reader wins: once they touch the page the sidebar is theirs. */
  ["wheel", "touchstart", "pointerdown", "keydown"].forEach(function (name) {{
    window.addEventListener(name, function () {{
      reading = true;
    }}, {{ once: true, passive: true }});
  }});

  /* Kept up for a moment rather than done once: the sidebar cannot be scrolled while the theme still has it hidden, and the theme sizes it a few times after that, which puts the tree back at the top. */
  (function align() {{
    var active = document.querySelector(ACTIVE);
    var scroller = active && active.closest(SCROLLER);
    if (scroller && scroller.scrollHeight > scroller.clientHeight) {{
      var entry = active.getBoundingClientRect();
      var view = scroller.getBoundingClientRect();
      if (entry.top < view.top || entry.bottom > view.bottom) {{
        scroller.scrollTop += entry.top - view.top - view.height / 3;
      }}
    }}
    if (!reading && Date.now() < deadline) window.requestAnimationFrame(align);
  }})();
}})();
"""


if __name__ == "__main__":
    patch_client_entry(
        MARKER, SNIPPET, "table of contents scrolled to the current chapter"
    )
