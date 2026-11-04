// Progressive enhancement only. The site is fully usable without JavaScript.
(function () {
  document.documentElement.classList.add("js");

  // Full-screen menu (tablet and mobile)
  var overlay = document.getElementById("overlay");
  var openBtn = document.querySelector(".site-header .menu-btn");
  var closeBtn = overlay && overlay.querySelector(".close");
  function setMenu(open) {
    if (!overlay) return;
    overlay.classList.toggle("open", open);
    if (open) overlay.scrollTop = 0;
    overlay.setAttribute("aria-hidden", open ? "false" : "true");
    if (openBtn) openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("locked", open);
  }
  if (openBtn) openBtn.addEventListener("click", function () { setMenu(true); });
  if (closeBtn) closeBtn.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });

  // Header rule and mobile booking bar once scrolled
  var header = document.querySelector(".site-header");
  var mbar = document.querySelector(".mbar");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (mbar) mbar.classList.toggle("show", y > 480);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Video: load YouTube (privacy-enhanced mode) only when asked
  document.querySelectorAll(".video[data-yt]").forEach(function (v) {
    var btn = v.querySelector(".play");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + v.getAttribute("data-yt") + "?autoplay=1&rel=0";
      f.title = btn.getAttribute("aria-label") || "Video";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      v.innerHTML = "";
      v.appendChild(f);
    });
  });

  // Enquiry form: compose an email to the private secretary
  var form = document.getElementById("enquiry");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var lines = ["Name: " + d.get("name"), "Telephone: " + d.get("phone"), "Email: " + (d.get("email") || "not given"),
        "Clinic: " + d.get("clinic"), "Reason: " + d.get("reason"), "Funding: " + d.get("funding"), "", d.get("message") || ""];
      window.location.href = "mailto:" + form.getAttribute("data-to") +
        "?subject=" + encodeURIComponent("Appointment enquiry: " + d.get("reason")) +
        "&body=" + encodeURIComponent(lines.join("\n"));
    });
  }


  // Hero reel: pause / play control
  document.querySelectorAll(".vhero .rp").forEach(function (b) {
    var v = b.parentNode.querySelector("video");
    if (!v) return;
    b.addEventListener("click", function () {
      if (v.paused) { v.play(); b.textContent = "Pause"; b.setAttribute("aria-label", "Pause video"); }
      else { v.pause(); b.textContent = "Play"; b.setAttribute("aria-label", "Play video"); }
    });
  });

  // Podcast lightbox: the YouTube player loads only when opened
  var lb = document.getElementById("lb");
  if (lb) {
    var fr = document.getElementById("lbfr");
    var heroV = document.querySelector(".vhero video");
    var openPod = function () {
      fr.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + fr.getAttribute("data-yt") + '?autoplay=1&rel=0" title="Podcast episode" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      lb.classList.add("on"); document.body.classList.add("locked");
      if (heroV) heroV.pause();
      var x = lb.querySelector(".x"); if (x) x.focus();
    };
    var closePod = function () {
      lb.classList.remove("on"); document.body.classList.remove("locked"); fr.innerHTML = "";
      if (heroV && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) heroV.play();
    };
    document.querySelectorAll("[data-open-pod]").forEach(function (b) { b.addEventListener("click", openPod); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.closest(".x")) closePod(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && lb.classList.contains("on")) closePod(); });
  }

  // Blog: filter articles by topic
  var bf = document.querySelector(".bfilter");
  if (bf) {
    bf.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      bf.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
      var c = b.getAttribute("data-cat");
      document.querySelectorAll(".journal li[data-cat]").forEach(function (li) { li.hidden = !!c && li.getAttribute("data-cat") !== c; });
    });
  }

  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Looping clips: load and play only while on screen
  var clips = document.querySelectorAll("video[data-lazy]");
  if ("IntersectionObserver" in window && !still && clips.length) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) {
          if (!v.dataset.loaded) { v.querySelectorAll("source").forEach(function (s) { s.src = s.dataset.src; }); v.load(); v.dataset.loaded = "1"; }
          var pr = v.play(); if (pr && pr.catch) pr.catch(function () {});
        } else if (v.dataset.loaded) { v.pause(); }
      });
    }, { rootMargin: "200px 0px" });
    clips.forEach(function (v) { vio.observe(v); });
  }

  // Timeline: pin and move sideways while scrolling (larger screens)
  var hz = document.querySelector("[data-hz]");
  var hzTrack = hz && hz.querySelector("[data-hztrack]");
  var hzBar = hz && hz.querySelector("[data-hzbar]");
  var hzWide = window.matchMedia("(min-width: 64rem)");
  var hzSize = function () {
    if (!hz) return;
    var on = hzWide.matches && !still;
    hz.classList.toggle("pin", on);
    if (on) { var extra = hzTrack.scrollWidth - window.innerWidth; hz.style.setProperty("--hzh", (window.innerHeight + Math.max(0, extra)) + "px"); hz.dataset.extra = Math.max(0, extra); }
  };
  var hzMove = function () {
    if (!hz) return;
    var r = hz.getBoundingClientRect(), span = r.height - window.innerHeight;
    var p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
    if (hz.classList.contains("pin")) hz.style.setProperty("--hzx", (p * (+hz.dataset.extra || 0)).toFixed(1));
    else p = hzTrack.scrollLeft / Math.max(1, hzTrack.scrollWidth - hzTrack.clientWidth);
    if (hzBar) hzBar.parentNode.style.setProperty("--hzp", p.toFixed(3));
  };
  if (hz) {
    hzSize(); hzMove();
    window.addEventListener("resize", function () { hzSize(); hzMove(); });
    window.addEventListener("scroll", function () { requestAnimationFrame(hzMove); }, { passive: true });
    hzTrack.addEventListener("scroll", hzMove, { passive: true });
    window.addEventListener("load", function () { hzSize(); hzMove(); });
  }

  // Scroll reveal for sections and cards
  var reveals = document.querySelectorAll("[data-r], .fade, .h-anim");
  if ("IntersectionObserver" in window && !still) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Scroll-linked effects: the hero eases back, the statement lights up word by word
  var hero = document.querySelector("[data-hero]");
  var say = document.querySelector("[data-say]");
  var words = say ? say.querySelectorAll(".w") : [];
  var pars = document.querySelectorAll("[data-par]");
  var jn = document.querySelector(".jn");
  var chs = jn ? jn.querySelectorAll(".ch") : [];
  var yearEl = document.querySelector("[data-year]");
  var bar = document.querySelector("[data-progress]");
  if (jn && chs.length) {
    chs[0].classList.add("on");
    var shown = chs[0].getAttribute("data-y");
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        chs.forEach(function (c) { c.classList.toggle("on", c === en.target); });
        var y = en.target.getAttribute("data-y");
        if (yearEl && y !== shown) {
          shown = y; yearEl.classList.add("swap");
          setTimeout(function () { yearEl.textContent = y; yearEl.classList.remove("swap"); }, 220);
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    chs.forEach(function (c) { cio.observe(c); });
  }
  if (!still && (hero || say || pars.length || bar)) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var vh = window.innerHeight;
      if (hero) hero.style.setProperty("--hp", Math.min(1, Math.max(0, window.scrollY / vh)).toFixed(3));
      pars.forEach(function (el) {
        var b = el.parentNode.getBoundingClientRect();
        el.style.setProperty("--py", Math.min(1, Math.max(0, (vh - b.top) / (vh + b.height))).toFixed(3));
      });
      if (bar) {
        var jr = jn.getBoundingClientRect();
        bar.style.setProperty("--jp", Math.min(1, Math.max(0, (vh * 0.5 - jr.top) / jr.height)).toFixed(3));
        bar.parentNode.style.setProperty("--jp", bar.style.getPropertyValue("--jp"));
      }
      if (say) {
        var r = say.getBoundingClientRect();
        var p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
        var lit = p * words.length;
        for (var i = 0; i < words.length; i++) words[i].style.setProperty("--on", Math.min(1, Math.max(0, lit - i)).toFixed(2));
      }
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }
})();
