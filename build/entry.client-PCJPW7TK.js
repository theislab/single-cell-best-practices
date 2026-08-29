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

/* myst-scroll-toc */
;(function () {
  if (typeof window === "undefined" || window.__mystScrollToc) return;
  window.__mystScrollToc = true;

  var ACTIVE = '.myst-toc [aria-current="page"]';
  var SCROLLER = ".myst-primary-sidebar-nav";
  var WINDOW_MS = 2000;

  var deadline = Date.now() + WINDOW_MS;
  var reading = false;

  /* The reader wins: once they touch the page the sidebar is theirs. */
  ["wheel", "touchstart", "pointerdown", "keydown"].forEach(function (name) {
    window.addEventListener(name, function () {
      reading = true;
    }, { once: true, passive: true });
  });

  /* Kept up for a moment rather than done once: the sidebar cannot be scrolled while the theme still has it hidden, and the theme sizes it a few times after that, which puts the tree back at the top. */
  (function align() {
    var active = document.querySelector(ACTIVE);
    var scroller = active && active.closest(SCROLLER);
    if (scroller && scroller.scrollHeight > scroller.clientHeight) {
      var entry = active.getBoundingClientRect();
      var view = scroller.getBoundingClientRect();
      if (entry.top < view.top || entry.bottom > view.bottom) {
        scroller.scrollTop += entry.top - view.top - view.height / 3;
      }
    }
    if (!reading && Date.now() < deadline) window.requestAnimationFrame(align);
  })();
})();
