"""Build the whole site:  python3 _build/build.py

Writes HTML into the repo root (which is the deployable site). Blog posts in
content/blog/*.md with a future `date` are skipped until that date; the daily
GitHub Action rebuild publishes them automatically.
"""
import datetime
import os
import re
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402
import md  # noqa: E402
from layout import (NAME, SHORT, PHYSICIAN_REF, POSTNOM, ROOT, SITE, SITEMAP, crumbs_html, crumbs_schema,  # noqa: E402
                    faq_html, faq_schema, picture, render, strip_tags)

TODAY = datetime.date.fromisoformat(os.environ.get("BUILD_DATE", datetime.date.today().isoformat()))
NAV = {"procedures": C.PROCEDURES, "locations": C.LOCATIONS, "phone": C.SEC_PHONE, "phone_tel": C.SEC_TEL,
       "email": C.SEC_EMAIL, "iwgc": C.IWGC, "rating": C.IWGC_RATING, "count": "100% five-star",
       "sec_name": C.SEC_NAME, "youtube": C.YOUTUBE_CHANNEL}
PROC = {p["slug"]: p for p in C.PROCEDURES}
ALL_POSTS = md.load_posts(os.path.join(ROOT, "content", "blog"), TODAY)
POSTS = [p for p in ALL_POSTS if p["published"]]
SCHEDULED = [p for p in ALL_POSTS if not p["published"]]
UPDATED = TODAY.strftime("%-d %B %Y")


def portrait(lazy=True, sizes="(min-width: 64rem) 38vw, 92vw"):
    return picture("zu-portrait", "Mr Md Zaker Ullah, consultant breast surgeon, at Nuffield Health The Holly Hospital", sizes, [600, 900, 1300], 957, 1277, lazy=lazy)


def loc_address(l):
    return f'{l["street"]}, {l["locality"]} {l["postcode"]}'


def hospital_schema(l):
    d = {"@type": "Hospital", "name": l["name"],
         "address": {"@type": "PostalAddress", "streetAddress": l["street"], "addressLocality": l["locality"],
                     "addressRegion": l["region"], "postalCode": l["postcode"], "addressCountry": "GB"}}
    if l.get("tel"):
        d["telephone"] = l["tel"]
    return d


PHYSICIAN = {
    "@context": "https://schema.org", "@type": "Physician", "@id": SITE + "/#physician",
    "name": NAME, "alternateName": ["Mr Zaker Ullah", "Mr M Z Ullah", "Dr Zaker Ullah", "Mr Md Z Ullah"],
    "honorificPrefix": "Mr", "honorificSuffix": POSTNOM,
    "description": "Consultant oncoplastic breast and general surgeon in London and Essex. Clinical Lead of the Breast Unit at Whipps Cross University Hospital, Barts Health NHS Trust. Private practice at The Harley Street Clinic, Nuffield Health at St Bartholomew's and Nuffield Health The Holly Hospital.",
    "url": SITE + "/", "image": SITE + "/assets/img/zu-portrait-900.jpg",
    "telephone": C.SEC_TEL, "email": C.SEC_EMAIL, "priceRange": "££££",
    "address": {"@type": "PostalAddress", "streetAddress": "High Road", "addressLocality": "Buckhurst Hill", "addressRegion": "Essex", "postalCode": "IG9 5HX", "addressCountry": "GB"},
    "areaServed": ["London", "Essex", "Hertfordshire", "Central London", "East London", "North East London", "City of London"],
    "medicalSpecialty": ["Oncologic", "Surgical", "PlasticSurgery"], "isAcceptingNewPatients": True,
    "knowsLanguage": ["en-GB", "bn"],
    "identifier": {"@type": "PropertyValue", "propertyID": "GMC", "value": "4368515"},
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": "MBBS", "credentialCategory": "degree"},
        {"@type": "EducationalOccupationalCredential", "name": "FRCSEd", "recognizedBy": {"@type": "Organization", "name": "Royal College of Surgeons of Edinburgh"}},
        {"@type": "EducationalOccupationalCredential", "name": "FRCS (General Surgery)", "recognizedBy": {"@type": "Organization", "name": "Intercollegiate Specialty Board"}},
    ],
    "memberOf": [{"@type": "Organization", "name": n} for n in ["Association of Breast Surgery", "Association of Surgeons of Great Britain and Ireland", "European Association for Endoscopic Surgery", "Royal College of Surgeons of Edinburgh"]],
    "award": "European Association for Endoscopic Surgery, best video presentation (2003)",
    "hospitalAffiliation": [hospital_schema(l) for l in C.LOCATIONS] + [{"@type": "Hospital", "name": "Whipps Cross University Hospital, Barts Health NHS Trust", "address": {"@type": "PostalAddress", "streetAddress": "Whipps Cross Road", "addressLocality": "London", "postalCode": "E11 1NR", "addressCountry": "GB"}}],
    "availableService": [{"@type": "MedicalProcedure", "name": p["nav"], "url": f"{SITE}/procedures/{p['slug']}/"} for p in C.PROCEDURES],
    "knowsAbout": C.KNOWS_ABOUT,
    "sameAs": [C.IWGC, C.FACEBOOK, C.LINKEDIN, C.YOUTUBE_CHANNEL, "https://www.nuffieldhealth.com/consultants/mr-md-zaker-ullah", "https://www.doctify.com/uk/specialist/mr-md-z-ullah", "https://www.topdoctors.co.uk/doctor/zaker-ullah/", "https://www.finder.bupa.co.uk/Consultant/view/192096/mr_md_z_ullah", "https://whippscrosswf.com/people/mr-md-zaker-ullah/"],
}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": f"{NAME}, Consultant Breast Surgeon", "publisher": PHYSICIAN_REF, "inLanguage": "en-GB"}


def medical_page(path, name, desc):
    return {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": f"{SITE}/{path}", "name": name, "description": desc,
            "inLanguage": "en-GB", "lastReviewed": TODAY.isoformat(), "reviewedBy": PHYSICIAN_REF, "author": PHYSICIAN_REF,
            "audience": {"@type": "Patient"}, "isPartOf": {"@id": SITE + "/#website"}}


# ------------------------------------------------------------------ components
def page_head(crumbs, label, h1, lede, actions="", meta=()):
    m = "".join(f'<div><span class="label">{k}</span><p>{v}</p></div>' for k, v in meta)
    return f'''<header class="page-head"><div class="wrap">{crumbs_html(crumbs)}
<div class="railed"><div class="rail"><span class="label">{label}</span></div><div>
<h1>{h1}</h1><p class="lede">{lede}</p>{f'<div class="actions">{actions}</div>' if actions else ""}
{f'<div class="meta">{m}</div>' if m else ""}</div></div></div></header>'''


def railed(label, inner, sub="", cls="section"):
    return f'<section class="{cls}"><div class="wrap railed"><div class="rail"><span class="label">{label}</span>{f"<span class=label>{sub}</span>" if sub else ""}</div><div>{inner}</div></div></section>'


def treatment_index(items=None):
    items = items or C.PROCEDURES
    lis = "".join(f'<li><a href="~/procedures/{p["slug"]}/"><span class="num">{C.PROCEDURES.index(p) + 1:02d}</span><span class="t">{p["nav"]}</span><span class="d">{p["summary"]}</span><span class="go" aria-hidden="true">&rarr;</span></a></li>' for p in items)
    return f'<ol class="index">{lis}</ol>'


def clinic_cols():
    out = []
    for l in C.LOCATIONS:
        tel = l["phone"] or C.SEC_PHONE
        tel_href = l["tel"] or C.SEC_TEL
        out.append(f'<div class="clinic"><span class="label">{l["area"]}</span><h3>{l["name"]}</h3><address>{l["street"]}<br>{l["locality"]} {l["postcode"]}</address>'
                   f'<a class="tel" href="tel:{tel_href}">{tel}</a><span class="sp"></span><a class="more" href="~/locations/{l["slug"]}/">Clinic details</a></div>')
    return f'<div class="clinics">{"".join(out)}</div>'


