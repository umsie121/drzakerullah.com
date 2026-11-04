"""Shared layout, components and helpers for the static site generator.

All hrefs/srcs in page content are written with a leading "~/" meaning
"site root"; render() rewrites them to the correct relative prefix so the
site works from any folder (custom domain or GitHub Pages sub-path).

Naming: always "Mr" Ullah (UK surgical convention for FRCS). "Dr" appears
only in verbatim patient reviews and in schema alternateName for search.
"""
import hashlib
import json
import os
import re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://drzakerullah.com"
SITEMAP = []


def asset_v(rel):
    """Short content hash so browsers refetch CSS/JS when they change."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

NAME = "Mr Md Zaker Ullah"
SHORT = "Mr Zaker Ullah"
POSTNOM = "MBBS FRCSEd FRCS (Gen. Surg.)"
PHYSICIAN_REF = {"@id": SITE + "/#physician"}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..800,0..100,0..1;1,9..144,300..800,0..100,0..1&family=Figtree:wght@300..800&display=swap">')


def picture(base, alt, sizes, widths, w, h, lazy=True):
    """<picture> with WebP + JPEG sources from assets/img/{base}-{width}.{ext}."""
    webp = ", ".join(f"~/assets/img/{base}-{x}.webp {x}w" for x in widths)
    jpg = ", ".join(f"~/assets/img/{base}-{x}.jpg {x}w" for x in widths)
    mid = widths[len(widths) // 2]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="~/assets/img/{base}-{mid}.jpg" srcset="{jpg}" sizes="{sizes}" alt="{escape(alt)}" width="{w}" height="{h}" {load}></picture>')


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    for a, b in (("&rsquo;", "’"), ("&lsquo;", "‘"), ("&amp;", "&"), ("&nbsp;", " "), ("&ldquo;", "“"), ("&rdquo;", "”")):
        s = s.replace(a, b)
    return s


def faq_html(faqs):
    items = "".join(
        f'<details><summary>{escape(q)}</summary><div class="a">{"".join("<p>" + p + "</p>" for p in a.split("||"))}</div></details>'
        for q, a in faqs)
    return f'<div class="faq">{items}</div>'


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
        lis.append(f'<li aria-current="page">{escape(n)}</li>' if i == len(crumbs) - 1 else f'<li><a href="~/{p}">{escape(n)}</a></li>')
    return f'<ol class="crumbs" aria-label="Breadcrumb">{"".join(lis)}</ol>'


def brand(extra=""):
    return f'<a class="brand{extra}" href="~/" aria-label="{SHORT}, home"><span class="mk" aria-hidden="true">ZU</span><span><span class="n">{SHORT}</span><span class="r">Consultant Breast Surgeon</span></span></a>'


# ---------------------------------------------------------------- navigation model
def nav_model(nav):
    return [
        ("Treatments", "procedures", "~/procedures/", "From a first breast symptom to surgery and reconstruction, under one consultant.",
         [(p["nav"], f"~/procedures/{p['slug']}/", p["short_desc"]) for p in nav["procedures"]]),
        ("Clinics", "locations", "~/locations/", "Private appointments in central London, the City and on the Essex border.",
         [(l["name"], f"~/locations/{l['slug']}/", l["area"]) for l in nav["locations"]]),
        ("About", "about", "~/biography/", "His training, his patients' reviews, and his work on podcasts and television.",
         [("Biography", "~/biography/", "Training and career"), ("Patient reviews", "~/reviews/", f"Rated {nav['rating']}, {nav['count']}"),
          ("Podcast and videos", "~/podcast/", "Podcast, TV3 Bangla, YouTube"), ("Second opinions", "~/second-opinion/", "An independent view")]),
        ("Patients", "patients", "~/your-visit/", "Everything you need to know before your first appointment.",
         [("Your first visit", "~/your-visit/", "What happens on the day"), ("Fees and insurance", "~/fees-and-insurance/", "Insured and self-funding"),
          ("Video and international", "~/remote-consultations/", "Consultations from anywhere"), ("Questions answered", "~/faqs/", "Every common question"), ("Book a consultation", "~/booking/", "Online, by phone or email")]),
    ]


def header(nav, active):
    model = nav_model(nav)

    def drop(item):
        title, key, href, intro, links = item
        cur = ' aria-current="page"' if active == key else ""
        lis = "".join(f'<li><a href="{h}">{t}<span>{d}</span></a></li>' for t, h, d in links)
        if key == "procedures" and nav.get("groups"):
            lis = "".join(f'<li class="grp"><span class="gh">{g}</span>' + "".join(f'<a href="~/procedures/{p["slug"]}/">{p["nav"]}</a>' for p in ps) + "</li>" for g, ps in nav["groups"])
        return (f'<div class="drop"><button type="button" aria-haspopup="true"{cur}>{title}</button>'
                f'<div class="panel"><div class="wrap"><div class="intro"><span class="label">{title}</span><p>{intro}</p>'
                f'<p><a class="more" href="{href}">Overview</a></p></div><ul>{lis}</ul></div></div></div>')

    journal_cur = ' aria-current="page"' if active == "news" else ""
    groups = "".join(
        f'<div class="group{" small" if i > 1 else ""}"><span class="label">{t}</span>' + "".join(f'<a href="{h}">{lt}</a>' for lt, h, _ in links) + "</div>"
        for i, (t, _, _, _, links) in enumerate(model))
    return f'''<div class="topline" hidden><div class="wrap"><span class="tl-l">Bupa Platinum consultant · Same day imaging and results for new breast symptoms</span><span>Private secretary <a href="tel:{nav["phone_tel"]}">{nav["phone"]}</a></span></div></div>
<header class="site-header">
  <div class="wrap bar">
    <nav class="nav left" aria-label="Primary">{"".join(drop(m) for m in model[:3])}</nav>
    {brand()}
    <nav class="nav right" aria-label="Secondary">{drop(model[3])}<a href="~/news/"{journal_cur}>Blog</a><a class="btn" href="~/booking/">Book</a></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="overlay">Menu</button>
  </div>
</header>
<div class="overlay" id="overlay" aria-hidden="true">
  <div class="wrap top">{brand()}<button class="menu-btn close" type="button" style="display:block">Close</button></div>
  <nav class="wrap" aria-label="Menu">{groups}<div class="group small"><span class="label">Blog</span><a href="~/news/">All articles</a></div></nav>
  <div class="wrap foot">Private secretary <a href="tel:{nav["phone_tel"]}">{nav["phone"]}</a></div>
</div>'''


def footer(nav):
    procs = "".join(f'<li><a href="~/procedures/{p["slug"]}/">{p["nav"]}</a></li>' for p in nav["procedures"])
    locs = "".join(f'<li><a href="~/locations/{l["slug"]}/">{l["name"]}</a></li>' for l in nav["locations"])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="f-cols">
      <div class="f-about">{brand()}<p>Consultant Oncoplastic Breast and General Surgeon, and Clinical Lead of the Breast Unit at Whipps Cross University Hospital, Barts Health NHS Trust. Bupa Platinum consultant, fee-assured. {POSTNOM}.</p>
        <p class="contact">{nav["sec_name"]}, private secretary<br><a href="tel:{nav["phone_tel"]}">{nav["phone"]}</a><br><a href="mailto:{nav["email"]}">{nav["email"]}</a></p></div>
      <div><h4>Treatments</h4><ul>{procs}</ul></div>
      <div><h4>Clinics</h4><ul>{locs}<li><a href="~/locations/">All clinics</a></li></ul></div>
      <div><h4>Patients</h4><ul><li><a href="~/your-visit/">Your first visit</a></li><li><a href="~/fees-and-insurance/">Fees and insurance</a></li><li><a href="~/second-opinion/">Second opinions</a></li><li><a href="~/remote-consultations/">Video and international</a></li><li><a href="~/faqs/">Questions answered</a></li><li><a href="~/booking/">Book</a></li></ul></div>
      <div><h4>About</h4><ul><li><a href="~/biography/">Biography</a></li><li><a href="~/reviews/">Patient reviews</a></li><li><a href="~/podcast/">Podcast and videos</a></li><li><a href="~/news/">Blog</a></li><li><a href="{nav["iwgc"]}" target="_blank" rel="noopener">iWantGreatCare</a></li><li><a href="{nav["youtube"]}" target="_blank" rel="noopener">YouTube</a></li></ul></div>
    </div>
    <div class="f-legal"><span>&copy; 2026 {NAME} · <a href="https://www.gmc-uk.org/registrants/4368515" target="_blank" rel="noopener">GMC 4368515</a> · <a href="~/privacy/">Privacy</a> · <a href="~/cookies/">Cookies</a> · <a href="~/bn/" lang="bn">বাংলা</a> · <a href="~/ar/" lang="ar">العربية</a></span><span>Information on this website is general and not a substitute for a consultation. In an emergency, call 999.</span></div>
  </div>
</footer>
<div class="mbar" aria-label="Quick contact"><a href="tel:{nav["phone_tel"]}">Call</a><a href="~/booking/">Book a consultation</a></div>'''


def appointment_band(nav, title="Let&rsquo;s get you <i>a clear answer</i>", text=None):
    text = text or "Most breast symptoms turn out to be nothing serious. A single appointment is usually all it takes to know for sure. Insured and self-funding patients are welcome at all three clinics."
    return f'''<section class="appt-band"><div class="wrap"><div class="appointment">
  <div><span class="label">Appointments</span><h2 class="mt-1">{title}</h2><p class="lede">{text}</p>
    <div class="actions"><a class="btn" href="~/booking/">Request an appointment</a><a class="btn line" href="~/your-visit/">What to expect</a></div></div>
  <div class="card">
    <div><span class="k">Telephone</span><a class="big" href="tel:{nav["phone_tel"]}">{nav["phone"]}</a></div>
    <div><span class="k">Secretary</span><span class="v">{nav["sec_name"]}</span></div>
    <div><span class="k">Email</span><a href="mailto:{nav["email"]}">{nav["email"]}</a></div>
    <div><span class="k">Clinics</span><span class="v">The Holly, Buckhurst Hill IG9 · Harley Street W1 · St Bartholomew&rsquo;s EC1</span></div>
  </div>
</div></div></section>'''


def render(path, *, title, desc, body, nav, active=None, schema=(), og_type="website",
           image="assets/img/og-card.jpg", priority="0.7", noindex=False, extra_head="", band=True):
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    rel = "../" * depth if depth else "./"
    if path == "404.html":
        rel = "/"  # served from arbitrary URLs, so links must be absolute
    canonical = SITE + "/" + path
    key = path.strip("/").replace("/", "-")
    if image == "assets/img/og-card.jpg" and key and os.path.exists(os.path.join(ROOT, "assets", "og", f"{key}.jpg")):
        image = f"assets/og/{key}.jpg"
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="{"noindex" if noindex else "index, follow, max-image-preview:large"}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#55203f">
<meta property="og:site_name" content="{NAME}, Consultant Breast Surgeon">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{SITE}/{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Mr Zaker Ullah, consultant oncoplastic breast surgeon">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="~/assets/img/icon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="~/assets/img/icon-192.png">
<link rel="apple-touch-icon" href="~/assets/img/apple-touch-icon.png">
<link rel="manifest" href="~/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Blog" href="~/feed.xml">
{FONTS}
<link rel="stylesheet" href="~/assets/css/main.css?v={asset_v("assets/css/main.css")}">
{extra_head}{blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(nav, active)}
<main id="main">
{body}
{appointment_band(nav) if band and not noindex else ""}
</main>
{footer(nav)}
<script src="~/assets/js/main.js?v={asset_v("assets/js/main.js")}" defer></script>
</body>
</html>
'''
    html = html.replace('"~/', '"' + rel).replace(" ~/", " " + rel)
    out = os.path.join(ROOT, "404.html") if path == "404.html" else os.path.join(ROOT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    if not noindex:
        SITEMAP.append((canonical, priority))
