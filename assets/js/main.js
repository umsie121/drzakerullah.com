// Progressive enhancement only — the site is fully usable without JS.
(function () {
  var doc = document.documentElement;

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      document.body.classList.toggle("nav-open", open);
    });
  }

  // Header shadow + mobile booking bar once scrolled
  var header = document.querySelector(".site-header");
  var mbar = document.querySelector(".mbar");
  var onScroll = function () {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 40);
    if (mbar) mbar.classList.toggle("show", y > 500);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Video facade: load YouTube (privacy-enhanced) only on click
  document.querySelectorAll(".video[data-yt]").forEach(function (v) {
    var btn = v.querySelector("button.play");
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

  // Enquiry form → pre-filled email to the private secretary
  var form = document.getElementById("enquiry");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var lines = ["Name: " + d.get("name"), "Phone: " + d.get("phone"), "Email: " + (d.get("email") || "-"),
        "Preferred clinic: " + d.get("clinic"), "Reason: " + d.get("reason"), "Funding: " + d.get("funding"), "", d.get("message") || ""];
      window.location.href = "mailto:" + form.getAttribute("data-to") +
        "?subject=" + encodeURIComponent("Appointment enquiry — " + d.get("reason")) +
        "&body=" + encodeURIComponent(lines.join("\n"));
    });
  }

  // Scroll reveal (motion-safe)
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var els = document.querySelectorAll(".card, .quote, .step, .loc, .post, .pillars > div, .reveal");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight * 0.92) {
        el.classList.add("reveal");
        io.observe(el);
      } else {
        el.classList.add("in");
      }
    });
  }
  doc.classList.add("js");
})();
