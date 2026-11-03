"""Build the whole site:  python3 _build/build.py

Writes HTML into the repo root (which is the deployable site). Blog posts in
content/blog/*.md with a future `date` are skipped until that date — the
daily GitHub Action rebuild publishes them automatically.
"""
import datetime
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402
import md  # noqa: E402
from layout import (ARROW, GO, NAME, PHYSICIAN_REF, PLAY, POSTNOM, ROOT, SHORT, SITE, SITEMAP,  # noqa: E402
                  crumbs_html, crumbs_schema, faq_html, faq_schema, picture, render, stars, strip_tags)

TODAY = datetime.date.fromisoformat(os.environ.get("BUILD_DATE", datetime.date.today().isoformat()))
NAV = {"procedures": C.PROCEDURES, "locations": C.LOCATIONS, "phone_label": C.PHONE_LABEL,
       "phone_tel": C.PHONE_TEL, "iwgc": C.IWGC}
PROC = {p["slug"]: p for p in C.PROCEDURES}
POSTS = [p for p in md.load_posts(os.path.join(ROOT, "content", "blog"), TODAY) if p["published"]]
SCHEDULED = [p for p in md.load_posts(os.path.join(ROOT, "content", "blog"), TODAY) if not p["published"]]

PORTRAIT = lambda lazy=True: picture("holly-portrait", "Mr Md Zaker Ullah, consultant breast surgeon, outside Nuffield Health The Holly Hospital", "(min-width: 62rem) 40vw, 92vw", [640, 1000, 1400], 1021, 1277, lazy=lazy)
WIDE = picture("holly-wide", "Mr Md Zaker Ullah in surgical scrubs outside The Holly Hospital, Buckhurst Hill", "(min-width: 62rem) 50vw, 92vw", [1200, 1800, 2500], 2500, 1277)


def loc_address(l):
    return f'{l["street"]}, {l["locality"]}, {l["postcode"]}'


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
    "honorificPrefix": "Mr", "honorificSuffix": "MBBS FRCSEd FRCS (Gen. Surg.)",
    "description": "Consultant oncoplastic breast and general surgeon in London and Essex. Clinical Lead of the Whipps Cross Breast Unit, Barts Health NHS Trust. Private practice at The Harley Street Clinic, Nuffield Health at St Bartholomew's and Nuffield Health The Holly Hospital.",
    "url": SITE + "/", "image": SITE + "/assets/img/holly-portrait-1000.jpg", "logo": SITE + "/assets/img/holly-head-600.jpg",
    "telephone": C.SEC_TEL, "email": C.SEC_EMAIL, "priceRange": "££££",
    "address": {"@type": "PostalAddress", "streetAddress": "High Road", "addressLocality": "Buckhurst Hill", "addressRegion": "Essex", "postalCode": "IG9 5HX", "addressCountry": "GB"},
    "areaServed": ["London", "Essex", "Hertfordshire", "Central London", "East London", "North East London", "City of London"],
    "medicalSpecialty": ["Oncologic", "Surgical", "PlasticSurgery"],
    "isAcceptingNewPatients": True,
    "knowsLanguage": ["en-GB", "bn"],
    "identifier": {"@type": "PropertyValue", "propertyID": "GMC", "value": "4368515"},
    "hasCredential": [
        {"@type": "EducationalOccupationalCredential", "name": "MBBS", "credentialCategory": "degree"},
        {"@type": "EducationalOccupationalCredential", "name": "FRCSEd", "recognizedBy": {"@type": "Organization", "name": "Royal College of Surgeons of Edinburgh"}},
        {"@type": "EducationalOccupationalCredential", "name": "FRCS (General Surgery)", "recognizedBy": {"@type": "Organization", "name": "Intercollegiate Specialty Board"}},
    ],
    "memberOf": [{"@type": "Organization", "name": n} for n in ["Association of Breast Surgery", "Association of Surgeons of Great Britain and Ireland", "European Association for Endoscopic Surgery", "Royal College of Surgeons of Edinburgh"]],
    "award": "European Association for Endoscopic Surgery — best video presentation (2003)",
    "hospitalAffiliation": [hospital_schema(l) for l in C.LOCATIONS] + [{"@type": "Hospital", "name": "Whipps Cross University Hospital, Barts Health NHS Trust", "address": {"@type": "PostalAddress", "streetAddress": "Whipps Cross Road", "addressLocality": "London", "postalCode": "E11 1NR", "addressCountry": "GB"}}],
    "availableService": [{"@type": "MedicalProcedure", "name": strip_tags(p["nav"]), "url": f"{SITE}/procedures/{p['slug']}/"} for p in C.PROCEDURES],
    "sameAs": [C.IWGC, "https://www.nuffieldhealth.com/consultants/mr-md-zaker-ullah", "https://www.doctify.com/uk/specialist/mr-md-z-ullah", "https://www.topdoctors.co.uk/doctor/zaker-ullah/", "https://www.finder.bupa.co.uk/Consultant/view/192096/mr_md_z_ullah", "https://whippscrosswf.com/people/mr-md-zaker-ullah/"],
}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": f"{NAME} — Consultant Breast Surgeon, London", "publisher": PHYSICIAN_REF, "inLanguage": "en-GB"}


def head(crumbs, eyebrow, h1, lede, actions="", aside=""):
    grid_open, grid_close = ('<div class="head-grid"><div>', f'</div><div class="head-aside">{aside}</div></div>') if aside else ("", "")
    return f'''<section class="page-head dark"><div class="wrap">{crumbs_html(crumbs)}{grid_open}
<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lede">{lede}</p>{f'<div class="actions">{actions}</div>' if actions else ""}{grid_close}
</div></section>'''


def review_cards(items, lead_first=True):
    out = []
    for i, (q, d, where) in enumerate(items):
        cls = " lead" if (i == 0 and lead_first) else ""
        out.append(f'<figure class="quote{cls}">{stars()}<blockquote>{escape(q)}</blockquote><figcaption><span>Verified patient · {where}</span><span>{d}</span></figcaption></figure>')
    return f'<div class="quotes">{"".join(out)}</div>'


def rating_panel():
    return f'''<div class="rating-panel"><div class="rating-big">{C.IWGC_RATING}<small>/5</small></div>
<div class="rating-meta">{stars(5, "Rated 5 out of 5")}<p>From {C.IWGC_COUNT} independent, verified reviews on iWantGreatCare — every one of them five stars.</p></div>
<a class="iwgc-badge" href="{C.IWGC}" target="_blank" rel="noopener"><i>iWGC</i>Read all reviews on iWantGreatCare</a></div>'''


def video_facade(caption=True):
    P = C.PODCAST
    cap = f'<span class="vcap">{P["show"]} · S{P["season"]} E{P["episode"]}</span>' if caption else ""
    return f'''<div class="video" data-yt="{P["youtube"]}"><img src="https://i.ytimg.com/vi/{P["youtube"]}/hqdefault.jpg" alt="{escape(P["title"])} — {P["show"]}" width="480" height="360" loading="lazy">
<button class="play" type="button" aria-label="Play episode: {escape(P["title"])}"><span>{PLAY}</span></button>{cap}</div>'''


def proc_cards(slugs=None, feature_first=True):
    items = [PROC[s] for s in slugs] if slugs else C.PROCEDURES
    out = []
    for i, p in enumerate(items):
        cls = " feature span-2" if (feature_first and i == 0 and not slugs) else ""
        tags = "".join(f"<span>{t}</span>" for t in p["tags"])
        out.append(f'<a class="card{cls}" href="~/procedures/{p["slug"]}/"><span class="num">{C.PROCEDURES.index(p) + 1:02d}</span>{GO}<h3>{p["nav"]}</h3><p>{strip_tags(p["lede"]).split(". ")[0]}.</p><div class="tags">{tags}</div></a>')
    return f'<div class="cards">{"".join(out)}</div>'


