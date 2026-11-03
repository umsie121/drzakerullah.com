"""Shared layout, components and helpers for the static site generator.

All hrefs/srcs in page content are written with a leading "~/" meaning
"site root"; render() rewrites them to the correct relative prefix so the
site works from any folder (custom domain or GitHub Pages sub-path).
"""
import json
import os
import re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.drzakerullah.com"
TODAY = "2026-11-03"
SITEMAP = []

NAME = "Mr Md Zaker Ullah"
SHORT = "Mr Zaker Ullah"
POSTNOM = "MBBS FRCSEd FRCS (Gen. Surg.)"

# ---------------------------------------------------------------- icons
ARROW = '<svg class="arr" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
GO = '<span class="go" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 8h11M9 4l4 4-4 4"/></svg></span>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 3.5l3 3 3-3"/></svg>'
STAR = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6L10 15l-5.4 3 1.2-6L1.3 7.8l6.1-.7z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l12-7.5z"/></svg>'
MARK = ('<svg class="mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="none" stroke="#b18c55" stroke-width="1"/>'
        '<circle cx="24" cy="24" r="19.5" fill="#0b1b20"/>'
        '<text x="24" y="30.5" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="17" font-style="italic" fill="#f6f2ea" letter-spacing="-0.5">zu</text></svg>')


def stars(n=5, label=None):
    lab = label or f"{n} out of 5 stars"
    return f'<span class="stars" role="img" aria-label="{lab}">' + STAR * n + "</span>"


def picture(base, alt, sizes, widths, ratio_w, ratio_h, lazy=True, cls=""):
    """<picture> with WebP + JPEG fallbacks from assets/img/{base}-{w}.{ext}."""
    webp = ", ".join(f"~/assets/img/{base}-{w}.webp {w}w" for w in widths)
    jpg = ", ".join(f"~/assets/img/{base}-{w}.jpg {w}w" for w in widths)
    mid = widths[len(widths) // 2]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="~/assets/img/{base}-{mid}.jpg" srcset="{jpg}" sizes="{sizes}" alt="{escape(alt)}" width="{ratio_w}" height="{ratio_h}" {load}></picture>')


def faq_html(faqs):
    items = "".join(
        f'<details><summary>{escape(q)}</summary><div class="a">{"".join("<p>" + p + "</p>" for p in a.split("||"))}</div></details>'
        for q, a in faqs)
    return f'<div class="faq">{items}</div>'


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&rsquo;", "’").replace("&amp;", "&").replace("&mdash;", "—").replace("&nbsp;", " ")


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a.replace("||", " "))}} for q, a in faqs]}


def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + p}
                                for i, (n, p) in enumerate(crumbs)]}


