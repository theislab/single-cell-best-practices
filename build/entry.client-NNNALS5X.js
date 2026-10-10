import{o as r}from"/build/_shared/chunk-UBXX7P26.js";import{a,c as l,d as i}from"/build/_shared/chunk-KB7LMXDF.js";import{e as o}from"/build/_shared/chunk-RAQ24GF6.js";var t=o(a()),m=o(l()),e=o(i());function d(){(0,t.startTransition)(()=>{(0,m.hydrateRoot)(document,(0,e.jsx)(t.StrictMode,{children:(0,e.jsx)(r,{})}))})}window.requestIdleCallback?window.requestIdleCallback(d):window.setTimeout(d,1);

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