def loc_cards(with_nhs=True):
    out = []
    for l in C.LOCATIONS:
        tel = f'<a class="tel" href="tel:{l["tel"]}">{l["phone"]}</a>' if l.get("phone") else f'<a class="tel" href="tel:{C.SEC_TEL}">{C.SEC_PHONE}</a>'
        out.append(f'''<article class="loc"><p class="area">{l["area"]}</p><h3>{l["name"]}</h3><address>{loc_address(l)}</address><p>{l["travel"]}</p>
<div class="loc-actions">{tel}<a class="link-arrow" href="~/locations/{l["slug"]}/">Clinic details {ARROW}</a></div></article>''')
    if with_nhs:
        out.append(f'''<article class="loc nhs"><p class="area">NHS · Leytonstone, London E11</p><h3>Whipps Cross University Hospital</h3><address>Whipps Cross Road, London E11 1NR</address><p>Mr Ullah is Clinical Lead of the Breast Unit at Whipps Cross, part of Barts Health NHS Trust. NHS referrals are made through your GP in the usual way.</p>
<div class="loc-actions"><a class="link-arrow" href="https://www.bartshealth.nhs.uk/find-a-consultant/contact/md-zaker-ullah-301/?consultant=301" target="_blank" rel="noopener">Barts Health profile {ARROW}</a></div></article>''')
    return f'<div class="locs">{"".join(out)}</div>'


def insurers():
    return '<div class="insurers">' + "".join(f"<span>{i}</span>" for i in C.INSURERS) + "</div>"


def post_cards(posts):
    out = []
    for p in posts:
        out.append(f'''<a class="post" href="~/news/{p["slug"]}/"><span class="meta">{escape(p["category"])} · {p["minutes"]} min read</span><h3>{escape(p["title"])}</h3><p>{escape(p["description"])}</p><span class="link-arrow">Read article {ARROW}</span></a>''')
    return f'<div class="posts">{"".join(out)}</div>'


def faq_block(faqs, title="Questions patients <em>ask first</em>", intro=""):
    return f'''<section class="section rule-top"><div class="wrap faq-grid"><div><p class="eyebrow">FAQ</p><h2>{title}</h2>{f'<p class="lede mt-1">{intro}</p>' if intro else ""}</div>{faq_html(faqs)}</div></section>'''


# =================================================================== HOME
HOME_FAQS = [
    ("How quickly can I see Mr Ullah privately?", "Patients with new breast symptoms are prioritised, and appointments can often be arranged within days. At The Holly, Mr Ullah runs a Rapid Access Breast Clinic on Tuesday afternoons, where examination, imaging and biopsy can happen at a single visit."),
    ("Do I need a GP referral?", "If you are using private medical insurance, most insurers ask for a GP referral before authorising a specialist appointment — check with your insurer first. Self-funding patients can usually book directly."),
    ("Which insurers is Mr Ullah recognised by?", "Mr Ullah is recognised by the major UK private medical insurers, including Bupa, Bupa Global, AXA Health, Aviva, Vitality, WPA, Cigna, Healix and Health-on-Line, and is fee-assured with the main insurers — so you should not face a shortfall for his fees."),
    ("Where does Mr Ullah see private patients?", "At The Harley Street Clinic (London W1), Nuffield Health at St Bartholomew's (City of London, EC1) and Nuffield Health The Holly Hospital (Buckhurst Hill, Essex IG9). He also leads the NHS breast unit at Whipps Cross University Hospital."),
    ("Why is a surgeon called “Mr” rather than “Dr”?", "It is a British surgical tradition. On gaining a fellowship of a Royal College of Surgeons, surgeons revert to Mr, Miss, Ms or Mrs — a mark of the surgical qualification itself. Mr Ullah holds the FRCSEd and the FRCS in General Surgery."),
    ("Does Mr Ullah see men?", "Yes. Mr Ullah assesses and treats male breast conditions, including gynaecomastia and new lumps in the male breast, as well as a full general surgical practice for hernias and gallstones."),
]


