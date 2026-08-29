import{o as r}from"/build/_shared/chunk-AQ2CODAG.js";import{a,c as l,d as i}from"/build/_shared/chunk-JJXTQVMA.js";import{f as o}from"/build/_shared/chunk-OZE3FFNP.js";var t=o(a()),m=o(l()),e=o(i());function d(){(0,t.startTransition)(()=>{(0,m.hydrateRoot)(document,(0,e.jsx)(t.StrictMode,{children:(0,e.jsx)(r,{})}))})}window.requestIdleCallback?window.requestIdleCallback(d):window.setTimeout(d,1);

/* myst-reload-on-back-workaround */
;(function () {
  if (typeof window === "undefined" || window.__mystReloadOnBack) return;
  window.__mystReloadOnBack = true;

  /* Which page the current history entry belongs to. A key takeaway link only adds a
     fragment, so a back navigation away from one stays on the same page, and that is the
     POP the theme cannot render. Chapter to chapter back and forward changes the path and
     is left as an in place transition. */
  var page = window.location.pathname;

  function remember() {
    page = window.location.pathname;
  }

  /* The router navigates with pushState, so follow it to keep `page` current. */
  ["pushState", "replaceState"].forEach(function (name) {
    var original = window.history[name];
    if (typeof original !== "function") return;
    window.history[name] = function () {
      var result = original.apply(this, arguments);
      remember();
      return result;
    };
  });

  window.addEventListener("popstate", function () {
    var leaving = page;
    remember();
    if (leaving !== window.location.pathname) return;
    /* The URL is already the one being navigated to when popstate fires, so a plain
       reload lands on the right page. */
    window.location.reload();
  });
})();

/* myst-expand-toc */
;(function () {
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
  function expand() {
    deadline = Date.now() + WINDOW_MS;
    if (running) return;
    running = true;
    var opened = false;
    var quiet = 0;

    (function pass() {
      var collapsed = document.querySelectorAll(COLLAPSED);
      collapsed.forEach(function (button) {
        button.click();
      });
      opened = opened || collapsed.length > 0;
      quiet = collapsed.length > 0 ? 0 : quiet + 1;
      if (Date.now() < deadline && !(opened && quiet > QUIET_FRAMES)) {
        window.requestAnimationFrame(pass);
        return;
      }
      running = false;
      reveal();
    })();
  }

  /* The expanded tree is taller than the sidebar, so scroll it, and only it, to the chapter being read. */
  function reveal() {
    var active = document.querySelector(ACTIVE);
    var scroller = active && active.closest(SCROLLER);
    if (!scroller) return;
    var entry = active.getBoundingClientRect();
    var view = scroller.getBoundingClientRect();
    if (entry.top >= view.top && entry.bottom <= view.bottom) return;
    scroller.scrollTop += entry.top - view.top - view.height / 3;
  }

  ["pushState", "replaceState"].forEach(function (name) {
    var original = window.history[name];
    if (typeof original !== "function") return;
    window.history[name] = function () {
      var result = original.apply(this, arguments);
      expand();
      return result;
    };
  });
  window.addEventListener("popstate", expand);

  expand();
})();
