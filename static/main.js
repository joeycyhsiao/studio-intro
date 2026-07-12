/* In-Clues deck — replaces the old x-dc runtime.
   Vertical-nav scroll-spy, floating CTA, and the testimonial carousel. */
(function () {
  "use strict";

  // ---- vertical nav scroll-spy ----
  function spy() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".vnav a"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    var byId = {};
    links.forEach(function (a) { byId[(a.getAttribute("href") || "").slice(1)] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove("is-active"); });
        var a = byId[e.target.id];
        if (a) a.classList.add("is-active");
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    document.querySelectorAll("section[id]").forEach(function (s) { obs.observe(s); });
  }

  // ---- floating "book a call" button ----
  function fab() {
    var el = document.getElementById("fab");
    if (!el) return;
    function onScroll() {
      var contact = document.getElementById("contact");
      var past = window.scrollY > window.innerHeight * 0.8;
      var near = contact ? contact.getBoundingClientRect().top < window.innerHeight * 0.9 : false;
      if (past && !near) el.classList.add("show"); else el.classList.remove("show");
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- testimonial carousel (clone-based infinite loop) ----
  function carousel() {
    var track = document.querySelector("[data-voices-track]");
    if (!track) return;
    var real = Array.prototype.slice.call(track.querySelectorAll("figure"));
    if (real.length < 2) return;

    var cloneLast = real[real.length - 1].cloneNode(true);
    var cloneFirst = real[0].cloneNode(true);
    cloneLast.setAttribute("aria-hidden", "true");
    cloneFirst.setAttribute("aria-hidden", "true");
    track.insertBefore(cloneLast, real[0]);
    track.appendChild(cloneFirst);

    var count = real.length;   // number of real cards
    var target = 1;            // 1..count (index into full list incl. clones)
    var timer = null;

    function cards() { return Array.prototype.slice.call(track.querySelectorAll("figure")); }
    function center(card) {
      return card.offsetLeft - (track.clientWidth - card.getBoundingClientRect().width) / 2;
    }
    function nearestIndex() {
      var cs = cards(), best = 0, bd = Infinity;
      cs.forEach(function (c, i) {
        var d = Math.abs(center(c) - track.scrollLeft);
        if (d < bd) { bd = d; best = i; }
      });
      return best;
    }
    function syncGeom() {
      var cw = track.clientWidth;
      if (!cw) return;
      var w = Math.min(520, Math.round(cw * 0.62));
      var pad = Math.round((cw - w) / 2);
      cards().forEach(function (c) { c.style.flex = "0 0 " + w + "px"; });
      track.style.paddingLeft = pad + "px";
      track.style.paddingRight = pad + "px";
    }

    // dots
    var dotsWrap = document.querySelector("[data-voices-dots]");
    var dots = [];
    if (dotsWrap) {
      dotsWrap.innerHTML = "";
      for (var i = 1; i <= count; i++) {
        (function (n) {
          var b = document.createElement("button");
          b.type = "button";
          b.setAttribute("aria-label", "第 " + n + " 則推薦");
          b.style.cssText = "width:10px;height:10px;border-radius:50%;border:none;padding:0;cursor:pointer;background:#D8D6E4;transition:background 0.2s;";
          b.addEventListener("click", function () { goTo(n); });
          dotsWrap.appendChild(b);
          dots.push(b);
        })(i);
      }
    }
    function setActive(t) {
      target = t;
      dots.forEach(function (b, k) { b.style.background = (k + 1 === t) ? "#5F5B8C" : "#D8D6E4"; });
    }
    function goTo(n) {
      var cs = cards();
      if (!cs[n]) return;
      syncGeom();
      track.scrollTo({ left: center(cs[n]), behavior: "smooth" });
      setActive(n);
    }
    function step(dir) {
      var cs = cards();
      if (cs.length < 3) return;
      syncGeom();
      var next = target + dir;
      if (next > count) {
        track.scrollLeft = center(cs[0]);
        next = 1;
        requestAnimationFrame(function () { track.scrollTo({ left: center(cs[1]), behavior: "smooth" }); });
      } else if (next < 1) {
        track.scrollLeft = center(cs[count + 1]);
        next = count;
        requestAnimationFrame(function () { track.scrollTo({ left: center(cs[count]), behavior: "smooth" }); });
      } else {
        track.scrollTo({ left: center(cs[next]), behavior: "smooth" });
      }
      setActive(next);
    }
    function normalize() {
      var cs = cards();
      if (cs.length < 3) return;
      var i = nearestIndex();
      if (i <= 0) { track.scrollLeft = center(cs[count]); setActive(count); }
      else if (i >= count + 1) { track.scrollLeft = center(cs[1]); setActive(1); }
      else { setActive(i); }
    }

    var prev = document.querySelector("[data-voices-prev]");
    var next = document.querySelector("[data-voices-next]");
    if (prev) prev.addEventListener("click", function () { step(-1); });
    if (next) next.addEventListener("click", function () { step(1); });
    track.addEventListener("scroll", function () {
      clearTimeout(timer);
      timer = setTimeout(normalize, 150);
    }, { passive: true });

    function init() {
      syncGeom();
      var cs = cards();
      if (cs[target]) track.scrollLeft = center(cs[target]);
    }
    init();
    setTimeout(init, 400);
    setTimeout(init, 1200);
    window.addEventListener("resize", init);
    setActive(1);
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () { spy(); fab(); carousel(); });
})();