def crumbs_html(crumbs):
    lis = []
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            lis.append(f'<li aria-current="page">{escape(n)}</li>')
        else:
            lis.append(f'<li><a href="~/{p}">{escape(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


PHYSICIAN_REF = {"@id": SITE + "/#physician"}


# ---------------------------------------------------------------- chrome
def header(nav, active):
    proc_links = "".join(
        f'<a href="~/procedures/{p["slug"]}/"><strong>{p["nav"]}</strong><span>{p["navdesc"]}</span></a>'
        for p in nav["procedures"])
    loc_links = "".join(
        f'<a href="~/locations/{l["slug"]}/"><strong>{l["name"]}</strong><span>{l["area"]}</span></a>'
        for l in nav["locations"])

    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return f'''<div class="topbar"><div class="wrap">
  <span class="tb-left"><span class="dot" aria-hidden="true"></span>Prompt private appointments for new breast symptoms</span>
  <span class="tb-right"><span class="tb-hide">Fee-assured with all major UK insurers</span><a href="tel:{nav["phone_tel"]}">{nav["phone_label"]}</a></span>
</div></div>
<header class="site-header">
  <div class="wrap bar">
    <a class="wordmark" href="~/" aria-label="{SHORT}, Consultant Breast Surgeon, home">{MARK}<span><span class="name">{SHORT}</span><span class="role">Consultant Breast Surgeon</span></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span></span><span></span></button>
    <nav class="site-nav" id="nav" aria-label="Main">
      <div class="nav-drop"><button type="button" aria-haspopup="true"{cur("procedures")}>Treatments {CHEV}</button>
        <div class="mega">{proc_links}<div class="mega-foot"><span>Not sure where to start?</span><a class="link-arrow" href="~/procedures/">All treatments {ARROW}</a></div></div></div>
      <div class="nav-drop"><button type="button" aria-haspopup="true"{cur("locations")}>Locations {CHEV}</button>
        <div class="mega locs">{loc_links}<div class="mega-foot"><span>London &amp; Essex</span><a class="link-arrow" href="~/locations/">All clinics {ARROW}</a></div></div></div>
      <a href="~/biography/"{cur("about")}>About</a>
      <a href="~/reviews/"{cur("reviews")}>Reviews</a>
      <a href="~/podcast/"{cur("podcast")}>Podcast</a>
      <a href="~/news/"{cur("news")}>Insights</a>
      <a class="btn sm" href="~/booking/">Book a consultation</a>
    </nav>
  </div>
</header>'''


def footer(nav):
    procs = "".join(f'<li><a href="~/procedures/{p["slug"]}/">{p["nav"]}</a></li>' for p in nav["procedures"])
    locs = "".join(f'<li><a href="~/locations/{l["slug"]}/">{l["name"]}</a></li>' for l in nav["locations"])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="f-top">
      <div>
        <a class="wordmark" href="~/">{MARK}<span><span class="name">{SHORT}</span><span class="role">{POSTNOM}</span></span></a>
        <p class="f-blurb">Consultant Oncoplastic Breast &amp; General Surgeon. Clinical Lead, Whipps Cross Breast Unit, Barts Health NHS Trust. GMC registration no.&nbsp;4368515.</p>
        <div class="f-social"><a href="{nav["iwgc"]}" rel="noopener" target="_blank">iWantGreatCare</a><a href="~/podcast/">Podcast</a><a href="https://www.gmc-uk.org/registrants/4368515" rel="noopener" target="_blank">GMC register</a></div>
      </div>
      <div><h4>Treatments</h4><ul>{procs}<li><a href="~/second-opinion/">Second opinions</a></li></ul></div>
      <div><h4>Clinics</h4><ul>{locs}<li><a href="~/booking/">Appointments</a></li></ul></div>
      <div><h4>Practice</h4><ul><li><a href="~/biography/">About Mr Ullah</a></li><li><a href="~/reviews/">Patient reviews</a></li><li><a href="~/podcast/">Podcast</a></li><li><a href="~/news/">Insights</a></li><li><a href="~/booking/">Book a consultation</a></li></ul></div>
    </div>
    <div class="f-legal"><span>&copy; 2026 {NAME}. All rights reserved.</span><span>Information on this site is general and does not replace a consultation. In an emergency call 999.</span></div>
  </div>
</footer>
<div class="mbar" aria-label="Quick contact"><a href="tel:{nav["phone_tel"]}">Call</a><a class="primary" href="~/booking/">Book a consultation</a></div>'''


def cta_band(title="Arrange a <em>consultation</em>", text=None, nav=None):
    text = text or "Private appointments on Harley Street, in the City of London and at The Holly in Buckhurst Hill, with priority for new breast symptoms. Insured and self-funding patients welcome."
    phones = f'<span>Private secretary: <a href="tel:{nav["phone_tel"]}">{nav["phone_label"].split(": ")[-1]}</a></span>' + "".join(f'<span>{l["short"]}: <a href="tel:{l["tel"]}">{l["phone"]}</a></span>' for l in nav["locations"] if l.get("phone"))
    return f'''<div class="cta-wrap"><div class="wrap"><div class="cta reveal">
  <div><p class="eyebrow">Appointments</p><h2>{title}</h2><p>{text}</p></div>
  <div class="cta-side"><a class="btn gold" href="~/booking/">Book a consultation {ARROW}</a><a class="btn ghost on-dark" href="~/locations/">Choose a clinic</a><div class="cta-phones">{phones}</div></div>
</div></div></div>'''


def render(path, *, title, desc, body, nav, active=None, schema=(), og_type="website",
           image="assets/img/og-card.png", priority="0.7", noindex=False, extra_head=""):
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    rel = "../" * depth if depth else "./"
    if path == "404.html":
        rel = "/"  # served from arbitrary URLs, so links must be absolute
    canonical = SITE + "/" + path
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b1b20">
<meta name="geo.region" content="GB-LND">
<meta property="og:site_name" content="{NAME} — Consultant Breast Surgeon">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="~/assets/img/favicon.svg">
<link rel="apple-touch-icon" href="~/assets/img/holly-head-600.jpg">
<link rel="preload" href="~/assets/fonts/fraunces-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="~/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="~/assets/css/main.css">
{extra_head}{blocks}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header(nav, active)}
<main id="main">
{body}
</main>
{cta_band(nav=nav) if path not in ("booking/",) and not noindex else ""}
{footer(nav)}
<script src="~/assets/js/main.js" defer></script>
</body>
</html>
'''
    html = html.replace('"~/', '"' + rel).replace(" ~/", " " + rel)
    out = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    if path == "404.html":
        out = os.path.join(ROOT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    if not noindex:
        SITEMAP.append((canonical, priority))