def stars():
    return '<span class="stars" role="img" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'


def testimonials(items):
    lis = "".join(f'<li>{stars()}<blockquote>{escape(q)}</blockquote><div class="who"><strong>Verified patient</strong>, {where}, {d}</div></li>' for q, d, where in items)
    return f'<ul class="testimonials">{lis}</ul>'


def review_cards(items):
    lis = "".join(f'<figure class="review-card">{stars()}<blockquote>&ldquo;{escape(q)}&rdquo;</blockquote><figcaption>Verified patient, {where}, {d}</figcaption></figure>' for q, d, where in items)
    return f'<div class="review-grid">{lis}</div>'


def rating_block():
    return f'''<div class="rating"><span class="score">{C.IWGC_RATING}<small>out of 5</small></span>
<p>{stars()}Average rating on iWantGreatCare, where 100% of his independent, verified reviews are five stars.</p></div>'''


VIDEO_ENTRIES = [{**v, "description": v["desc"], "category": f"Video, in {v['lang']}", "date_obj": datetime.date.fromisoformat(v["date"]), "thumb": v["id"]} for v in C.VIDEOS]
ENTRIES = sorted(POSTS + VIDEO_ENTRIES, key=lambda e: e["date_obj"], reverse=True)


def journal_list(entries, grid=True):
    out = []
    for p in entries:
        thumb = f'<span class="thumb"><img src="https://i.ytimg.com/vi/{p["thumb"]}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy"></span>' if p.get("thumb") else ""
        out.append(f'<li><a href="~/news/{p["slug"]}/">{thumb}<span class="label">{escape(p["category"])}</span><span><span class="t">{escape(p["title"])}</span><span class="d">{escape(p["description"])}</span></span><span class="m">{p["date_obj"].strftime("%-d %B %Y")}</span></a></li>')
    return f'<ul class="journal{" grid" if grid else ""}">{"".join(out)}</ul>'


def video(vid=None, title=None, label=None):
    P = C.PODCAST
    vid, title = vid or P["youtube"], title or P["title"]
    return f'''<div class="video" data-yt="{vid}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{escape(title)}" width="480" height="360" loading="lazy">
<button class="play" type="button" aria-label="Play video: {escape(title)}"><span>Play</span></button></div>'''


def faq_section(faqs, title="Questions", label="Questions"):
    return railed(label, f'<h2>{title}</h2><div class="mt-3">{faq_html(faqs)}</div>', cls="section rule")


def with_ids(html):
    """Give each <h2> an id and return (html, [(id, text)]) for a contents list."""
    toc = []

    def rep(m):
        text = strip_tags(m.group(1))
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        toc.append((slug, text))
        return f'<h2 id="{slug}">{m.group(1)}</h2>'
    html = re.sub(r'<h2(?: id="[^"]*")?>(.*?)</h2>', rep, html)
    return html, toc


def toc_html(toc, extra=()):
    items = list(toc) + list(extra)
    return '<nav class="toc" aria-label="Contents">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in items) + "</nav>"


def appt_aside():
    return f'''<div class="block appt"><h3>Arrange a consultation</h3><p>Harley Street, the City of London and The Holly, Buckhurst Hill.</p>
<a class="tel" href="tel:{C.SEC_TEL}">{C.SEC_PHONE}</a><a class="btn" href="~/booking/">Request an appointment</a></div>'''


def quote_band(r, cls="section tone tight", label="A patient writes"):
    return f'<section class="{cls}"><div class="wrap railed"><div class="rail"><span class="label">{label}</span></div><div><figure class="quote">{stars()}<blockquote class="mt-1">{escape(r[0])}</blockquote><figcaption><span>Verified patient, {r[2]}, {r[1]}</span><a class="more" href="~/reviews/">Rated {C.IWGC_RATING}, 100% five-star</a></figcaption></figure></div></div></section>'


HOME_FAQS = [
    ("How quickly can I see Mr Ullah?", "New breast symptoms are given priority. Face to face appointments can often be arranged within days, and a video or telephone consultation can usually be arranged within 24 to 48 hours of your enquiry."),
    ("Will I get my results on the same day?", "At his one-stop clinics, imaging and provisional results are usually given on the same day. Biopsy results, where a biopsy is needed, follow within a few days."),
    ("Is Mr Ullah the same person as Dr Zaker Ullah?", "Yes. Surgeons in the United Kingdom who hold the fellowship of a Royal College of Surgeons are addressed as Mr rather than Dr. You may see him called Dr Zaker Ullah on his YouTube channel and in older articles; it is the same surgeon."),
    ("Do I need a GP referral?", "Insured patients usually need one before their insurer will authorise the appointment. Self-funding patients can book directly. <a href=\"~/fees-and-insurance/\">Fees and insurance</a>."),
    ("Is Mr Ullah recognised by Bupa?", "Yes. Mr Ullah is a Bupa Platinum consultant, fee-assured, and part of Bupa&rsquo;s Open Referral network. He is also recognised by AXA Health, Aviva, Vitality, WPA, Cigna and other major insurers."),
]


# ================================================================== HOME
def build_home():
    P = C.PODCAST
    body = f'''
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="label">Consultant breast surgeon in London and Essex</span>
      <h1 class="mt-2">Expert breast care, with time to listen</h1>
      <p class="lede">{SHORT} is a consultant oncoplastic breast surgeon and leads the Breast Unit at Whipps Cross University Hospital. Most breast symptoms turn out to be nothing serious, and his one-stop clinics give you imaging and provisional results on the same day. When surgery is needed, he plans the treatment and the result together.</p>
      <div class="actions"><a class="btn coral" href="~/booking/">Book a consultation</a><a class="btn line" href="~/procedures/">Explore treatments</a></div>
      <div class="proof"><span>{stars()} <strong>{C.IWGC_RATING}</strong>, 100% five-star reviews</span><span class="sep"></span><span>Consultations in English and Bengali</span></div>
    </div>
    <div class="arch">{portrait(lazy=False)}
      <div class="badge"><b>30+</b><span><strong style="color:var(--navy)">years in surgery</strong><br>Royal Marsden trained</span></div></div>
  </div>
  <div class="facts-strip">
    <div><span class="k">Same day</span><span class="v">Imaging and provisional results at one-stop clinics</span></div>
    <div><span class="k">24 to 48 hours</span><span class="v">For a video or telephone consultation</span></div>
    <div><span class="k">Clinical Lead</span><span class="v">Breast Unit, Whipps Cross, Barts Health NHS Trust</span></div>
    <div><span class="k">Bupa Platinum</span><span class="v">Platinum consultant, fee-assured, in Bupa&rsquo;s Open Referral network</span></div>
  </div>
</div></section>

<section class="section tight"><div class="wrap"><div class="reassure">
  <div class="big">9<small> in 10</small></div>
  <div><h2>Most breast lumps are not cancer</h2><p>Cysts, fibroadenomas and normal breast tissue are far more common. The only way to be sure is a proper assessment, and at a one-stop clinic that usually takes a single visit.</p></div>
  <a class="btn" href="~/procedures/benign-breast-conditions/">The one-stop clinic</a>
</div></div></section>

{railed("His approach", f"""<p class="statement fade">One surgeon plans your cancer treatment and the shape of your breast together, from the very first appointment. <span class="muted">That is oncoplastic surgery, and it is the heart of Mr Ullah&rsquo;s practice.</span></p>
<div class="cols-2 mt-3"><p class="stone">He trained at The Royal Marsden, St Mary&rsquo;s and The Royal Free, and has been a consultant at Barts Health NHS Trust since 2012. At Whipps Cross he introduced the one-stop breast clinic and fat grafting for breast reconstruction.</p>
<p class="stone">The surgeon who examines you is the surgeon who operates and who looks after you afterwards. Patients describe him, again and again, as someone who listens and never rushes.</p></div>
<p class="mt-3"><a class="more" href="~/biography/">About Mr Ullah</a></p>""")}

<section class="section tone"><div class="wrap railed"><div class="rail"><span class="label">Treatments</span><span class="label">{len(C.PROCEDURES)} specialties</span></div><div>
<h2>How Mr Ullah can help</h2><div class="mt-3">{treatment_index()}</div><p class="mt-3"><a class="more" href="~/procedures/">All treatments</a></p></div></div></section>

<section class="section night"><div class="wrap railed"><div class="rail"><span class="label">Patient reviews</span></div><div>
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:2rem"><h2 style="max-width:13em">Kind, thorough and never rushed</h2>{rating_block()}</div>
  <div class="mt-3">{review_cards(C.REVIEWS[:6])}</div>
  <p class="mt-3"><a class="more" href="~/reviews/">Read every review</a></p>
</div></div></section>

{railed("Clinics", f'<h2>Three private clinics</h2><p class="lede mt-1">Central London, the City, and the border of London and Essex, with parking at The Holly.</p><div class="mt-3">{clinic_cols()}</div>')}

<section class="section blush"><div class="wrap railed"><div class="rail"><span class="label">Watch and listen</span><span class="label">{P["date_label"]}</span></div><div>
  <div class="pod">{video()}
  <div><h2>Five questions about breast cancer, answered by a surgeon</h2><p class="lede mt-1">Mr Ullah on <em>{P["show"]}</em>, recorded before a live audience.</p>
  <ol class="chapters">{"".join(f"<li>{c}</li>" for c in P["chapters"])}</ol>
  <p class="mt-2"><a class="more" href="~/podcast/">Podcast and videos</a></p></div></div>
  <p class="mt-3 stone">He also presents health advice in Bengali, for TV3 Bangla and on his own YouTube channel.</p>
</div></div></section>

{railed("Journal", f'<h2>Clear answers, in plain English</h2><div class="mt-3">{journal_list(POSTS[:3])}</div><p class="mt-3"><a class="more" href="~/news/">All articles and videos</a></p>') if POSTS else ""}

{faq_section(HOME_FAQS, "Questions patients ask first")}
'''
    render("", title="Breast Surgeon London & Essex | Mr Zaker Ullah FRCS",
           desc=f"Mr Zaker Ullah FRCS, consultant breast surgeon in London and Essex, 100% five-star reviews. Same day results at The Holly, Buckhurst Hill, Harley Street and St Bartholomew's.",
           body=body, nav=NAV, schema=[PHYSICIAN, WEBSITE, faq_schema(HOME_FAQS)], priority="1.0")


