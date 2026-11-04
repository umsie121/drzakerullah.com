"""Cover images for the Bengali videos:  python3 _build/covers.py

Renders 1280x720 covers with local Google Chrome into assets/img/video/<slug>.{jpg,webp}.
They replace YouTube's own thumbnails on the blog and video pages.
"""
import os
import subprocess
import sys
import tempfile
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "video")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IMG = "file://" + os.path.join(ROOT, "assets", "img")

# slug: (Bangla title, English line, background)
COVERS = {
    "breast-cancer-self-examination-in-bangla": ("How to check your breasts", "Breast Cancer Awareness Month",
                                                 "radial-gradient(120% 140% at 100% 0,#7d3a60 0,#55203f 48%,#3a1529 100%)", "In Bangla"),
    "coronavirus-qampa-in-bangla": ("Coronavirus questions answered", "Recorded during the pandemic",
                                    "radial-gradient(120% 140% at 100% 0,#3b2a33 0,#1a0f08 60%,#120a06 100%)", "In Bangla"),
    "covid-advice-with-dr-zaker-ullah": ("COVID advice", "A health segment for TV3 Bangla",
                                         "radial-gradient(120% 140% at 100% 0,#a4533f 0,#6a2b50 55%,#3a1529 100%)", "In Bangla"),
    "health-advice": ("Everyday health advice", "Viewers' questions, answered on TV3 Bangla",
                      "radial-gradient(120% 140% at 100% 0,#5a3a4a 0,#2c1a22 55%,#1a0f08 100%)", "In Bangla"),
    "podcast": ("Five questions about breast cancer, answered by a surgeon", "Everything Changed with Rosie Fawehimi",
                "radial-gradient(120% 140% at 100% 0,#f8c3ae 0,#ee8a6c 30%,#6a2b50 75%,#3a1529 100%)", "Podcast"),
}


def html(title, sub, bg, source, tag):
    size = 96 if len(title) < 22 else 80 if len(title) < 34 else 64
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@500;800&family=Figtree:wght@500;600;700&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,560,50,1;1,9..144,560,60,1&display=block">
<style>*{{margin:0;box-sizing:border-box}}html,body{{width:1280px;height:720px;overflow:hidden}}
body{{background:{bg};color:#fbf1ec;font-family:Figtree,sans-serif;-webkit-font-smoothing:antialiased;position:relative}}
.k{{position:absolute;left:88px;top:84px;font:700 20px Figtree;letter-spacing:.08em;text-transform:uppercase;color:#f8c3ae}}
.k b{{font-family:"Noto Sans Bengali";font-weight:800;letter-spacing:0;text-transform:none;margin-left:10px}}
h1{{position:absolute;left:88px;top:150px;width:660px;font-family:Fraunces,serif;font-weight:560;font-variation-settings:"opsz" 144,"SOFT" 50,"WONK" 1;letter-spacing:-.04em;font-size:{size}px;line-height:1.02;color:#fff}}
.en{{position:absolute;left:88px;bottom:160px;font:500 30px Figtree;color:rgba(251,241,236,.72)}}
.ring{{position:absolute;right:96px;top:50%;transform:translateY(-50%);width:400px;height:400px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 12px rgba(248,195,174,.14),0 0 0 28px rgba(248,195,174,.06)}}
.ring img{{width:100%;height:100%;object-fit:cover;object-position:50% 22%}}
.play{{position:absolute;right:96px;bottom:118px;width:112px;height:112px;border-radius:50%;background:#ee8a6c;display:grid;place-items:center;box-shadow:0 24px 50px -18px rgba(0,0,0,.55)}}
.play:after{{content:"";border-style:solid;border-width:20px 0 20px 32px;border-color:transparent transparent transparent #55203f;margin-left:8px}}
.foot{{position:absolute;left:88px;right:88px;bottom:70px;display:flex;gap:18px;align-items:center;font:600 21px Figtree}}
.foot .m{{color:rgba(251,241,236,.6);font-weight:500}} .foot .sp{{flex:1}}
.mono{{font-family:Fraunces,serif;font-style:italic;font-size:34px;color:#ee8a6c;letter-spacing:-.06em;margin-right:6px}}
</style></head><body>
<span class="k">{escape(tag)}</span>
<h1>{escape(title)}</h1><p class="en">{escape(sub)}</p>
<div class="ring"><img src="{IMG}/zu-navy-900.jpg"></div><span class="play"></span>
<div class="foot"><span class="mono">zu</span><span>Mr Zaker Ullah FRCS</span><span class="sp"></span><span class="m">{escape(source)}</span></div>
</body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        items = [(v["slug"], v.get("by", "YouTube")) for v in C.VIDEOS] + [("podcast", "Season 3")]
        for slug, source in items:
            if slug not in COVERS:
                continue
            title, sub, bg, tag = COVERS[slug]
            src, png = os.path.join(tmp, "c.html"), os.path.join(tmp, "c.png")
            open(src, "w").write(html(title, sub, bg, source, tag))
            v = {"slug": slug}
            cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                   "--virtual-time-budget=7000", "--window-size=1280,720", f"--screenshot={png}", "file://" + src]
            if subprocess.run(cmd, capture_output=True).returncode != 0:
                subprocess.run(cmd, check=True, capture_output=True)
            jpg = os.path.join(OUT, f"{v['slug']}.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", png, "-q:v", "3", jpg], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", jpg, "-quality", "78", jpg[:-4] + ".webp"], check=True)
            print("cover", v["slug"])


if __name__ == "__main__":
    main()
