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

  // Gentle fade for statement blocks below the fold
  var fades = document.querySelectorAll(".fade");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    fades.forEach(function (el) { io.observe(el); });
  } else {
    fades.forEach(function (el) { el.classList.add("in"); });
  }
})();