# ================================================================== ABOUT
def build_about():
    path = "biography/"
    crumbs = [("Home", ""), ("Biography", path)]
    faqs = [
        ("Why is Mr Ullah called Mr and not Dr?", "In British surgical tradition, doctors who gain the fellowship of a Royal College of Surgeons are addressed as Mr, Miss, Ms or Mrs rather than Dr. The title marks the completion of advanced surgical training."),
        ("Does Mr Ullah treat NHS patients?", "Yes. He leads the NHS breast unit at Whipps Cross University Hospital, part of Barts Health NHS Trust. NHS referrals are made through your GP in the usual way. This website describes his private practice."),
        ("Does Mr Ullah speak Bengali?", "Yes. Mr Ullah consults in English and Bengali, and many patients and families value discussing a diagnosis in their first language."),
        ("Can I see Mr Ullah for a second opinion?", "Yes. Many patients see him for a second opinion on a diagnosis or a proposed operation. <a href=\"~/second-opinion/\">More about second opinions</a>."),
    ]
    body = page_head(crumbs, "Biography", NAME, f"Consultant Oncoplastic Breast and General Surgeon at Barts Health NHS Trust, and Clinical Lead of the Breast Unit at Whipps Cross University Hospital.",
                     meta=[("Qualifications", POSTNOM), ("GMC registration", '<a href="https://www.gmc-uk.org/registrants/4368515" target="_blank" rel="noopener">No. 4368515</a>'), ("Languages", "English and Bengali")]) + f'''
<section class="section"><div class="wrap railed"><div class="rail"><figure class="figure tall">{portrait(sizes="(min-width: 64rem) 15rem, 92vw")}</figure></div>
<div class="prose">
<p>Mr Ullah qualified in medicine in 1987 and began his surgical training in the United Kingdom in 1993. He trained through the North East Thames rotation, with higher surgical posts at <strong>The Royal Marsden</strong>, Europe&rsquo;s largest specialist cancer centre, and at <strong>St Mary&rsquo;s</strong>, <strong>The Royal Free</strong> and Broomfield hospitals. It was there that his interest in oncoplastic breast surgery took shape.</p>
<h2>Consultant practice</h2>
<p>He was appointed consultant at <strong>Barts Health NHS Trust in 2012</strong> and is Clinical Lead of the Breast Unit at Whipps Cross University Hospital. He introduced the hospital&rsquo;s <strong>one-stop breast clinic</strong>, where patients with new symptoms are examined, imaged and, where needed, biopsied at a single visit. He also introduced <strong>fat grafting</strong> for breast deformity at the hospital.</p>
<p>His practice covers the full range of modern breast surgery: breast conserving cancer surgery and therapeutic mammoplasty, mastectomy, reconstruction with implants and with latissimus dorsi, chest wall perforator and Grisotti flaps, fat grafting, nipple reconstruction, risk reducing surgery for carriers of BRCA and other gene variants, and reduction and uplift for symmetry. In general surgery he maintains a laparoscopic practice in gallstone disease, hernia repair and appendicectomy.</p>
<h2>Teaching and research</h2>
<p>Mr Ullah is a clinical and educational supervisor to surgeons in training and directs the <strong>Whipps Cross Higher Surgery FRCS course</strong>, which prepares senior trainees for the fellowship examination of the Royal Colleges of Surgeons. He gives regular educational talks to local GPs.</p>
<p>His keyhole hernia repair technique, using a glove balloon, won the prize for <strong>best video presentation at the European Association for Endoscopic Surgery</strong> in 2003. He has published research on oncoplastic reconstruction, laparoscopic hernia repair, breast cancer in Asian populations and diagnostic laparoscopy.</p>
<h2>Beyond the clinic</h2>
<p>He is a trustee of Planetary Health Academia, a consortium of doctors of Bangladeshi heritage, and speaks at international cancer meetings. In October 2026 he joined Rosie Fawehimi on her podcast <a href="~/podcast/"><em>Everything Changed</em></a> to answer the questions patients ask most.</p>
</div></div></section>
<section class="section tone"><div class="wrap railed"><div class="rail"><span class="label">Career</span></div><div>
<h2>Appointments and distinctions</h2>
<ol class="timeline mt-3">
<li><span class="y">1987</span><div><h3>Qualifies in medicine</h3><p>MBBS.</p></div></li>
<li><span class="y">1993</span><div><h3>Begins surgical training in the United Kingdom</h3><p>North East Thames rotation through London teaching and district general hospitals.</p></div></li>
<li><span class="y">1996</span><div><h3>Fellow of the Royal College of Surgeons of Edinburgh</h3><p>FRCSEd.</p></div></li>
<li><span class="y">2003</span><div><h3>European Association for Endoscopic Surgery</h3><p>Best video presentation, for a keyhole hernia repair technique.</p></div></li>
<li><span class="y">2009</span><div><h3>FRCS in General Surgery</h3><p>Specialty fellowship, following higher training including The Royal Marsden, St Mary&rsquo;s and The Royal Free.</p></div></li>
<li><span class="y">2012</span><div><h3>Consultant, Barts Health NHS Trust</h3><p>Oncoplastic breast and general surgeon at Whipps Cross University Hospital.</p></div></li>
<li><span class="y">Today</span><div><h3>Clinical Lead, Whipps Cross Breast Unit</h3><p>Leads the unit, directs the FRCS course, and sees private patients at Harley Street, St Bartholomew&rsquo;s and The Holly.</p></div></li>
</ol></div></div></section>
{railed("Memberships", '<dl class="facts"><div><dt>Fellowships</dt><dd>Royal College of Surgeons of Edinburgh (FRCSEd). FRCS in General Surgery.</dd></div><div><dt>Associations</dt><dd>Association of Breast Surgery. Association of Surgeons of Great Britain and Ireland. European Association for Endoscopic Surgery.</dd></div><div><dt>Register</dt><dd>General Medical Council, no. 4368515, on the Specialist Register.</dd></div><div><dt>NHS</dt><dd>Consultant, Barts Health NHS Trust, since 2012.</dd></div></dl>')}
{faq_section(faqs, "About Mr Ullah")}'''
    render(path, title="Mr Md Zaker Ullah FRCS | Biography, Consultant Breast Surgeon",
           desc="Biography of Mr Md Zaker Ullah FRCS: Royal Marsden trained oncoplastic breast surgeon, Barts Health consultant since 2012, Clinical Lead of the Whipps Cross Breast Unit.",
           body=body, nav=NAV, active="about", priority="0.9",
           schema=[PHYSICIAN, {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": PHYSICIAN_REF, "dateModified": TODAY.isoformat()}, crumbs_schema(crumbs), faq_schema(faqs)])


# ================================================================== TREATMENTS
def build_procedures():
    crumbs = [("Home", ""), ("Treatments", "procedures/")]
    body = page_head(crumbs, "Treatments", "Areas of practice",
                     "The diagnosis and surgical treatment of breast disease, benign and malignant, with oncoplastic and reconstructive surgery, the male breast, and keyhole general surgery.") + \
        railed("Index", treatment_index() + '<p class="note mt-3" style="max-width:38rem">Not sure where to begin? Start with a consultation. The right operation, and whether to operate at all, follows from the diagnosis.</p>')
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/procedures/{p['slug']}/", "name": p["nav"]} for i, p in enumerate(C.PROCEDURES)]}
    render("procedures/", title="Breast Surgery Treatments London & Essex | Mr Zaker Ullah",
           desc="Breast and general surgery with Mr Zaker Ullah FRCS in London and Essex: breast lump clinics, cancer surgery, reconstruction, reduction, gynaecomastia and keyhole surgery.",
           body=body, nav=NAV, active="procedures", priority="0.9", schema=[items, crumbs_schema(crumbs)])

    for i, p in enumerate(C.PROCEDURES):
        path = f"procedures/{p['slug']}/"
        crumbs = [("Home", ""), ("Treatments", "procedures/"), (p["nav"], path)]
        sections, toc = with_ids(p["sections"])
        glance = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["glance"])
        rel = "".join(f'<li><a href="~/procedures/{s}/">{PROC[s]["nav"]}</a></li>' for s in p["related"])
        rel += "".join(f'<li><a href="~/news/{x["slug"]}/">{escape(x["title"])}</a></li>' for x in POSTS if p["slug"] in x["related"][:2])[:2000]
        q = C.REVIEWS[(i + 2) % len(C.REVIEWS)]
        body = page_head(crumbs, f"Treatment {i + 1:02d}", p["h1"], p["lede"],
                         actions=f'<a class="btn" href="~/booking/">Book a consultation</a><a class="btn line" href="#questions">Questions</a>') + f'''
<section class="section"><div class="wrap article">
  <div class="rail"><span class="label">Contents</span>{toc_html(toc, [("questions", "Questions")])}</div>
  <div><div class="byline"><img src="~/assets/img/zu-head-400.webp" alt="" width="400" height="400" loading="lazy"><span>Written and medically reviewed by <a href="~/biography/">{NAME} FRCS</a>. Updated {UPDATED}.</span></div>
    <div class="prose">{sections}<p class="note">This page is general information and not medical advice. Whether a procedure is right for you can only be decided in consultation.</p></div></div>
  <aside class="aside"><div class="block"><span class="label">At a glance</span><dl>{glance}</dl></div>{appt_aside()}<div class="block"><span class="label">Related</span><ul>{rel}</ul></div></aside>
</div></section>
{quote_band(q)}
<div id="questions"></div>{faq_section(p["faqs"], f"Questions about {p['nav'].lower()}")}'''
        render(path, title=p["title"], desc=p["desc"], body=body, nav=NAV, active="procedures", priority="0.9",
               schema=[medical_page(path, p["h1"], p["desc"]),
                       {"@context": "https://schema.org", "@type": "MedicalProcedure", "name": p["nav"], "url": f"{SITE}/{path}", "description": p["lede"], "performer": PHYSICIAN_REF},
                       crumbs_schema(crumbs), faq_schema(p["faqs"])])


def build_second_opinion():
    path = "second-opinion/"
    crumbs = [("Home", ""), ("Second opinions", path)]
    faqs = [
        ("Will a second opinion delay my treatment?", "Rarely. A private second opinion can usually be arranged within days, and for most breast cancers a short pause to be sure of the plan does not affect the outcome. If timing is critical in your case, Mr Ullah will say so plainly."),
        ("Do I need to tell my current team?", "It is helpful but not required. Most consultants welcome a second opinion, and your team can share imaging and pathology to make the review complete."),
        ("What should I bring?", "Clinic letters, imaging reports (and the images themselves if possible), biopsy or pathology reports, and a list of your questions. The private secretary can help to request records."),
        ("Is a second opinion covered by insurance?", "Many UK insurers cover a second opinion consultation. Check with your insurer and obtain a pre-authorisation number first."),
    ]
    body = page_head(crumbs, "Second opinions", "A second opinion on breast cancer or breast surgery",
                     "An independent view from an experienced oncoplastic breast surgeon can confirm a plan, or show you options you had not been offered.",
                     actions='<a class="btn" href="~/booking/">Request a second opinion</a>') + \
        railed("When to ask", '''<div class="prose"><p>Patients most often ask for a second opinion when:</p><ul>
<li>A mastectomy has been advised and they want to know whether breast conserving or oncoplastic surgery is possible</li>
<li>They want to understand reconstruction before cancer surgery rather than after it</li>
<li>A benign diagnosis has been given but symptoms persist</li>
<li>They are considering risk reducing surgery because of a BRCA or other gene variant, or a strong family history</li>
<li>They are unhappy with the result of previous breast surgery</li></ul>
<h2>What Mr Ullah reviews</h2><p>Your history and examination, your imaging and pathology, and where useful a request for further tests or a specialist review of the scans or slides. You receive a clear explanation of what he would recommend and why, with a letter for you and for your existing team.</p></div>''') + \
        quote_band(C.REVIEWS[2]) + \
        faq_section(faqs, "Questions about second opinions")
    desc = "Breast cancer second opinion in London and Essex with consultant oncoplastic surgeon Mr Zaker Ullah: diagnosis, mastectomy or conservation, and reconstruction options."
    render(path, title="Breast Cancer Second Opinion London | Mr Zaker Ullah FRCS", desc=desc, body=body, nav=NAV, active="about", priority="0.8",
           schema=[medical_page(path, "Breast cancer second opinion", desc), crumbs_schema(crumbs), faq_schema(faqs)])


# ================================================================== CLINICS
def build_locations():
    crumbs = [("Home", ""), ("Clinics", "locations/")]
    body = page_head(crumbs, "Clinics", "Private clinics in London and Essex",
                     "Mr Ullah sees private patients at three hospitals: in London&rsquo;s medical district, within the St Bartholomew&rsquo;s site in the City, and at Buckhurst Hill on the Essex border.") + \
        railed("Three clinics", clinic_cols()) + \
        railed("NHS", f'<h3>Whipps Cross University Hospital</h3><p class="stone mt-1" style="max-width:38rem">Whipps Cross Road, London E11 1NR. Mr Ullah is Clinical Lead of the Breast Unit, part of Barts Health NHS Trust. NHS referrals are made through your GP.</p><p class="mt-2"><a class="more" href="https://www.bartshealth.nhs.uk/find-a-consultant/contact/md-zaker-ullah-301/?consultant=301" target="_blank" rel="noopener">Barts Health profile</a></p>', cls="section rule")
    render("locations/", title="Private Breast Clinics London & Essex | Mr Zaker Ullah",
           desc="Where to see breast surgeon Mr Zaker Ullah privately: The Harley Street Clinic W1, Nuffield Health St Bartholomew's EC1 and Nuffield Health The Holly, Buckhurst Hill IG9.",
           body=body, nav=NAV, active="locations", priority="0.9", schema=[crumbs_schema(crumbs)])

    for l in C.LOCATIONS:
        path = f"locations/{l['slug']}/"
        crumbs = [("Home", ""), ("Clinics", "locations/"), (l["short"], path)]
        maps = "https://www.google.com/maps/search/?api=1&query=" + (l["name"] + " " + l["postcode"]).replace(" ", "+").replace("'", "")
        appts = f'Private secretary <a href="tel:{C.SEC_TEL}">{C.SEC_PHONE}</a>' + (f'<br>Hospital {l["phone"]}' if l["phone"] else "")
        meta = [("Address", f'{l["street"]}<br>{l["locality"]} {l["postcode"]}'), ("Appointments", appts)]
        meta.append(("Clinic times", l["clinics"]) if l.get("clinics") else ("Operated by", l["operator"]))
        faqs = [
            (f"How do I book with Mr Ullah at {l['name']}?", f"Call his private secretary on {C.SEC_PHONE}, send an enquiry through this website, or ask your GP to refer you to Mr Md Zaker Ullah at {l['name']}. Insured patients should obtain a pre-authorisation number from their insurer first."),
            (f"Where is {l['name']}?", f"{l['name']} is at {loc_address(l)}. {l['travel']}"),
            ("Which conditions does Mr Ullah treat here?", "New breast lumps and breast pain, nipple discharge, breast cancer surgery, reconstruction, breast reduction, fat grafting, gynaecomastia, and general surgery including hernia and gallbladder operations. Some operations take place only at particular hospitals; the secretary will advise."),
            ("Can I be seen quickly with a new breast symptom?", "Yes. New breast symptoms are given priority, with the aim of examination, imaging and any biopsy at a single visit."),
        ]
        if l.get("local"):
            faqs[0:0] = [("Is there a private breast surgeon near Woodford Green?", "Yes. Mr Ullah consults at Nuffield Health The Holly Hospital on the High Road in Buckhurst Hill, a few minutes from Woodford Green, South Woodford, Loughton and Chigwell, with parking on site. His Rapid Access Breast Clinic runs on Tuesday afternoons."),
                         ("Can I see Mr Ullah at The Holly if I am an NHS patient at Whipps Cross?", "Yes, if you choose to be seen privately, either through insurance or as a self-funding patient. Mr Ullah leads the breast unit at Whipps Cross and many patients from the area see him at The Holly.")]
        others = "".join(f'<li><a href="~/locations/{o["slug"]}/">{o["name"]}</a></li>' for o in C.LOCATIONS if o is not l)
        body = page_head(crumbs, l["area"], l["h1"], l["intro"], meta=meta,
                         actions=f'<a class="btn" href="~/booking/">Book at {l["short"]}</a><a class="btn line" href="{maps}" target="_blank" rel="noopener">Map</a>') + \
            railed("The clinic", '<ul class="list-plain">' + "".join(f"<li>{w}</li>" for w in l["why"]) + "</ul>") + \
            (railed("Close to home", f'<p class="lede">{l["local"]}</p>') if l.get("local") else "") + \
            railed("Getting here", f'<p class="lede">{l["travel"]}</p><p class="mt-2"><a class="more" href="{maps}" target="_blank" rel="noopener">Open in Google Maps</a></p>', cls="section rule") + \
            railed("Patients from", '<div class="areas">' + "".join(f"<span>{a}</span>" for a in l["serves"]) + '</div><p class="stone mt-1">And many travel from further afield.</p>', cls="section rule") + \
            railed("Treatments here", treatment_index(), cls="section rule") + \
            quote_band(C.REVIEWS[3]) + \
            faq_section(faqs, f"Seeing Mr Ullah at {l['short']}") + \
            railed("Other clinics", f'<ul class="list-plain">{others}</ul>', cls="section rule tight")
        clinic = {"@context": "https://schema.org", "@type": "MedicalClinic", "@id": f"{SITE}/{path}#clinic",
                  "name": f"{NAME}, Breast Surgeon at {l['name']}", "url": f"{SITE}/{path}", "image": PHYSICIAN["image"],
                  "telephone": C.SEC_TEL, "priceRange": "££££", "medicalSpecialty": ["Oncologic", "Surgical", "PlasticSurgery"],
                  "address": hospital_schema(l)["address"], "areaServed": l["serves"], "employee": PHYSICIAN_REF,
                  "containedInPlace": hospital_schema(l), "hasMap": maps, "isAcceptingNewPatients": True}
        render(path, title=l["title"], desc=l["desc"], body=body, nav=NAV, active="locations", priority="0.9",
               schema=[clinic, crumbs_schema(crumbs), faq_schema(faqs)])


# ================================================================== PATIENT INFORMATION
VISIT_FAQS = [
    ("How long is the first appointment?", "Allow up to an hour and a half if you have a new breast symptom, so that imaging and any biopsy can take place at the same visit. Follow-up appointments are shorter."),
    ("Can I bring someone with me?", "Yes, and many patients do. A relative or friend can help you remember what was said and ask the questions you may forget."),
    ("Will my GP be told?", "With your consent, Mr Ullah writes to your GP after each consultation so that your medical record stays complete."),
    ("Can I have a chaperone?", "Yes. A chaperone is always available for examinations, and you can ask for one at any point."),
]
FEES_FAQS = [
    ("Do I need a GP referral if I am insured?", "Most insurers ask for a GP referral before they authorise a specialist appointment. Some accept a referral from a digital GP service included in your policy. Check with your insurer."),
    ("Is Mr Ullah fee-assured?", "Yes. Mr Ullah is a Bupa Platinum consultant and fee-assured with Bupa, and is recognised by the other major UK insurers, so you should not face a shortfall for his fees. Confirm your own cover with your insurer."),
    ("How much does a consultation cost if I am self-funding?", "Consultation fees are set and confirmed by each hospital when you book. For tests or surgery, the hospital provides a written, fixed price before you commit."),
    ("Is breast reconstruction covered?", "Reconstruction after breast cancer, including surgery to the other breast for symmetry, is normally covered by insurers as part of cancer treatment. Cosmetic procedures generally are not."),
]


def build_patient_pages():
    path = "your-visit/"
    crumbs = [("Home", ""), ("Your first visit", path)]
    body = page_head(crumbs, "Patients", "Your first visit",
                     "What to expect from a first appointment with Mr Ullah, from booking to the plan you leave with.",
                     actions='<a class="btn" href="~/booking/">Book a consultation</a>') + \
        railed("Four stages", '''<ol class="steps">
<li><h3>Booking</h3><p>Call the private secretary or send an enquiry. If you are insured, obtain a GP referral and a pre-authorisation number from your insurer.</p></li>
<li><h3>Consultation</h3><p>A full history and examination with Mr Ullah himself, with time to talk and to ask questions.</p></li>
<li><h3>Assessment</h3><p>Ultrasound, mammography and needle biopsy at the same visit where needed. This is triple assessment.</p></li>
<li><h3>The plan</h3><p>Results and a written plan. If surgery is needed, the surgeon who examined you is the surgeon who operates.</p></li></ol>''') + \
        railed("Bring with you", '<ul class="list-plain"><li>Your GP referral letter, if you have one</li><li>Any previous breast imaging or biopsy results</li><li>A list of the medicines you take</li><li>Your insurance details and pre-authorisation number</li><li>A list of your questions</li></ul><p class="note mt-2">If you may need a mammogram, avoid deodorant and talcum powder on the day.</p>', cls="section rule") + \
        railed("Afterwards", '<div class="prose"><p>Imaging findings are usually explained on the day. Biopsy results normally take a few working days, after which Mr Ullah sees you again or telephones to explain them. If treatment is needed, it is planned with you and, for cancer, with a multidisciplinary team.</p><p>With your consent, Mr Ullah writes to your GP after each consultation. You can read about <a href="~/fees-and-insurance/">fees and insurance</a> or see <a href="~/faqs/">every common question</a>.</p></div>', cls="section rule") + \
        faq_section(VISIT_FAQS, "Questions about your visit")
    render(path, title="Your First Appointment with a Breast Surgeon | Mr Zaker Ullah",
           desc="What happens at a first private appointment with consultant breast surgeon Mr Zaker Ullah: booking, examination, imaging and biopsy, results and what to bring.",
           body=body, nav=NAV, active="patients", priority="0.8", schema=[crumbs_schema(crumbs), faq_schema(VISIT_FAQS)])

    path = "fees-and-insurance/"
    crumbs = [("Home", ""), ("Fees and insurance", path)]
    body = page_head(crumbs, "Patients", "Fees and insurance",
                     "Mr Ullah sees insured and self-funding patients at each of his clinics. Here is how payment and authorisation work.") + \
        railed("Insured", f'<div class="prose"><p>Mr Ullah is recognised by the major UK private medical insurers and is fee-assured with the principal insurers, so you should not face a shortfall for his fees.</p><p>With Bupa he is a <strong>Platinum consultant</strong>, <strong>fee-assured</strong>, and part of Bupa&rsquo;s <strong>Open Referral network</strong>. If your GP gives an open referral, ask Bupa for Mr Md Z Ullah by name, or choose Nuffield Health The Holly in Buckhurst Hill.</p><p>Before your first appointment, most insurers ask for two things: a <strong>GP referral</strong>, and a <strong>pre-authorisation number</strong>, which you obtain by calling your insurer with the referral. Bring the number to your appointment.</p></div><div class="mt-3"><span class="label">Recognised by</span><div class="insurers mt-1">{"".join(f"<span>{i}</span>" for i in C.INSURERS)}</div></div>') + \
        railed("Self-funding", '<div class="prose"><p>You do not need insurance or a referral. The hospital confirms the consultation fee when you book. If you need tests or surgery, it gives you a written, fixed price before anything is arranged, so there are no surprises.</p><p>Each hospital sets its own prices, which is why they are not published here. The <a href="~/booking/">private secretary</a> can tell you who to ask.</p></div>', cls="section rule") + \
        faq_section(FEES_FAQS, "Questions about fees")
    render(path, title="Fees & Insurance | Private Breast Surgeon Mr Zaker Ullah",
           desc="Seeing Mr Zaker Ullah privately: insurers he is recognised by, GP referrals and pre-authorisation, and how self-funding prices are confirmed by each hospital.",
           body=body, nav=NAV, active="patients", priority="0.7", schema=[crumbs_schema(crumbs), faq_schema(FEES_FAQS)])

    path = "faqs/"
    crumbs = [("Home", ""), ("Questions answered", path)]
    groups = [("Appointments", VISIT_FAQS), ("Fees and insurance", FEES_FAQS)] + [(p["nav"], p["faqs"]) for p in C.PROCEDURES]
    inner = "".join(f'<div class="faq-group"><h2 id="{re.sub("[^a-z]+", "-", g.lower())}">{g}</h2><div class="mt-2">{faq_html(f)}</div></div>' for g, f in groups)
    toc = toc_html([(re.sub("[^a-z]+", "-", g.lower()), g) for g, _ in groups])
    body = page_head(crumbs, "Patients", "Questions answered", "Answers to the questions patients ask most often, gathered from every page of this website.") + \
        f'<section class="section"><div class="wrap article" style="grid-template-columns:var(--rail) minmax(0,1fr)"><div class="rail"><span class="label">Topics</span>{toc}</div><div>{inner}</div></div></section>'
    render(path, title="Breast Surgery Questions Answered | Mr Zaker Ullah FRCS",
           desc="Answers from consultant breast surgeon Mr Zaker Ullah to common questions on breast lumps, cancer surgery, reconstruction, reduction, gynaecomastia, fees and appointments.",
           body=body, nav=NAV, active="patients", priority="0.7", schema=[crumbs_schema(crumbs)])


# ================================================================== REVIEWS
def build_reviews():
    path = "reviews/"
    crumbs = [("Home", ""), ("Patient reviews", path)]
    body = page_head(crumbs, "Patient reviews", "What his patients say",
                     f"Mr Ullah&rsquo;s reviews are collected independently by iWantGreatCare, the UK&rsquo;s platform for verified healthcare feedback. Every one of them is five stars.",
                     actions=f'<a class="btn" href="{C.IWGC}" target="_blank" rel="noopener">Read all on iWantGreatCare</a><a class="btn line" href="{C.IWGC}" target="_blank" rel="noopener">Leave a review</a>') + \
        railed("Rating", rating_block()) + \
        railed("In their words", testimonials(C.REVIEWS) + '<p class="note mt-2">Excerpts are reproduced word for word from public reviews on iWantGreatCare, some shortened where marked. They refer to care at The Holly and at Whipps Cross University Hospital.</p>', cls="section rule") + \
        railed("Your experience", f'<p class="lede">If Mr Ullah has treated you, a review helps future patients choose their care. Reviews can be left anonymously. If something did not go as it should have, please also tell the hospital where you were treated.</p><p class="mt-2"><a class="more" href="{C.IWGC}" target="_blank" rel="noopener">Review Mr Ullah on iWantGreatCare</a></p>', cls="section rule")
    render(path, title=f"Mr Zaker Ullah Reviews: Rated {C.IWGC_RATING}, 100% Five-Star",
           desc=f"Verified patient reviews of consultant breast surgeon Mr Md Zaker Ullah FRCS on iWantGreatCare: rated {C.IWGC_RATING} out of 5, with 100% five-star reviews.",
           body=body, nav=NAV, active="about", priority="0.8", schema=[crumbs_schema(crumbs)])
    render("feedback/", title="Patient reviews", desc="This page has moved to /reviews/.", nav=NAV, noindex=True,
           extra_head='<meta http-equiv="refresh" content="0; url=../reviews/">',
           body='<section class="section"><div class="wrap"><p>This page has moved. <a href="~/reviews/">Read patient reviews</a>.</p></div></section>')


# ================================================================== PODCAST
def build_podcast():
    P = C.PODCAST
    path = "podcast/"
    crumbs = [("Home", ""), ("Podcast and videos", path)]
    qa = [
        ("Lumpectomy or mastectomy: how is the decision made?", "It depends on the size of the cancer relative to the breast, where it lies, whether there is more than one area, genetics and, above all, the patient&rsquo;s own wishes. Oncoplastic techniques mean many women who once needed a mastectomy can keep their breast. <a href=\"~/news/lumpectomy-vs-mastectomy/\">Read the full article</a>." if any(p["slug"] == "lumpectomy-vs-mastectomy" for p in POSTS) else "It depends on the size of the cancer relative to the breast, where it lies, whether there is more than one area, genetics and, above all, the patient&rsquo;s own wishes. Oncoplastic techniques mean many women who once needed a mastectomy can keep their breast. <a href=\"~/procedures/breast-cancer-surgery/\">Breast cancer surgery</a>."),
        ("What symptoms should I look for, and how should I check?", "Not only a lump: dimpling of the skin, a change in size or shape, a newly inverted nipple, a rash on the nipple or bloodstained discharge, and persistent pain in one place. Know what is normal for you and have any change checked. <a href=\"~/news/breast-lump-when-to-see-a-specialist/\">When to see a specialist</a>."),
        ("Is breast cancer rising in young women?", "UK figures show breast cancer has become more common in younger women in recent decades, although it remains far less common under 40. No woman should be told she is too young to have a new symptom assessed."),
        ("Does everyone need radiotherapy?", "No. Radiotherapy is standard after most breast conserving surgery and is used selectively after mastectomy. Some patients at lower risk can safely avoid it. The decision is made by the multidisciplinary team, based on the biology and stage of the cancer."),
        ("What is triple negative breast cancer?", "A type of breast cancer without oestrogen, progesterone or HER2 receptors, so hormone and HER2 treatments do not work against it. It is often treated with chemotherapy, sometimes with immunotherapy, before surgery, and many patients respond well to modern treatment."),
    ]
    body = page_head(crumbs, f"Podcast · {P['date_label']}", "Five questions about breast cancer, answered by a surgeon",
                     f"Mr Ullah on <em>{P['show']}</em>, season {P['season']}, episode {P['episode']}. {P['summary']}",
                     actions=f'<a class="btn" href="#watch">Watch</a><a class="btn line" href="{P["spotify"]}" target="_blank" rel="noopener">Spotify</a><a class="btn line" href="{P["apple"]}" target="_blank" rel="noopener">Apple Podcasts</a>') + \
        f'<section class="section" id="watch"><div class="wrap railed"><div class="rail"><span class="label">Episode</span><span class="label">{P["duration_label"]}</span></div><div>{video()}<p class="stone small mt-1">Hosted by {P["host"]}. The video loads from YouTube when you press play.</p></div></div></section>' + \
        faq_section(qa, "The five questions", "In this episode") + \
        railed("About the show", f'<p class="lede"><em>Everything Changed</em> is {P["host"]}&rsquo;s podcast about life during and after breast cancer. In this live episode she talks to the surgeon who diagnosed her and later performed her double mastectomy and reconstruction.</p>', cls="section rule") + \
        f'<section class="section blush"><div class="wrap railed"><div class="rail"><span class="label">In Bengali</span><span class="label">TV3 Bangla and YouTube</span></div><div><h2>Health advice in Bengali</h2><p class="lede mt-1">Mr Ullah presents health talks in Bengali for TV3 Bangla and on his own YouTube channel, from breast self-examination to questions about COVID-19.</p><div class="mt-3">{journal_list(VIDEO_ENTRIES)}</div><p class="mt-3"><a class="more" href="{C.YOUTUBE_CHANNEL}" target="_blank" rel="noopener">His YouTube channel</a></p></div></div></section>'
    ep = {"@context": "https://schema.org", "@type": "PodcastEpisode", "name": P["title"], "url": P["spotify"], "datePublished": P["date"],
          "timeRequired": P["duration"], "episodeNumber": P["episode"], "description": P["summary"],
          "partOfSeries": {"@type": "PodcastSeries", "name": P["show"]}, "actor": [{"@type": "Person", "name": P["host"]}, PHYSICIAN_REF],
          "associatedMedia": {"@type": "MediaObject", "contentUrl": P["spotify"]}}
    vid = {"@context": "https://schema.org", "@type": "VideoObject", "name": f"{P['title']}, {P['show']}", "description": P["summary"],
           "thumbnailUrl": f"https://i.ytimg.com/vi/{P['youtube']}/hqdefault.jpg", "uploadDate": P["date"], "duration": P["duration"],
           "embedUrl": f"https://www.youtube.com/embed/{P['youtube']}", "contentUrl": f"https://www.youtube.com/watch?v={P['youtube']}"}
    render(path, title="Podcast & Videos | Breast Surgeon Mr Zaker Ullah FRCS",
           desc="Breast surgeon Mr Zaker Ullah on the Everything Changed podcast with Rosie Fawehimi, and his Bengali health talks for TV3 Bangla and YouTube.",
           body=body, nav=NAV, active="about", priority="0.8", schema=[ep, vid, crumbs_schema(crumbs), faq_schema(qa)])


# ================================================================== JOURNAL
def build_news():
    crumbs = [("Home", ""), ("Journal", "news/")]
    body = page_head(crumbs, "Journal", "The journal",
                     "Plain English guides to breast symptoms, diagnosis, surgery and recovery, written by Mr Ullah, alongside his health talks in Bengali.") + \
        railed(f"{len(ENTRIES)} articles and videos", journal_list(ENTRIES))
    render("news/", title="Breast Health Articles & Advice | Mr Zaker Ullah",
           desc="Articles by London consultant breast surgeon Mr Zaker Ullah FRCS on breast lumps, breast cancer, oncoplastic surgery, reconstruction, gynaecomastia and private care.",
           body=body, nav=NAV, active="news", priority="0.8",
           schema=[crumbs_schema(crumbs), {"@context": "https://schema.org", "@type": "Blog", "name": "Journal of Mr Zaker Ullah", "url": SITE + "/news/", "author": PHYSICIAN_REF,
                                           "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/news/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]}])

    for p in POSTS:
        path = f"news/{p['slug']}/"
        crumbs = [("Home", ""), ("Journal", "news/"), (p["title"], path)]
        date_label = p["date_obj"].strftime("%-d %B %Y")
        reviewed = datetime.date.fromisoformat(p.get("reviewed", p["date"])).strftime("%-d %B %Y")
        html, toc = with_ids(p["html"])
        faq = faq_html([(q, a.replace("<p>", "").replace("</p>", "||").rstrip("|")) for q, a in p["faqs"]]) if p["faqs"] else ""
        rel = "".join(f'<li><a href="~/procedures/{s}/">{PROC[s]["nav"]}</a></li>' for s in p["related"] if s in PROC)
        more = [x for x in POSTS if x is not p][:3]
        body = f'''<article>{page_head(crumbs, f'{escape(p["category"])}', escape(p["title"]), escape(p["description"]), meta=[("Published", f'<time datetime="{p["date"]}">{date_label}</time>'), ("Reading time", f'{p["minutes"]} minutes'), ("Medically reviewed", reviewed)])}
<section class="section"><div class="wrap article">
  <div class="rail"><span class="label">Contents</span>{toc_html(toc, [("questions", "Questions")] if faq else [])}</div>
  <div><div class="byline"><img src="~/assets/img/zu-head-400.webp" alt="" width="400" height="400" loading="lazy"><span>By <a href="~/biography/">{NAME} FRCS</a>, Consultant Oncoplastic Breast Surgeon.</span></div>
    <div class="prose">{html}{f'<h2 id="questions">Questions</h2>{faq}' if faq else ""}
    <p class="note">This article is general information and not medical advice. If you have a breast symptom, arrange an assessment through your GP or a <a href="~/booking/">specialist clinic</a>. In an emergency, call 999.</p></div></div>
  <aside class="aside">{appt_aside()}{f'<div class="block"><span class="label">Treatments</span><ul>{rel}</ul></div>' if rel else ""}<div class="block"><span class="label">Further reading</span><ul><li><a href="~/reviews/">Patient reviews</a></li><li><a href="~/podcast/">The podcast</a></li><li><a href="~/your-visit/">Your first visit</a></li></ul></div></aside>
</div></section></article>
{railed("Further reading", journal_list(more), cls="section rule") if more else ""}'''
        posting = {"@context": "https://schema.org", "@type": ["BlogPosting", "MedicalWebPage"], "headline": p["title"], "description": p["description"],
                   "url": f"{SITE}/{path}", "mainEntityOfPage": f"{SITE}/{path}", "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
                   "lastReviewed": p.get("reviewed", p["date"]), "author": {"@type": "Person", "@id": SITE + "/#physician", "name": NAME, "url": SITE + "/biography/"},
                   "reviewedBy": PHYSICIAN_REF, "publisher": PHYSICIAN_REF, "image": SITE + "/assets/img/og-card.png", "keywords": p["keyword"],
                   "articleSection": p["category"], "wordCount": p["words"], "inLanguage": "en-GB"}
        schema = [posting, crumbs_schema(crumbs)] + ([faq_schema(p["faqs_text"])] if p["faqs"] else [])
        render(path, title=p["title"] if len(p["title"]) > 44 else f'{p["title"]} | Mr Zaker Ullah', desc=p["description"], body=body,
               nav=NAV, active="news", og_type="article", priority="0.7", schema=schema)


def build_videos():
    for v in C.VIDEOS:
        path = f"news/{v['slug']}/"
        crumbs = [("Home", ""), ("Journal", "news/"), (v["title"], path)]
        d = datetime.date.fromisoformat(v["date"])
        body = page_head(crumbs, f"Video, in {v['lang']}", escape(v["title"]), escape(v["desc"]),
                         meta=[("Published", d.strftime("%-d %B %Y")), ("Language", v["lang"]), ("Source", v["by"])]) + \
            f'<section class="section"><div class="wrap railed"><div class="rail"><span class="label">Watch</span></div><div style="max-width:56rem">{video(v["id"], v["title"])}<p class="stone small mt-1">The video loads from YouTube when you press play. <a class="more" href="{C.YOUTUBE_CHANNEL}" target="_blank" rel="noopener">More on YouTube</a></p></div></div></section>' + \
            railed("More videos", journal_list([x for x in VIDEO_ENTRIES if x["slug"] != v["slug"]]), cls="section rule")
        schema = [{"@context": "https://schema.org", "@type": "VideoObject", "name": v["title"], "description": v["desc"], "inLanguage": "bn",
                   "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg", "uploadDate": v["date"],
                   "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "contentUrl": f"https://www.youtube.com/watch?v={v['id']}", "actor": PHYSICIAN_REF},
                  crumbs_schema(crumbs)]
        render(path, title=f"{v['title']} | Mr Zaker Ullah"[:70], desc=v["desc"][:160], body=body, nav=NAV, active="news", priority="0.5", schema=schema)
    # He does not offer augmentation; keep the old URL from 404ing.
    render("procedures/breast-augmentation/", title="Treatments", desc="This page has moved.", nav=NAV, noindex=True,
           extra_head='<meta http-equiv="refresh" content="0; url=../">',
           body='<section class="section"><div class="wrap"><p>This page has moved. <a href="~/procedures/">See all treatments</a>.</p></div></section>')


# ================================================================== BOOKING
def build_booking():
    path = "booking/"
    crumbs = [("Home", ""), ("Book a consultation", path)]
    opts = "".join(f"<option>{l['name']}</option>" for l in C.LOCATIONS)
    procs = "".join(f"<option>{p['nav']}</option>" for p in C.PROCEDURES)
    body = page_head(crumbs, "Appointments", "Book a consultation",
                     "Telephone Ms Juliet Willes, Mr Ullah&rsquo;s private secretary, or send an enquiry and the team will call you back. New breast symptoms are given priority, and video or telephone consultations can usually be arranged within 24 to 48 hours.",
                     meta=[("Telephone", f'<a href="tel:{C.SEC_TEL}">{C.SEC_PHONE}</a>'), ("Email", f'<a href="mailto:{C.SEC_EMAIL}">{C.SEC_EMAIL}</a>'), ("Rapid access", "Tuesday afternoons at The Holly")]) + f'''
<section class="section"><div class="wrap railed"><div class="rail"><span class="label">Enquiry</span></div><div class="cols-2">
  <form class="form" id="enquiry" data-to="{C.SEC_EMAIL}">
    <div class="row"><label>Name<input name="name" required autocomplete="name"></label><label>Telephone<input name="phone" type="tel" required autocomplete="tel"></label></div>
    <div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Clinic<select name="clinic">{opts}<option>No preference</option></select></label></div>
    <div class="row"><label>Reason<select name="reason">{procs}<option>Second opinion</option><option>Other</option></select></label><label>Funding<select name="funding"><option>Private medical insurance</option><option>Self-funding</option><option>Not yet decided</option></select></label></div>
    <label>Anything else (optional)<textarea name="message" placeholder="For example, the best time to call, or your insurer"></textarea></label>
    <label class="consent"><input type="checkbox" required> I agree to be contacted about this enquiry by Mr Ullah&rsquo;s private practice.</label>
    <button class="btn" type="submit">Send enquiry</button>
  </form>
  <div>
    <p class="stone">Your enquiry opens in your email application, addressed to Mr Ullah&rsquo;s private secretary. Please keep medical detail for the consultation.</p>
    <dl class="facts mt-2"><div><dt>Insured</dt><dd>A GP referral and pre-authorisation number are needed by most insurers. <a href="~/fees-and-insurance/">Fees and insurance</a></dd></div>
    <div><dt>Self-funding</dt><dd>No referral is needed. The hospital confirms fees in advance.</dd></div>
    <div><dt>Your visit</dt><dd>What happens and what to bring. <a href="~/your-visit/">Your first visit</a></dd></div>
    <div><dt>Urgent</dt><dd>If you are acutely unwell, call 999 or go to your nearest emergency department.</dd></div></dl>
  </div>
</div></div></section>
{railed("Clinics", clinic_cols(), cls="section rule")}'''
    render(path, title="Book a Private Breast Surgeon in London | Mr Zaker Ullah",
           desc=f"Book a private consultation with breast surgeon Mr Zaker Ullah FRCS at Harley Street, St Bartholomew's or The Holly, Buckhurst Hill. Telephone {C.SEC_PHONE}.",
           body=body, nav=NAV, active="patients", priority="0.9", schema=[crumbs_schema(crumbs)], band=False)


def build_404():
    body = '''<section class="section notfound"><div class="wrap railed"><div class="rail"><span class="label">Error 404</span></div><div><h1>This page could not be found</h1>
<p class="lede">It may have moved when the website was redesigned.</p><div class="actions mt-2"><a class="btn" href="/">Home</a><a class="btn line" href="/procedures/">Treatments</a><a class="btn line" href="/booking/">Book</a></div></div></div></section>'''
    render("404.html", title="Page not found | Mr Zaker Ullah", desc="Page not found.", body=body, nav=NAV, noindex=True)


# ================================================================== FILES
def build_files():
    from html import escape as e
    urls = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{p}</priority></url>\n" for u, p in SITEMAP)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /content/\n\nSitemap: {SITE}/sitemap.xml\n")
    items = "".join(f"<item><title>{e(p['title'])}</title><link>{SITE}/news/{p['slug']}/</link><guid>{SITE}/news/{p['slug']}/</guid><pubDate>{datetime.datetime.combine(p['date_obj'], datetime.time(8)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{e(p['description'])}</description></item>" for p in POSTS)
    open(os.path.join(ROOT, "feed.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Journal of Mr Zaker Ullah</title><link>{SITE}/news/</link><description>Articles by consultant breast surgeon Mr Md Zaker Ullah FRCS</description><language>en-gb</language>{items}</channel></rss>\n')
    llms = [f"# {NAME} FRCS, Consultant Oncoplastic Breast Surgeon, London and Essex", "",
            f"> {PHYSICIAN['description']} GMC 4368515. Rated {C.IWGC_RATING} out of 5 on iWantGreatCare (100% five-star). Bupa Platinum consultant, fee-assured, in Bupa's Open Referral network. Private secretary: {C.SEC_PHONE}.", "",
            "## Key pages", f"- [Biography]({SITE}/biography/)", f"- [Book a consultation]({SITE}/booking/)", f"- [Your first visit]({SITE}/your-visit/)", f"- [Fees and insurance]({SITE}/fees-and-insurance/)",
            f"- [Questions answered]({SITE}/faqs/)", f"- [Reviews]({SITE}/reviews/)", f"- [Podcast]({SITE}/podcast/)", f"- [Second opinions]({SITE}/second-opinion/)", "", "## Treatments"] + \
           [f"- [{p['nav']}]({SITE}/procedures/{p['slug']}/): {p['summary']}" for p in C.PROCEDURES] + ["", "## Clinics"] + \
           [f"- [{l['name']}]({SITE}/locations/{l['slug']}/): {loc_address(l)}" for l in C.LOCATIONS] + ["", "## Journal"] + [f"- [{p['title']}]({SITE}/news/{p['slug']}/)" for p in POSTS]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(llms) + "\n")


if __name__ == "__main__":
    build_home(); build_about(); build_procedures(); build_second_opinion(); build_locations(); build_patient_pages()
    build_reviews(); build_podcast(); build_news(); build_videos(); build_booking(); build_404(); build_files()
    print(f"Built {len(SITEMAP)} indexable pages · {len(POSTS)} posts live · {len(SCHEDULED)} scheduled")
    for s in SCHEDULED:
        print(f"  scheduled {s['date']}  {s['slug']}")
