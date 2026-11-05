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

  // Hero reel: make sure it plays (Safari can refuse autoplay, e.g. in Low Power Mode, until the first interaction)
  var reel = document.querySelector(".vhero video");
  // Phones get the portrait cut of the reel (via <source media>); match its poster too
  if (reel && reel.dataset.posterPhone && window.matchMedia("(max-width: 47.99rem)").matches) reel.poster = reel.dataset.posterPhone;
  if (reel && !still) {
    reel.muted = true; reel.defaultMuted = true; reel.setAttribute("playsinline", "");
    var go = function () { var p = reel.play(); if (p && p.catch) p.catch(function () {}); };
    go();
    reel.addEventListener("canplay", go, { once: true });
    ["touchstart", "scroll", "pointerdown", "keydown"].forEach(function (ev) { window.addEventListener(ev, function () { if (reel.paused) go(); }, { once: true, passive: true }); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden && reel.paused) go(); });
  }

  // Homepage reviews: arrow buttons scroll the row by one card
  var rvs = document.querySelector(".rv-scroll");
  if (rvs) document.querySelectorAll("[data-rv]").forEach(function (b) {
    b.addEventListener("click", function () { var c = rvs.querySelector(".rc"); rvs.scrollBy({ left: (+b.dataset.rv) * ((c ? c.offsetWidth : 320) + 16), behavior: still ? "auto" : "smooth" }); });
  });

  // Clinic pages open in an overlay sheet (the full pages remain for search and direct links)
  (function () {
    var sheet, body, lastFocus;
    var isClinic = function (a) {
      var u; try { u = new URL(a.href, location.href); } catch (e) { return false; }
      return u.origin === location.origin && /\/locations\/[^/]+\/$/.test(u.pathname) && u.pathname !== location.pathname && !/harley-street/.test(u.pathname);
    };
    var close = function () {
      if (!sheet) return;
      sheet.classList.remove("on"); document.body.classList.remove("locked");
      if (lastFocus) lastFocus.focus();
    };
    var build = function () {
      sheet = document.createElement("div");
      sheet.className = "sheet"; sheet.setAttribute("role", "dialog"); sheet.setAttribute("aria-modal", "true"); sheet.setAttribute("aria-label", "Clinic");
      sheet.innerHTML = '<div class="sheet-bg"></div><div class="sheet-p"><button type="button" class="sheet-x" aria-label="Close">&times;</button><div class="sheet-b"></div></div>';
      document.body.appendChild(sheet);
      body = sheet.querySelector(".sheet-b");
      sheet.querySelector(".sheet-x").addEventListener("click", close);
      sheet.querySelector(".sheet-bg").addEventListener("click", close);
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    };
    var open = function (href) {
      if (!sheet) build();
      lastFocus = document.activeElement;
      body.innerHTML = '<p class="sheet-load">Loading</p>';
      sheet.classList.add("on"); document.body.classList.add("locked");
      sheet.querySelector(".sheet-x").focus();
      fetch(href).then(function (r) { return r.text(); }).then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        var main = doc.querySelector("main"); if (!main) { location.href = href; return; }
        main.querySelectorAll(".appt-band, .crumbs, script").forEach(function (n) { n.remove(); });
        main.querySelectorAll("[href], [src], [srcset], [poster]").forEach(function (n) {
          ["href", "src", "poster"].forEach(function (k) { var v = n.getAttribute(k); if (v && !/^(https?:|mailto:|tel:|#)/.test(v)) n.setAttribute(k, new URL(v, href).href); });
          var ss = n.getAttribute("srcset");
          if (ss) n.setAttribute("srcset", ss.split(",").map(function (p) { var b = p.trim().split(/\s+/); b[0] = new URL(b[0], href).href; return b.join(" "); }).join(", "));
        });
        main.querySelectorAll("[data-r]").forEach(function (n) { n.classList.add("in"); });
        body.innerHTML = main.innerHTML + '<p class="sheet-full"><a class="more" href="' + href + '">Open the full clinic page</a></p>';
        body.scrollTop = 0;
      }).catch(function () { location.href = href; });
    };
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank" || !isClinic(a)) return;
      if (a.closest(".sheet")) return;
      e.preventDefault();
      if (typeof setMenu === "function") setMenu(false);
      open(a.href);
    });
  })();

  // Offer the Bangla or Arabic page to visitors whose device is set to that language (never redirect)
  (function () {
    if (document.documentElement.lang.indexOf("en") !== 0) return;
    var pref = (navigator.languages || [navigator.language || ""]).map(function (l) { return (l || "").slice(0, 2).toLowerCase(); });
    var want = pref[0] === "ar" ? "ar" : pref[0] === "bn" ? "bn" : null;
    try { if (!want || localStorage.getItem("langhint") === "no") return; } catch (e) { if (!want) return; }
    var copy = { ar: ["هذه الصفحة متوفرة بالعربية", "العربية"], bn: ["এই পেজটি বাংলায়ও আছে", "বাংলা"] }[want];
    var root = document.querySelector('link[rel="icon"]').getAttribute("href").split("assets/")[0];
    var d = document.createElement("div");
    d.className = "langhint"; d.setAttribute("lang", want); d.setAttribute("dir", want === "ar" ? "rtl" : "ltr");
    d.innerHTML = '<span>' + copy[0] + '</span><a href="' + root + want + '/">' + copy[1] + '</a><button type="button" aria-label="Close">&times;</button>';
    d.querySelector("button").addEventListener("click", function () { d.remove(); try { localStorage.setItem("langhint", "no"); } catch (e) {} });
    document.body.appendChild(d);
  })();

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
