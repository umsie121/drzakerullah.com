"""Share cards (Open Graph images), one per page:  python3 _build/og.py [--force]

Renders 1200x630 cards with local Google Chrome into assets/og/<page-key>.jpg. A card is only
re-rendered when its text changes (the text hash is kept in assets/og/index.json), so run this
after adding blog posts or changing page titles, then commit the new images. Pages without a
card fall back to assets/img/og-card.jpg, so the daily GitHub build never needs Chrome.
"""
import hashlib
import html
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402
import content as C  # noqa: E402

ROOT = B.ROOT
OUT = os.path.join(ROOT, "assets", "og")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..800,0..100,0..1;'
         '1,9..144,300..800,0..100,0..1&family=Figtree:wght@400..700&family=Noto+Sans+Bengali:wght@500;800&family=Noto+Naskh+Arabic:wght@700&family=Noto+Sans+Arabic:wght@500&display=block">')
IMG = "file://" + os.path.join(ROOT, "assets", "img")

BASE = """*{margin:0;box-sizing:border-box}html,body{width:1200px;height:630px;overflow:hidden}
body{font-family:Figtree,"Noto Sans Bengali","Noto Sans Arabic",sans-serif;-webkit-font-smoothing:antialiased}
.serif{font-family:Fraunces,"Noto Sans Bengali","Noto Naskh Arabic",serif;font-variation-settings:"opsz" 144,"SOFT" 50,"WONK" 1;letter-spacing:-.04em}
.k{font-weight:700;font-size:18px;letter-spacing:.07em;text-transform:uppercase}
.mono{position:absolute;width:64px;height:64px;border-radius:16px;display:grid;place-items:center}
.mono span{font-family:Fraunces,serif;font-style:italic;font-weight:560;font-size:44px;letter-spacing:-.06em;font-variation-settings:"opsz" 144,"SOFT" 60,"WONK" 1;transform:translate(-2px,-4px)}
.foot{position:absolute;left:80px;right:80px;bottom:56px;display:flex;align-items:center;gap:18px;font-size:19px;font-weight:600}
.foot img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.foot .sp{flex:1}"""


def card(kind, eyebrow, title, sub=""):
    """Return the HTML for one card. kind: treatment | clinic | post | page."""
    t = html.escape(title)
    size = 92 if len(title) < 26 else 76 if len(title) < 44 else 62 if len(title) < 64 else 54
    if kind == "post":
        css = BASE + f""" body{{background:linear-gradient(160deg,#fffaf7 0,#f8dccf 100%);color:#55203f}}
.t{{position:absolute;left:80px;top:150px;right:180px}} .t .k{{color:#b9472f}}
h1{{margin-top:22px;font-size:{size}px;line-height:1.02;font-weight:560;color:#55203f}}
.sub{{margin-top:22px;font-size:23px;color:#76656d;max-width:820px;line-height:1.4}}
.mono{{right:80px;top:64px;background:#55203f}} .mono span{{color:#f8c3ae}}
.foot{{color:#55203f;border-top:1.5px solid rgba(85,32,63,.18);padding-top:26px;bottom:48px}} .foot .m{{color:#76656d;font-weight:500}}"""
        body = f"""<div class="mono"><span>zu</span></div><div class="t"><span class="k">{html.escape(eyebrow)}</span><h1 class="serif">{t}</h1>{f'<p class="sub">{html.escape(sub)}</p>' if sub else ''}</div>
<div class="foot"><img src="{IMG}/zu-navy-600.jpg"><span>Mr Zaker Ullah FRCS</span><span class="m">Consultant Breast Surgeon</span><span class="sp"></span><span class="m">drzakerullah.com</span></div>"""
    elif kind in ("treatment", "clinic"):
        css = BASE + f""" body{{background:radial-gradient(120% 140% at 100% 0,#7d3a60 0,#55203f 45%,#3a1529 100%);color:#fbf1ec}}
.t{{position:absolute;left:80px;top:168px;right:400px}} .t .k{{color:#f8c3ae}}
h1{{margin-top:24px;font-size:{size + 8}px;line-height:.98;font-weight:560;color:#fff}}
.sub{{margin-top:24px;font-size:24px;line-height:1.42;color:rgba(251,241,236,.74);max-width:640px}}
.ring{{position:absolute;right:80px;top:50%;transform:translateY(-58%);width:300px;height:300px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 10px rgba(248,195,174,.14),0 0 0 22px rgba(248,195,174,.07)}}
.ring img{{width:100%;height:100%;object-fit:cover;object-position:50% 22%}}
.mono{{left:80px;top:64px;width:auto;height:auto}} .mono span{{color:#f8c3ae;font-size:40px}}
.foot{{color:#fff}} .foot .m{{color:rgba(251,241,236,.6);font-weight:500}}"""
        body = f"""<div class="mono"><span>zu</span></div><div class="t"><span class="k">{html.escape(eyebrow)}</span><h1 class="serif">{t}</h1>{f'<p class="sub">{html.escape(sub)}</p>' if sub else ''}</div>
<div class="ring"><img src="{IMG}/zu-navy-900.jpg"></div>
<div class="foot"><span>Mr Zaker Ullah FRCS</span><span class="m">Consultant Oncoplastic Breast Surgeon</span><span class="sp"></span><span class="m">drzakerullah.com</span></div>"""
    else:
        css = BASE + f""" body{{background:#1a0f08;color:#fbf1ec}}
.p{{position:absolute;right:0;top:0;width:520px;height:630px;background:url({IMG}/zu-navy-1300.jpg) 50% 16%/cover}}
.p:after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#1a0f08 0,rgba(26,15,8,0) 40%),linear-gradient(0deg,#1a0f08 0,rgba(26,15,8,0) 20%)}}
.t{{position:absolute;left:80px;top:168px;width:660px}} .t .k{{color:#f8c3ae}}
h1{{margin-top:22px;font-size:{size + 4}px;line-height:.98;font-weight:560;color:#fff}}
.sub{{margin-top:24px;font-size:24px;line-height:1.42;color:rgba(251,241,236,.74)}}
.mono{{left:80px;top:64px;width:auto;height:auto}} .mono span{{color:#ee8a6c;font-size:40px}}
.foot{{color:#fff;right:600px}} .foot .m{{color:rgba(251,241,236,.6);font-weight:500}}"""
        body = f"""<div class="p"></div><div class="mono"><span>zu</span></div><div class="t"><span class="k">{html.escape(eyebrow)}</span><h1 class="serif">{t}</h1>{f'<p class="sub">{html.escape(sub)}</p>' if sub else ''}</div>
<div class="foot"><span>Mr Zaker Ullah FRCS</span><span class="sp"></span><span class="m">drzakerullah.com</span></div>"""
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body>{body}</body></html>'