def build_home():
    P = C.PODCAST
    marquee_items = "".join(f"<span>{x}</span>" for x in C.INSURERS + ["The Harley Street Clinic", "Nuffield Health", "Barts Health NHS Trust"]) * 2
    body = f'''
<section class="hero dark"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="pill"><b>New</b> Mr Ullah on the <em>Everything Changed</em> podcast &rarr; <a href="~/podcast/" style="color:inherit">Listen</a></span>
      <p class="eyebrow">Consultant Oncoplastic Breast Surgeon · London &amp; Essex</p>
      <h1>Expert breast surgery in London, <em>with the whole of you in mind.</em></h1>
      <p class="lede">Mr Md Zaker Ullah FRCS has been a doctor since 1987 and leads the Breast Unit at Whipps Cross University Hospital. Privately, he sees patients on Harley Street, in the City and in Buckhurst Hill — from a first worrying lump through to cancer surgery and reconstruction.</p>
      <div class="actions"><a class="btn gold" href="~/booking/">Book a consultation {ARROW}</a><a class="btn ghost" href="~/procedures/">Explore treatments</a></div>
    </div>
    <div class="hero-media">
      {PORTRAIT(lazy=False)}
      <a class="float-card fc-rating" href="~/reviews/"><span class="fc-k">{C.IWGC_RATING}</span><span class="fc-v">{stars()}<strong>{C.IWGC_COUNT} verified reviews</strong>iWantGreatCare</span></a>
      <div class="float-card fc-role"><span class="fc-v"><strong>Clinical Lead</strong>Whipps Cross Breast Unit, Barts Health NHS Trust</span></div>
    </div>
  </div>
  <div class="hero-trust">
    <div><span class="k">Since 1987</span><span class="v">Qualified in medicine; UK surgical training from 1993</span></div>
    <div><span class="k">FRCS <sup>(Gen. Surg.)</sup></span><span class="v">FRCSEd 1996 · FRCS General Surgery 2009</span></div>
    <div><span class="k">5.0 <sup>★</sup></span><span class="v">{C.IWGC_COUNT} independent reviews, all five-star</span></div>
    <div><span class="k">Fee-assured</span><span class="v">With Bupa, AXA Health, Aviva, Vitality &amp; more</span></div>
  </div>
</div></section>

<div class="marquee" aria-label="Recognised by"><div class="wrap row"><span class="label">Recognised by</span><div class="viewport"><div class="track">{marquee_items}</div></div></div></div>

<section class="section"><div class="wrap">
  <p class="eyebrow">The approach</p>
  <p class="statement reveal">Oncoplastic surgery means planning every operation twice — <em>once for the cancer, and once for the person</em> who lives with the result.</p>
  <div class="sig"><img src="~/assets/img/holly-head-600.webp" alt="" width="600" height="600" loading="lazy"><div><strong>Mr Md Zaker Ullah</strong><span>{POSTNOM}</span></div></div>
  <div class="pillars">
    <div><span class="n">i.</span><h3>Answers in a single visit</h3><p>He introduced the one-stop breast clinic at Whipps Cross. Examination, imaging and biopsy are done together, so you are not left waiting weeks between appointments.</p></div>
    <div><span class="n">ii.</span><h3>Cancer first, appearance never an afterthought</h3><p>Trained at The Royal Marsden, St Mary's and The Royal Free. He combines complete removal of the cancer with plastic-surgical reshaping, reconstruction and symmetry.</p></div>
    <div><span class="n">iii.</span><h3>One surgeon, start to finish</h3><p>The surgeon who examines you is the one who operates and follows you up. Every cancer case also goes to a full multidisciplinary team.</p></div>
  </div>
</div></section>

<section class="section sand"><div class="wrap">
  <div class="head-row"><div><p class="eyebrow">Treatments</p><h2>From a first symptom to <em>reconstruction</em></h2></div><p class="lede">Benign and malignant breast disease, oncoplastic and reconstructive surgery, men's breast health, and keyhole general surgery, all under one consultant.</p></div>
  {proc_cards()}
  <p class="mt-3"><a class="link-arrow" href="~/second-opinion/">Facing a diagnosis? Get a second opinion {ARROW}</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="head-row"><div><p class="eyebrow">Patient reviews</p><h2>In his patients&rsquo; <em>own words</em></h2></div>{rating_panel()}</div>
  {review_cards(C.REVIEWS[:6])}
  <p class="mt-2 center"><a class="btn ghost" href="~/reviews/">More patient reviews {ARROW}</a></p>
</div></section>

<section class="section dark"><div class="wrap pod">
  <div>
    <p class="eyebrow">Podcast · {P["date_label"]}</p>
    <h2>&ldquo;5 breast cancer questions, <em>answered by a surgeon</em>&rdquo;</h2>
    <p class="lede mt-1">{P["summary"]}</p>
    <ol class="episodes">{"".join(f'<li><a href="~/podcast/#q{i + 1}"><span class="ep">Q{i + 1}</span><span class="et">{c}</span><span class="ed">&rarr;</span></a></li>' for i, c in enumerate(P["chapters"]))}</ol>
    <div class="platforms"><a class="btn light sm" href="~/podcast/">Watch &amp; listen</a><a class="btn ghost sm" href="{P["spotify"]}" target="_blank" rel="noopener">Spotify</a><a class="btn ghost sm" href="{P["apple"]}" target="_blank" rel="noopener">Apple Podcasts</a></div>
  </div>
  {video_facade()}
</div></section>

<section class="section"><div class="wrap">
  <div class="head-row"><div><p class="eyebrow">Your first appointment</p><h2>What happens when you <em>book</em></h2></div><p class="lede">Most patients go home from their first visit either reassured or with a clear plan.</p></div>
  <div class="steps four">
    <div class="step"><h3>Book</h3><p>Call the private secretary or send an enquiry. If you are insured, ask your GP for a referral letter and get a pre-authorisation number from your insurer.</p></div>
    <div class="step"><h3>Consult</h3><p>A full history and examination with Mr Ullah himself. There is time to talk, and nothing is rushed.</p></div>
    <div class="step"><h3>Assess</h3><p>Ultrasound, mammogram and biopsy can be done at the same visit where needed. This is the gold-standard “triple assessment”.</p></div>
    <div class="step"><h3>Plan</h3><p>You get results and a written plan. If you need surgery, the same surgeon who examined you performs it.</p></div>
  </div>
</div></section>

<section class="section sand"><div class="wrap">
  <div class="head-row"><div><p class="eyebrow">Clinics</p><h2>Private clinics across <em>London &amp; Essex</em></h2></div><div><p class="lede">He is fee-assured with the major UK insurers, and self-funding patients are equally welcome.</p><div class="mt-2">{insurers()}</div></div></div>
  {loc_cards()}
</div></section>

<section class="section"><div class="wrap split wide-right">
  <figure class="frame-img reveal">{WIDE}<figcaption>Mr Ullah at Nuffield Health The Holly Hospital, Buckhurst Hill</figcaption></figure>
  <div>
    <p class="eyebrow">About Mr Ullah</p>
    <h2>Three decades of surgery, <em>one field of focus</em></h2>
    <div class="prose mt-2"><p>Mr Ullah trained in London&rsquo;s teaching hospitals, including The Royal Marsden, St Mary&rsquo;s and The Royal Free. He has been a consultant at Barts Health NHS Trust since 2012 and leads its breast unit at Whipps Cross. There he introduced the one-stop breast clinic and fat grafting for breast deformities.</p>
    <p>He teaches the next generation of surgeons, directing the Whipps Cross Higher Surgery FRCS course. His keyhole hernia technique won best video at the European Association for Endoscopic Surgery. He consults in English and Bengali.</p></div>
    <p class="mt-2"><a class="link-arrow" href="~/biography/">Full biography {ARROW}</a></p>
  </div>
</div></section>

{f'<section class="section sand"><div class="wrap"><div class="head-row"><div><p class="eyebrow">Insights</p><h2>Clear answers from a <em>breast surgeon</em></h2></div><p class="lede">Plain-English guides to symptoms, diagnosis and treatment, written by Mr Ullah.</p></div>{post_cards(POSTS[:3])}<p class="mt-3"><a class="link-arrow" href="~/news/">All articles {ARROW}</a></p></div></section>' if POSTS else ""}

{faq_block(HOME_FAQS)}
'''
    render("", title="Breast Surgeon London & Essex | Mr Zaker Ullah FRCS",
           desc=f"Mr Md Zaker Ullah FRCS: consultant oncoplastic breast surgeon in London & Essex. Rated 5.0★ by {C.IWGC_COUNT} patients. Rapid breast lump clinics, breast cancer surgery & reconstruction at Harley Street, Barts & The Holly.",
           body=body, nav=NAV, schema=[PHYSICIAN, WEBSITE, faq_schema(HOME_FAQS)], priority="1.0")


