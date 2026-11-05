"""Add an Unsplash photo to every blog post that does not have one yet:
    python3 _build/unsplash.py [--forget] [--redo slug]

Reads the access key from $UNSPLASH_ACCESS_KEY or _build/.secrets/unsplash (see unsplash_key.py).
For each post it searches Unsplash with the post's `image_query`, saves the photo to
assets/img/blog/<slug>-{800,1600}.{jpg,webp}, records the photographer for the credit line,
and pings Unsplash's download endpoint as their API guidelines require. --forget deletes the
key file afterwards. Choose calm, non-clinical images: no bodies, no breasts, no ribbons.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request


def strip_emoji(text):
    """Drop emoji (flags, pictographs, variation selectors) from a name, keeping plain text."""
    return re.sub("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]", "", text).strip()


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KEY_FILE = os.path.join(HERE, ".secrets", "unsplash")
OUT = os.path.join(ROOT, "assets", "img", "blog")
APP = "drzakerullah"


def key():
    k = os.environ.get("UNSPLASH_ACCESS_KEY") or (open(KEY_FILE).read().strip() if os.path.exists(KEY_FILE) else "")
    if not k:
        sys.exit("No key. Run python3 _build/unsplash_key.py first, or set UNSPLASH_ACCESS_KEY.")
    return k


def api(url, k):
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {k}", "Accept-Version": "v1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def front(path):
    text = open(path).read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    return text, m, meta


def set_fields(path, fields):
    text, m, _ = front(path)
    head = m.group(1)
    for k, v in fields.items():
        line = f"{k}: {v}"
        head = re.sub(rf"^{k}:.*$", line, head, flags=re.M) if re.search(rf"^{k}:", head, re.M) else head + "\n" + line
    open(path, "w").write(f"---\n{head}\n---\n" + text[m.end():])


def main():
    k = key()
    redo = sys.argv[sys.argv.index("--redo") + 1] if "--redo" in sys.argv else None
    os.makedirs(OUT, exist_ok=True)
    used = set()
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "blog", "*.md"))):
        _, _, meta = front(path)
        if meta.get("image_id"):
            used.add(meta["image_id"])
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "blog", "*.md"))):
        _, _, meta = front(path)
        slug = meta["slug"]
        if meta.get("image") and slug != redo:
            continue
        q = meta.get("image_query") or meta.get("category", "calm")
        res = api(f"https://api.unsplash.com/search/photos?{urllib.parse.urlencode({'query': q, 'orientation': 'landscape', 'content_filter': 'high', 'per_page': 15})}", k)
        pick = next((p for p in res.get("results", []) if p["id"] not in used), None)
        if not pick:
            print("no photo for", slug, "query:", q)
            continue
        used.add(pick["id"])
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "p.jpg")
            urllib.request.urlretrieve(pick["urls"]["raw"] + "&w=1600&fit=max&q=80&fm=jpg", src)
            for w in (800, 1600):
                jpg = os.path.join(OUT, f"{slug}-{w}.jpg")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"scale={w}:-2", "-q:v", "4", jpg], check=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", jpg, "-quality", "75", jpg[:-4] + ".webp"], check=True)
        try:
            api(pick["links"]["download_location"], k)  # required by the Unsplash API guidelines
        except Exception:
            pass
        alt = (pick.get("alt_description") or q).replace(":", "").strip().capitalize()
        utm = f"?utm_source={APP}&utm_medium=referral"
        set_fields(path, {"image": f"blog/{slug}", "image_id": pick["id"], "image_alt": alt,
                          "image_credit": strip_emoji(pick["user"]["name"].replace(":", "")), "image_credit_url": pick["user"]["links"]["html"] + utm})
        print("photo", slug, "by", pick["user"]["name"])
    if "--forget" in sys.argv and os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
        print("key deleted")


if __name__ == "__main__":
    main()