def pages():
    """(page key, kind, eyebrow, title, sub) for every page that gets its own card."""
    out = [
        ("biography", "page", "Biography", "Mr Md Zaker Ullah", "From the Royal Marsden to leading the Whipps Cross Breast Unit."),
        ("reviews", "page", "Patient reviews", "Kind, thorough and never rushed", "Rated 5.0 on iWantGreatCare. 100% five-star."),
        ("podcast", "page", "Everything Changed podcast", "Five questions about breast cancer", "Answered by a breast surgeon."),
        ("booking", "page", "Appointments", "Book a consultation", "The Holly, Buckhurst Hill, Canary Wharf and the City of London."),
        ("faqs", "page", "Questions answered", "What patients ask first", "Appointments, results, insurance and surgery."),
        ("fees-and-insurance", "page", "Fees and insurance", "Insured or self-funding", "Bupa Platinum consultant, fee-assured. Most major insurers."),
        ("your-visit", "page", "Your first visit", "What happens on the day", "Consultation, imaging and provisional results, usually at one visit."),
        ("second-opinion", "page", "Second opinions", "An independent view", "On a diagnosis or a proposed operation."),
        ("remote-consultations", "page", "Video and international", "Consultations from anywhere", "By video or telephone, in English, Bangla or Arabic."),
        ("procedures", "treatment", "Treatments", "Areas of practice", "Breast symptoms, breast cancer, reconstruction, and men's and general surgery."),
        ("locations", "clinic", "Clinics", "Three private clinics", "The Holly, Buckhurst Hill · Canary Wharf · St Bartholomew's, City of London."),
        ("news", "post", "Blog", "Clear answers, in plain English", "Guides to breast symptoms, surgery and recovery, written by Mr Ullah."),
    ]
    for p in C.PROCEDURES:
        out.append((f"procedures-{p['slug']}", "treatment", "Treatment", p["nav"], p["summary"]))
    for l in C.LOCATIONS:
        out.append((f"locations-{l['slug']}", "clinic", l["area"], l["name"], B.loc_address(l)))
    out.append(("bn", "page", "বাংলা", "ডাঃ মোঃ জাকের উল্লাহ", "কনসালটেন্ট ব্রেস্ট সার্জন, লন্ডন। বাংলা, ইংরেজি ও আরবিতে কনসালটেশন।"))
    out.append(("ar", "page", "العربية", "الدكتور محمد ذاكر الله", "استشاري جراحة الثدي في لندن. استشارات بالعربية والإنجليزية والبنغالية."))
    for p in B.ALL_POSTS:
        out.append((f"news-{p['slug']}", "post", p["category"], p["title"], ""))
    return out


def main(force=False):
    if not os.path.exists(CHROME):
        sys.exit("Google Chrome not found; share cards need it locally.")
    os.makedirs(OUT, exist_ok=True)
    idx_path = os.path.join(OUT, "index.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
    made = 0
    with tempfile.TemporaryDirectory() as tmp:
        for key, kind, eyebrow, title, sub in pages():
            doc = card(kind, eyebrow, title, sub)
            h = hashlib.sha1(doc.encode()).hexdigest()[:12]
            jpg = os.path.join(OUT, f"{key}.jpg")
            if not force and idx.get(key) == h and os.path.exists(jpg):
                continue
            src, png = os.path.join(tmp, "c.html"), os.path.join(tmp, "c.png")
            open(src, "w").write(doc)
            cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                   "--virtual-time-budget=7000", "--window-size=1200,630", f"--screenshot={png}", "file://" + src]
            if subprocess.run(cmd, capture_output=True).returncode != 0:
                subprocess.run(cmd, check=True, capture_output=True)  # Chrome occasionally fails once; one retry
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", png, "-q:v", "2", jpg], check=True)
            idx[key] = h
            json.dump(idx, open(idx_path, "w"), indent=1, sort_keys=True)
            made += 1
            print("card", key)
    json.dump(idx, open(idx_path, "w"), indent=1, sort_keys=True)
    print(f"{made} cards rendered, {len(idx)} in total")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