# =================================================================== ABOUT
def build_about():
    faqs = [
        ("Why is Mr Ullah “Mr” and not “Dr”?", "In British surgical tradition, doctors who gain a fellowship of a Royal College of Surgeons set aside the title Dr and are addressed as Mr, Miss, Ms or Mrs. Far from being a demotion, it marks the completion of advanced surgical training."),
        ("Does Mr Ullah treat NHS patients?", "Yes. Mr Ullah leads the NHS breast unit at Whipps Cross University Hospital, part of Barts Health NHS Trust. NHS referrals are arranged through your GP; this website covers his private practice."),
        ("Does Mr Ullah speak Bengali?", "Yes. Mr Ullah consults in English and Bengali, and many patients and families value being able to discuss a diagnosis in their first language."),
        ("Can I see Mr Ullah for a second opinion?", "Yes. Many patients see Mr Ullah for a second opinion on a breast diagnosis or a proposed operation. Bring any imaging, biopsy results and clinic letters you have. <a href=\"~/second-opinion/\">Read more about second opinions</a>."),
    ]
    body = head([("Home", ""), ("About", "biography/")], "About Mr Ullah", "Three decades of surgery, <em>one field of focus</em>",
                f"{NAME} {POSTNOM} is a Consultant Oncoplastic Breast and General Surgeon at Barts Health NHS Trust and Clinical Lead of the Whipps Cross Breast Unit.",
                actions=f'<a class="btn gold" href="~/booking/">Book a consultation {ARROW}</a>') + f'''
<section class="section"><div class="wrap split wide-left top">
  <div class="prose">
    <p class="lead-p">Mr Ullah qualified in medicine in 1987 and began surgical training in the United Kingdom in 1993. He trained through the North East Thames Deanery, with higher surgical posts at <strong>The Royal Marsden</strong>, Europe&rsquo;s largest specialist cancer centre, and at <strong>St Mary&rsquo;s</strong>, <strong>The Royal Free</strong> and Broomfield hospitals. This is where he developed his specialist interest in oncoplastic breast surgery.</p>
    <h2>Consultant practice</h2>
    <p>Appointed a consultant at <strong>Barts Health NHS Trust in 2012</strong>, Mr Ullah is Clinical Lead of the Breast Unit at Whipps Cross University Hospital. He introduced the hospital&rsquo;s <strong>one-stop breast clinic</strong>, where patients with new breast symptoms are examined, imaged and biopsied in a single visit instead of over weeks of separate appointments. He also introduced <strong>fat grafting</strong> there for breast deformities.</p>
    <p>His oncoplastic practice covers the full range of modern breast surgery. That includes breast-conserving cancer surgery, mastectomy, implant-based reconstruction, latissimus dorsi, chest-wall perforator and Grisotti flap reconstruction, and therapeutic mammoplasty. He also performs fat grafting, nipple reconstruction, risk-reducing surgery for BRCA carriers, and reduction and augmentation for symmetry. In general surgery he keeps a laparoscopic practice covering gallstones, hernia repair and appendicectomy.</p>
    <h2>Teaching &amp; research</h2>
    <p>Mr Ullah is a clinical and educational supervisor to junior surgeons and serves as educational lead. He directs the <strong>Whipps Cross Higher Surgery FRCS course</strong>, which prepares senior trainees for the fellowship examination of the Royal Colleges of Surgeons. He also gives regular educational talks to local GPs.</p>
    <p>His keyhole hernia repair technique, using a glove-balloon, won <strong>best video presentation at the European Association for Endoscopic Surgery</strong> in 2003. He has published peer-reviewed research on oncoplastic reconstruction, laparoscopic hernia repair, breast cancer in Asian populations and diagnostic laparoscopy.</p>
    <h2>Beyond the clinic</h2>
    <p>Mr Ullah consults in English and Bengali. He is a trustee of Planetary Health Academia, a consortium of doctors of Bangladeshi heritage, and speaks at international cancer meetings. In October 2026 he joined breast cancer survivor Rosie Fawehimi on her podcast <a href="~/podcast/"><em>Everything Changed</em></a> to answer the questions patients ask most.</p>
  </div>
  <aside>
    <figure class="frame-img">{PORTRAIT()}<figcaption>Mr Ullah at The Holly, Buckhurst Hill</figcaption></figure>
    <dl class="facts mt-3">
      <div><dt>Qualifications</dt><dd>MBBS (1987) · FRCSEd (1996) · FRCS General Surgery (2009)</dd></div>
      <div><dt>GMC</dt><dd><a href="https://www.gmc-uk.org/registrants/4368515" target="_blank" rel="noopener">No. 4368515</a>, on the Specialist Register</dd></div>
      <div><dt>NHS</dt><dd>Consultant, Barts Health NHS Trust, since 2012; Clinical Lead, Whipps Cross Breast Unit</dd></div>
      <div><dt>Members of</dt><dd>Association of Breast Surgery · ASGBI · European Association for Endoscopic Surgery · RCS Edinburgh</dd></div>
      <div><dt>Languages</dt><dd>English, Bengali</dd></div>
    </dl>
  </aside>
</div></section>
<section class="section dark"><div class="wrap">
  <p class="eyebrow">Career</p><h2>A career built in <em>London&rsquo;s hospitals</em></h2>
  <div class="split top mt-3"><ol class="timeline">
    <li><span class="yr">1987</span><h4>Qualifies in medicine (MBBS)</h4><p>Begins a career that now spans almost four decades.</p></li>
    <li><span class="yr">1993</span><h4>UK surgical training begins</h4><p>North East Thames Deanery rotation through London teaching and district general hospitals.</p></li>
    <li><span class="yr">1996</span><h4>Fellow of the Royal College of Surgeons of Edinburgh</h4><p>FRCSEd.</p></li>
    <li><span class="yr">2003</span><h4>European award</h4><p>Best video presentation, European Association for Endoscopic Surgery, for a new keyhole hernia repair technique.</p></li>
  </ol><ol class="timeline">
    <li><span class="yr">2009</span><h4>FRCS in General Surgery</h4><p>Intercollegiate specialty fellowship, after higher training including The Royal Marsden, St Mary&rsquo;s and The Royal Free.</p></li>
    <li><span class="yr">2012</span><h4>Consultant, Barts Health NHS Trust</h4><p>Oncoplastic breast &amp; general surgeon at Whipps Cross University Hospital.</p></li>
    <li><span class="yr">Today</span><h4>Clinical Lead, Whipps Cross Breast Unit</h4><p>Leads the unit, directs the FRCS course and sees private patients at Harley Street, Barts and The Holly.</p></li>
  </ol></div>
</div></section>
{faq_block(faqs, "About <em>Mr Ullah</em>")}'''
    render("biography/", title="About Mr Md Zaker Ullah FRCS | Consultant Breast Surgeon, London",
           desc="Biography of Mr Md Zaker Ullah FRCS: Royal Marsden-trained oncoplastic breast surgeon, Barts Health consultant since 2012 and Clinical Lead of the Whipps Cross Breast Unit. Qualifications, GMC 4368515, awards.",
           body=body, nav=NAV, active="about", priority="0.9",
           schema=[PHYSICIAN, {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": PHYSICIAN_REF, "dateModified": TODAY.isoformat()}, crumbs_schema([("Home", ""), ("About", "biography/")]), faq_schema(faqs)])


# =================================================================== PROCEDURES
def medical_page_schema(path, name, desc):
    return {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": f"{SITE}/{path}", "name": name, "description": desc,
            "inLanguage": "en-GB", "lastReviewed": TODAY.isoformat(), "reviewedBy": PHYSICIAN_REF, "author": PHYSICIAN_REF,
            "audience": {"@type": "Patient"}, "isPartOf": {"@id": SITE + "/#website"}}


def build_procedures():
    body = head([("Home", ""), ("Treatments", "procedures/")], "Treatments", "Areas of <em>practice</em>",
                "Diagnosis and surgical treatment of breast disease, both benign and malignant, with oncoplastic and reconstructive surgery and a laparoscopic general surgical practice.") + f'''
<section class="section"><div class="wrap">{proc_cards()}
<div class="note mt-3" style="max-width:66ch">Not sure which page fits your situation? Start with a consultation. The right operation, and whether to operate at all, comes from the diagnosis.</div></div></section>'''
    items = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/procedures/{p['slug']}/", "name": strip_tags(p["nav"])} for i, p in enumerate(C.PROCEDURES)]}
    render("procedures/", title="Breast Surgery Treatments London & Essex | Mr Zaker Ullah FRCS",
           desc="Breast and general surgery with Mr Zaker Ullah FRCS in London & Essex: breast lump clinics, breast cancer surgery, reconstruction, reduction, augmentation, fat grafting, gynaecomastia and keyhole hernia & gallbladder surgery.",
           body=body, nav=NAV, active="procedures", priority="0.9", schema=[items, crumbs_schema([("Home", ""), ("Treatments", "procedures/")])])

    for p in C.PROCEDURES:
        path = f"procedures/{p['slug']}/"
        crumbs = [("Home", ""), ("Treatments", "procedures/"), (strip_tags(p["nav"]), path)]
        glance = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["glance"])
        related_posts = [x for x in POSTS if p["slug"] in x["related"]][:3]
        rel_links = "".join(f'<li><a href="~/procedures/{s}/">{PROC[s]["nav"]}</a></li>' for s in p["related"])
        rel_posts = "".join(f'<li><a href="~/news/{x["slug"]}/">{escape(x["title"])}</a></li>' for x in related_posts)
        body = head(crumbs, f"Treatments · {C.PROCEDURES.index(p) + 1:02d}", p["h1"], p["lede"],
                    actions=f'<a class="btn gold" href="~/booking/">Book a consultation {ARROW}</a><a class="btn ghost" href="#faq">FAQs</a>') + f'''
<section class="section"><div class="wrap article-layout">
  <div>
    <div class="reviewed"><img src="~/assets/img/holly-head-600.webp" alt="" width="600" height="600" loading="lazy"><span>Written and medically reviewed by <strong>{NAME} FRCS</strong>, Consultant Oncoplastic Breast Surgeon · Updated {TODAY.strftime("%-d %B %Y")}</span></div>
    <div class="prose">{p["sections"]}
    <div class="note">This page is general information, not medical advice. Whether a procedure is right for you can only be decided in consultation, after proper assessment.</div></div>
  </div>
  <aside>
    <div class="side-card"><h4>At a glance</h4><dl class="facts mt-1">{glance}</dl></div>
    <div class="side-card dark-card"><h4>Arrange a consultation</h4><p>Harley Street · City of London · Buckhurst Hill. Fee-assured with the major insurers.</p><a class="btn gold" href="~/booking/">Book now {ARROW}</a><p class="small mt-1">Or call <a href="tel:{C.SEC_TEL}" style="color:inherit">{C.SEC_PHONE}</a></p></div>
    <div class="side-card"><h4>Related</h4><ul>{rel_links}{rel_posts}<li><a href="~/reviews/">Patient reviews ({C.IWGC_RATING}★)</a></li></ul></div>
  </aside>
</div></section>
<section class="section sand tight"><div class="wrap"><div class="head-row" style="margin-bottom:2rem"><div><p class="eyebrow">Patient reviews</p><h2>Rated <em>{C.IWGC_RATING} out of 5</em></h2></div>{rating_panel()}</div>{review_cards(C.REVIEWS[:3], lead_first=False)}</div></section>
<div id="faq"></div>{faq_block(p["faqs"], "Common <em>questions</em>")}'''
        render(path, title=p["title"], desc=p["desc"], body=body, nav=NAV, active="procedures", priority="0.9",
               schema=[medical_page_schema(path, strip_tags(p["h1"]), p["desc"]),
                       {"@context": "https://schema.org", "@type": "MedicalProcedure", "name": strip_tags(p["nav"]), "url": f"{SITE}/{path}", "description": strip_tags(p["lede"]), "performer": PHYSICIAN_REF},
                       crumbs_schema(crumbs), faq_schema(p["faqs"])])


def build_second_opinion():
    path = "second-opinion/"
    crumbs = [("Home", ""), ("Second opinion", path)]
    faqs = [
        ("Will getting a second opinion delay my treatment?", "Rarely. A private second opinion can usually be arranged within days, and for most breast cancers a short pause to be sure of the plan does not affect outcome. If timing is critical, Mr Ullah will say so plainly."),
        ("Do I need to tell my current team?", "It is courteous and helpful, but not required. Most consultants welcome second opinions, and your existing team can share imaging and pathology to make the review more complete."),
        ("What should I bring?", "Clinic letters, imaging reports (and the images on disc or via an image-sharing link if possible), biopsy or pathology reports, and a list of your questions. Mr Ullah's secretary can help request records."),
        ("Is a second opinion covered by insurance?", "Many UK insurers cover a second opinion consultation. Check with your insurer and obtain a pre-authorisation number before your appointment."),
    ]
    body = head(crumbs, "Second opinions", "A second opinion on breast cancer <em>or breast surgery</em>",
                "Facing a diagnosis or a proposed operation is a big moment. An independent view from an experienced oncoplastic breast surgeon can confirm the plan, or show you options you had not been offered.",
                actions=f'<a class="btn gold" href="~/booking/">Request a second opinion {ARROW}</a>') + f'''
<section class="section"><div class="wrap split top">
  <div class="prose">
    <h2>When patients ask for one</h2>
    <ul><li>You have been offered a mastectomy and want to know whether breast-conserving or oncoplastic surgery is an option</li>
    <li>You want to understand your reconstruction choices before cancer surgery, not after</li>
    <li>You have a benign diagnosis but your symptoms persist</li>
    <li>You are considering risk-reducing surgery because of a BRCA or other gene variant, or a strong family history</li>
    <li>You are unhappy with the result of previous breast surgery and want to know what can be improved</li></ul>
    <h2>What Mr Ullah reviews</h2>
    <p>He reviews your history, examination, imaging and pathology, and where useful asks for further tests or a specialist radiology or pathology review. You get a clear explanation of what he would recommend and why, and a letter for you and your existing team.</p>
  </div>
  <div>{review_cards([C.REVIEWS[1], C.REVIEWS[2]], lead_first=True)}</div>
</div></section>{faq_block(faqs, "Second opinion <em>FAQs</em>")}'''
    desc = "Breast cancer second opinion in London & Essex with consultant oncoplastic breast surgeon Mr Zaker Ullah FRCS. Independent review of diagnosis, mastectomy vs breast-conserving surgery and reconstruction options."
    render(path, title="Breast Cancer Second Opinion London | Mr Zaker Ullah FRCS", desc=desc, body=body, nav=NAV, priority="0.8",
           schema=[medical_page_schema(path, "Breast cancer second opinion", desc), crumbs_schema(crumbs), faq_schema(faqs)])


# =================================================================== LOCATIONS
def build_locations():
    body = head([("Home", ""), ("Clinics", "locations/")], "Clinics", "Private breast clinics in <em>London &amp; Essex</em>",
                "Mr Ullah sees private patients at three hospitals: in London's medical district, inside the historic St Bartholomew's site, and on the Essex border at Buckhurst Hill.") + f'''
<section class="section"><div class="wrap">{loc_cards()}</div></section>
<section class="section sand tight"><div class="wrap split"><div><p class="eyebrow">Insurance</p><h2>Insured or <em>self-funding</em></h2><p class="lede mt-1">Fee-assured with the major UK insurers, so you should not face a shortfall for his fees. Self-pay patients receive a written quote from the hospital before any procedure.</p></div>{insurers()}</div></section>'''
    render("locations/", title="Private Breast Clinics London & Essex | Mr Zaker Ullah FRCS",
           desc="Where to see consultant breast surgeon Mr Zaker Ullah privately: The Harley Street Clinic (W1), Nuffield Health St Bartholomew's (EC1) and Nuffield Health The Holly Hospital, Buckhurst Hill (IG9).",
           body=body, nav=NAV, active="locations", priority="0.9", schema=[crumbs_schema([("Home", ""), ("Clinics", "locations/")])])

    for l in C.LOCATIONS:
        path = f"locations/{l['slug']}/"
        crumbs = [("Home", ""), ("Clinics", "locations/"), (l["short"], path)]
        phone = l.get("phone")
        book_line = f'<a class="btn ghost" href="tel:{l["tel"]}">Call {phone}</a>' if phone else f'<a class="btn ghost" href="tel:{C.SEC_TEL}">Call {C.SEC_PHONE}</a>'
        aside = f'<div><strong>{l["name"]}</strong>{loc_address(l)}</div><div><strong>Appointments</strong>Private secretary: <a href="tel:{C.SEC_TEL}" style="color:inherit">{C.SEC_PHONE}</a>{f"<br>Hospital: {phone}" if phone else ""}</div>' + (f'<div><strong>Clinic times</strong>{l["clinics"]}</div>' if l.get("clinics") else "")
        faqs = [
            (f"How do I book an appointment with Mr Ullah at {l['name']}?", f"Call Mr Ullah's private secretary on {C.SEC_PHONE}, send an enquiry through this website, or ask your GP to refer you to Mr Md Zaker Ullah at {l['name']}. Insured patients should get a pre-authorisation number from their insurer first."),
            (f"Where is {l['name']}?", f"{l['name']} is at {loc_address(l)}. {l['travel']}"),
            ("Which conditions does Mr Ullah treat here?", "New breast lumps and breast pain, nipple discharge, breast cancer surgery, reconstruction, breast reduction and augmentation, fat grafting, gynaecomastia and general surgery including hernia and gallbladder operations. Some operations are only performed at certain hospitals; the secretary will advise."),
            ("Can I be seen quickly with a new breast symptom?", "Yes. New breast symptoms are prioritised, and the aim is examination, imaging and any biopsy at a single visit."),
        ]
        others = "".join(f'<li><a href="~/locations/{o["slug"]}/">{o["name"]}</a></li>' for o in C.LOCATIONS if o is not l)
        maps = "https://www.google.com/maps/search/?api=1&query=" + (l["name"] + " " + l["postcode"]).replace(" ", "+").replace("'", "")
        body = head(crumbs, l["area"], l["h1"], l["intro"], aside=aside,
                    actions=f'<a class="btn gold" href="~/booking/">Book at {l["short"]} {ARROW}</a>{book_line}') + f'''
<section class="section"><div class="wrap split top">
  <div>
    <p class="eyebrow">Why patients choose {l["short"]}</p><h2>Specialist breast care, <em>close to you</em></h2>
    <ul class="kicker-list mt-2">{"".join(f"<li>{w}</li>" for w in l["why"])}</ul>
    <h3 class="mt-3">Getting here</h3><p class="muted mt-1">{l["travel"]}</p>
    <p class="mt-2"><a class="link-arrow" href="{maps}" target="_blank" rel="noopener">Open in Google Maps {ARROW}</a></p>
    <h3 class="mt-3">Patients travel from</h3><div class="area-list mt-1">{"".join(f"<span>{a}</span>" for a in l["serves"])}</div>
  </div>
  <div>
    <p class="eyebrow">Treatments available</p>
    <div class="side-card"><ul>{"".join(f'<li><a href="~/procedures/{p["slug"]}/">{p["nav"]}</a></li>' for p in C.PROCEDURES)}</ul></div>
    <div class="side-card"><h4>Other clinics</h4><ul>{others}</ul></div>
  </div>
</div></section>
<section class="section sand tight"><div class="wrap"><div class="head-row" style="margin-bottom:2rem"><div><p class="eyebrow">Patient reviews</p><h2>What patients <em>say</em></h2></div>{rating_panel()}</div>{review_cards(C.REVIEWS[3:6], lead_first=False)}</div></section>
{faq_block(faqs, f"Seeing Mr Ullah at <em>{l['short']}</em>")}'''
        clinic = {"@context": "https://schema.org", "@type": "MedicalClinic", "@id": f"{SITE}/{path}#clinic",
                  "name": f"{NAME} — Breast Surgeon at {l['name']}", "url": f"{SITE}/{path}", "image": PHYSICIAN["image"],
                  "telephone": C.SEC_TEL, "priceRange": "££££", "medicalSpecialty": ["Oncologic", "Surgical", "PlasticSurgery"],
                  "address": hospital_schema(l)["address"], "areaServed": l["serves"], "employee": PHYSICIAN_REF,
                  "containedInPlace": hospital_schema(l), "hasMap": maps, "isAcceptingNewPatients": True}
        render(path, title=l["title"], desc=l["desc"], body=body, nav=NAV, active="locations", priority="0.9",
               schema=[clinic, crumbs_schema(crumbs), faq_schema(faqs)])


# =================================================================== REVIEWS
def build_reviews():
    path = "reviews/"
    crumbs = [("Home", ""), ("Reviews", path)]
    body = head(crumbs, "Patient reviews", f"Rated {C.IWGC_RATING} <em>by his patients</em>",
                f"Independent, verified feedback matters more than anything a surgeon says about himself. Mr Ullah's patient reviews are collected and published by iWantGreatCare, the UK's independent platform for healthcare reviews. All {C.IWGC_COUNT} of them are five-star.",
                actions=f'<a class="btn gold" href="{C.IWGC}" target="_blank" rel="noopener">Read all on iWantGreatCare {ARROW}</a><a class="btn ghost" href="{C.IWGC}" target="_blank" rel="noopener">Leave a review</a>') + f'''
<section class="section"><div class="wrap"><div class="head-row"><div><p class="eyebrow">Verified on iWantGreatCare</p><h2>In their <em>own words</em></h2></div>{rating_panel()}</div>
{review_cards(C.REVIEWS)}
<p class="small muted mt-2">Excerpts are reproduced word for word from public reviews on iWantGreatCare, some shortened (…). Reviews refer to care at The Holly and at Whipps Cross University Hospital.</p></div></section>
<section class="section sand tight"><div class="wrap split"><div><p class="eyebrow">Treated by Mr Ullah?</p><h2>Share your <em>experience</em></h2></div><div><p class="lede">Positive or critical, your review helps future patients choose their care and helps the team improve. Reviews can be left anonymously.</p><p class="mt-2"><a class="btn" href="{C.IWGC}" target="_blank" rel="noopener">Review Mr Ullah on iWantGreatCare {ARROW}</a></p><p class="small muted mt-2">If something did not go as it should have, please also raise it with the hospital where you were treated so it can be properly addressed.</p></div></div></section>'''
    render(path, title=f"Mr Zaker Ullah Reviews: {C.IWGC_RATING}★ from {C.IWGC_COUNT} Patients",
           desc=f"Read verified patient reviews of consultant breast surgeon Mr Md Zaker Ullah FRCS on iWantGreatCare: rated {C.IWGC_RATING} out of 5 from {C.IWGC_COUNT} reviews, all five-star.",
           body=body, nav=NAV, active="reviews", priority="0.8", schema=[crumbs_schema(crumbs)])
    # Old URL from the previous rebuild → canonicalise to /reviews/
    render("feedback/", title="Patient reviews — moved", desc="This page has moved to /reviews/.", nav=NAV, noindex=True,
           extra_head='<meta http-equiv="refresh" content="0; url=../reviews/">',
           body='<section class="section"><div class="wrap"><p>This page has moved. <a href="~/reviews/">Read patient reviews</a>.</p></div></section>')


# =================================================================== PODCAST
def build_podcast():
    P = C.PODCAST
    path = "podcast/"
    crumbs = [("Home", ""), ("Podcast", path)]
    qa = [
        ("Lumpectomy or mastectomy — how is the decision made?", "It depends on the size of the cancer relative to the breast, where it sits, whether there is more than one area, genetics and, crucially, the patient's own wishes. Oncoplastic techniques mean many women who once needed mastectomy can now keep their breast. <a href=\"~/procedures/breast-cancer-surgery/\">Breast cancer surgery explained</a>."),
        ("What symptoms should I look for, and how should I self-check?", "Not just a lump: skin dimpling, a change in size or shape, a newly inverted nipple, nipple rash or bloodstained discharge, and persistent pain in one spot. Know what is normal for you and get any change checked. <a href=\"~/news/breast-lump-when-to-see-a-specialist/\">When to see a specialist</a>."),
        ("Is breast cancer rising in young women?", "UK data show breast cancer incidence has risen in younger women in recent decades, although it remains far less common under 40. Young women should never be told they are ‘too young’ to have a new symptom assessed."),
        ("Does everyone need radiotherapy?", "No. Radiotherapy is standard after most breast-conserving surgery, and selectively after mastectomy, but some lower-risk patients can safely omit it. The decision is made by the multidisciplinary team using the tumour's biology and stage."),
        ("What is triple-negative breast cancer?", "A type of breast cancer that lacks oestrogen, progesterone and HER2 receptors, so hormone and HER2-targeted drugs do not work. It is often treated with chemotherapy, sometimes with immunotherapy, before surgery, and responds well to modern regimens in many patients."),
    ]
    body = head(crumbs, f"Podcast · {P['date_label']}", "&ldquo;5 breast cancer questions, <em>answered by a surgeon</em>&rdquo;",
                f"Mr Ullah's guest appearance on <em>{P['show']}</em>, Season {P['season']}, Episode {P['episode']}. {P['summary']}",
                actions=f'<a class="btn gold" href="#watch">Watch now {ARROW}</a><a class="btn ghost" href="{P["spotify"]}" target="_blank" rel="noopener">Spotify</a><a class="btn ghost" href="{P["apple"]}" target="_blank" rel="noopener">Apple Podcasts</a>') + f'''
<section class="section" id="watch"><div class="wrap narrow">{video_facade()}
<p class="small muted mt-1">{P["duration_label"]} · Recorded live · Hosted by {P["host"]}. Video plays from YouTube when you press play.</p></div></section>
<section class="section flush-top"><div class="wrap faq-grid"><div><p class="eyebrow">In this episode</p><h2>The five <em>questions</em></h2><p class="lede mt-1">A short written summary of each topic, with links to more detail.</p></div>
<div class="faq">{"".join(f'<details id="q{i + 1}" open><summary>{i + 1}. {q}</summary><div class="a"><p>{a}</p></div></details>' for i, (q, a) in enumerate(qa))}</div></div></section>
<section class="section dark tight"><div class="wrap split"><div><p class="eyebrow">About the show</p><h2><em>Everything Changed</em></h2></div><p class="lede">{P["host"]}&rsquo;s podcast about life after breast cancer. In this live episode Rosie talks to the surgeon who diagnosed her and later performed her double mastectomy and reconstruction.</p></div></section>'''
    ep = {"@context": "https://schema.org", "@type": "PodcastEpisode", "name": P["title"], "url": P["spotify"], "datePublished": P["date"],
          "timeRequired": P["duration"], "episodeNumber": P["episode"], "description": P["summary"],
          "partOfSeries": {"@type": "PodcastSeries", "name": P["show"]}, "actor": [{"@type": "Person", "name": P["host"]}, PHYSICIAN_REF],
          "associatedMedia": {"@type": "MediaObject", "contentUrl": P["spotify"]}}
    video = {"@context": "https://schema.org", "@type": "VideoObject", "name": f"{P['title']} — {P['show']}", "description": P["summary"],
             "thumbnailUrl": f"https://i.ytimg.com/vi/{P['youtube']}/hqdefault.jpg", "uploadDate": P["date"], "duration": P["duration"],
             "embedUrl": f"https://www.youtube.com/embed/{P['youtube']}", "contentUrl": f"https://www.youtube.com/watch?v={P['youtube']}"}
    render(path, title="Breast Cancer Podcast: 5 Questions for a Surgeon | Mr Ullah",
           desc="Watch consultant breast surgeon Mr Zaker Ullah on Everything Changed with Rosie Fawehimi: lumpectomy vs mastectomy, symptoms, young women, radiotherapy and triple-negative breast cancer.",
           body=body, nav=NAV, active="podcast", priority="0.8", schema=[ep, video, crumbs_schema(crumbs), faq_schema(qa)])


# =================================================================== NEWS
def build_news():
    crumbs = [("Home", ""), ("Insights", "news/")]
    cats = sorted({p["category"] for p in POSTS})
    body = head(crumbs, "Insights", "Clear answers from a <em>breast surgeon</em>",
                "Plain-English guides to breast symptoms, diagnosis, surgery and recovery, written and reviewed by Mr Ullah.") + f'''
<section class="section"><div class="wrap"><div class="area-list" style="margin-bottom:2rem">{"".join(f"<span>{c}</span>" for c in cats)}</div>{post_cards(POSTS)}</div></section>'''
    render("news/", title="Breast Health Articles & Advice | Mr Zaker Ullah",
           desc="Expert breast health articles from London consultant breast surgeon Mr Zaker Ullah FRCS: breast lumps, breast cancer, oncoplastic surgery, reconstruction, gynaecomastia and recovery.",
           body=body, nav=NAV, active="news", priority="0.8",
           schema=[crumbs_schema(crumbs), {"@context": "https://schema.org", "@type": "Blog", "name": "Insights — Mr Zaker Ullah", "url": SITE + "/news/", "author": PHYSICIAN_REF,
                                            "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/news/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]}])

    for p in POSTS:
        path = f"news/{p['slug']}/"
        crumbs = [("Home", ""), ("Insights", "news/"), (p["title"], path)]
        date_label = p["date_obj"].strftime("%-d %B %Y")
        reviewed = p.get("reviewed", p["date"])
        rel_proc = "".join(f'<li><a href="~/procedures/{s}/">{PROC[s]["nav"]}</a></li>' for s in p["related"] if s in PROC)
        more = [x for x in POSTS if x is not p][:3]
        faq_section = faq_html([(q, a.replace("<p>", "").replace("</p>", "||").rstrip("|")) for q, a in p["faqs"]]) if p["faqs"] else ""
        body = f'''<article>{head(crumbs, f'{escape(p["category"])} · <time datetime="{p["date"]}">{date_label}</time> · {p["minutes"]} min read', escape(p["title"]), escape(p["description"]))}
<section class="section"><div class="wrap article-layout">
  <div>
    <div class="reviewed"><img src="~/assets/img/holly-head-600.webp" alt="" width="600" height="600" loading="lazy"><span>By <strong><a href="~/biography/" style="color:inherit">{NAME} FRCS</a></strong>, Consultant Oncoplastic Breast Surgeon · Medically reviewed {datetime.date.fromisoformat(reviewed).strftime("%-d %B %Y")}</span></div>
    <div class="prose">{p["html"]}
    {f'<h2 id="faq">Frequently asked questions</h2>{faq_section}' if faq_section else ""}
    <div class="note">This article is general information, not medical advice. If you have a breast symptom, arrange an assessment through your GP or a <a href="~/booking/">specialist clinic</a>. In an emergency call 999.</div></div>
  </div>
  <aside>
    <div class="side-card dark-card"><h4>Worried about a symptom?</h4><p>Prompt private appointments at Harley Street, the City and Buckhurst Hill.</p><a class="btn gold" href="~/booking/">Book a consultation {ARROW}</a></div>
    {f'<div class="side-card"><h4>Related treatments</h4><ul>{rel_proc}</ul></div>' if rel_proc else ""}
    <div class="side-card"><h4>Rated {C.IWGC_RATING}★</h4><p>{C.IWGC_COUNT} verified reviews on iWantGreatCare.</p><ul><li><a href="~/reviews/">Read patient reviews</a></li><li><a href="~/podcast/">Listen to the podcast</a></li></ul></div>
  </aside>
</div></section></article>
{f'<section class="section sand tight"><div class="wrap"><p class="eyebrow">Keep reading</p>{post_cards(more)}</div></section>' if more else ""}'''
        posting = {"@context": "https://schema.org", "@type": ["BlogPosting", "MedicalWebPage"], "headline": p["title"], "description": p["description"],
                   "url": f"{SITE}/{path}", "mainEntityOfPage": f"{SITE}/{path}", "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
                   "lastReviewed": reviewed, "author": {"@type": "Person", "@id": SITE + "/#physician", "name": NAME, "url": SITE + "/biography/"},
                   "reviewedBy": PHYSICIAN_REF, "publisher": PHYSICIAN_REF, "image": SITE + "/assets/img/og-card.png", "keywords": p["keyword"],
                   "articleSection": p["category"], "wordCount": p["words"], "inLanguage": "en-GB"}
        schema = [posting, crumbs_schema(crumbs)]
        if p["faqs"]:
            schema.append(faq_schema(p["faqs_text"]))
        render(path, title=p["title"] if len(p["title"]) > 44 else f'{p["title"]} | Mr Zaker Ullah', desc=p["description"], body=body, nav=NAV,
               active="news", og_type="article", priority="0.7", schema=schema)


# =================================================================== BOOKING
def build_booking():
    path = "booking/"
    crumbs = [("Home", ""), ("Book", path)]
    opts = "".join(f"<option>{l['name']}</option>" for l in C.LOCATIONS)
    procs = "".join(f"<option>{strip_tags(p['nav'])}</option>" for p in C.PROCEDURES)
    body = head(crumbs, "Appointments", "Book a consultation <em>with Mr Ullah</em>",
                "Call the private secretary, or send an enquiry and the team will call you back to arrange a time at the clinic that suits you. New breast symptoms are prioritised.",
                aside=f'<div><strong>Private secretary</strong><a href="tel:{C.SEC_TEL}" style="color:inherit;font-family:var(--serif);font-size:1.6rem">{C.SEC_PHONE}</a></div><div><strong>Email</strong><a href="mailto:{C.SEC_EMAIL}" style="color:inherit">{C.SEC_EMAIL}</a></div><div><strong>Rapid Access Breast Clinic</strong>Tuesday afternoons at The Holly</div>') + f'''
<section class="section"><div class="wrap split top">
  <div>
    <p class="eyebrow">Enquiry</p><h2>Request an <em>appointment</em></h2>
    <p class="muted mt-1">Your enquiry opens in your email app, addressed to Mr Ullah's private secretary. Please do not include detailed medical information; that is best discussed in consultation.</p>
    <form class="form mt-2" id="enquiry" data-to="{C.SEC_EMAIL}">
      <div class="row"><label>Full name<input name="name" required autocomplete="name"></label><label>Phone<input name="phone" type="tel" required autocomplete="tel"></label></div>
      <div class="row"><label>Email<input name="email" type="email" autocomplete="email"></label><label>Preferred clinic<select name="clinic">{opts}<option>No preference</option></select></label></div>
      <div class="row"><label>Reason for appointment<select name="reason">{procs}<option>Second opinion</option><option>Other</option></select></label><label>Funding<select name="funding"><option>Private medical insurance</option><option>Self-funding</option><option>Not sure yet</option></select></label></div>
      <label>Anything we should know (optional)<textarea name="message" placeholder="For example: best times to call, insurer name"></textarea></label>
      <label class="consent"><input type="checkbox" required> I agree to be contacted about my enquiry by Mr Ullah's private practice team.</label>
      <button class="btn gold" type="submit">Send enquiry {ARROW}</button>
    </form>
  </div>
  <div>
    <div class="side-card"><h4>Insured patients</h4><p>Mr Ullah is fee-assured with the major UK insurers. Most insurers need a GP referral and a pre-authorisation number before your first appointment.</p><div class="mt-1">{insurers()}</div></div>
    <div class="side-card"><h4>Self-funding patients</h4><p>You do not need insurance or a referral. The hospital confirms the consultation fee when you book, and gives a written, fixed price for any tests or surgery before you commit.</p></div>
    <div class="side-card"><h4>What to bring</h4><ul><li>GP referral letter (if you have one)</li><li>Previous breast imaging or biopsy results</li><li>A list of current medications</li><li>Insurance details and pre-authorisation number</li></ul></div>
    <div class="note mt-2"><strong>Urgent symptoms:</strong> if you are acutely unwell, call 999 or go to your nearest emergency department.</div>
  </div>
</div></section>
<section class="section sand"><div class="wrap"><div class="head-row"><div><p class="eyebrow">Clinics</p><h2>Choose where to be <em>seen</em></h2></div></div>{loc_cards(with_nhs=False)}</div></section>'''
    render(path, title="Book a Private Breast Surgeon in London | Mr Zaker Ullah",
           desc=f"Book a private consultation with breast surgeon Mr Zaker Ullah FRCS at Harley Street, Nuffield St Bartholomew's or The Holly, Buckhurst Hill. Call {C.SEC_PHONE}. Insured & self-pay welcome.",
           body=body, nav=NAV, priority="0.9", schema=[crumbs_schema(crumbs)])


def build_404():
    body = f'''<section class="section notfound"><div class="wrap center"><p class="eyebrow">Page not found</p><h1>We couldn&rsquo;t find <em>that page</em></h1>
<p class="lede mt-1">It may have moved during our redesign.</p><div class="actions mt-2" style="justify-content:center"><a class="btn" href="/">Home</a><a class="btn ghost" href="/procedures/">Treatments</a><a class="btn ghost" href="/booking/">Book</a></div></div></section>'''
    render("404.html", title="Page not found | Mr Zaker Ullah", desc="Page not found.", body=body, nav=NAV, noindex=True)


# =================================================================== FILES
def build_files():
    urls = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{p}</priority></url>\n" for u, p in SITEMAP)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /content/\n\nSitemap: {SITE}/sitemap.xml\n")
    items = "".join(f"<item><title>{escape(p['title'])}</title><link>{SITE}/news/{p['slug']}/</link><guid>{SITE}/news/{p['slug']}/</guid><pubDate>{datetime.datetime.combine(p['date_obj'], datetime.time(8)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{escape(p['description'])}</description></item>" for p in POSTS)
    open(os.path.join(ROOT, "feed.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mr Zaker Ullah — Breast Health Insights</title><link>{SITE}/news/</link><description>Articles by consultant breast surgeon Mr Md Zaker Ullah FRCS</description><language>en-gb</language>{items}</channel></rss>\n')
    llms = [f"# {NAME} FRCS — Consultant Oncoplastic Breast Surgeon, London & Essex", "",
            f"> {PHYSICIAN['description']} GMC 4368515. Rated {C.IWGC_RATING}/5 from {C.IWGC_COUNT} verified reviews on iWantGreatCare. Private secretary: {C.SEC_PHONE}.", "",
            "## Key pages", f"- [About]({SITE}/biography/)", f"- [Book a consultation]({SITE}/booking/)", f"- [Reviews]({SITE}/reviews/)", f"- [Podcast]({SITE}/podcast/)", f"- [Second opinions]({SITE}/second-opinion/)", "",
            "## Treatments"] + [f"- [{strip_tags(p['nav'])}]({SITE}/procedures/{p['slug']}/): {strip_tags(p['navdesc'])}" for p in C.PROCEDURES] + ["", "## Clinics"] + \
           [f"- [{l['name']}]({SITE}/locations/{l['slug']}/): {loc_address(l)}" for l in C.LOCATIONS] + ["", "## Articles"] + [f"- [{p['title']}]({SITE}/news/{p['slug']}/)" for p in POSTS]
    open(os.path.join(ROOT, "llms.txt"), "w").write("\n".join(llms) + "\n")


if __name__ == "__main__":
    build_home(); build_about(); build_procedures(); build_second_opinion(); build_locations()
    build_reviews(); build_podcast(); build_news(); build_booking(); build_404(); build_files()
    print(f"Built {len(SITEMAP)} indexable pages · {len(POSTS)} posts live · {len(SCHEDULED)} scheduled")
    for s in SCHEDULED:
        print(f"  scheduled {s['date']}  {s['slug']}")
