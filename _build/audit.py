"""SEO and LLM-readiness audit of the built site:  python3 _build/audit.py

Checks every generated page for the signals search engines and AI assistants read:
title and description length, a single h1, canonical URL, robots, Open Graph image,
hreflang, JSON-LD validity, image alt text and internal links that resolve. Also checks
that the sitemap lists exactly the indexable pages.
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_build"))
from layout import SITE  # noqa: E402

SKIP = {"_build", "content", "assets", "node_modules", ".git", ".github", ".claude"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.meta, self.links, self.h1, self.imgs, self.ld, self.hreflang = "", {}, [], 0, [], [], []
        self._t = self._ld = False
        self.canonical = None
        self.lang = None
        self.buf = ""

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._t = True
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang.append((a["hreflang"], a.get("href")))
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            self.imgs.append(a)
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld, self.buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        if tag == "script" and self._ld:
            self._ld = False
            self.ld.append(self.buf)

    def handle_data(self, d):
        if self._t:
            self.title += d
        if self._ld:
            self.buf += d


def url_for(path):
    rel = os.path.relpath(path, ROOT)
    if rel == "index.html":
        return SITE + "/"
    if rel == "404.html":
        return SITE + "/404.html"
    return SITE + "/" + rel[: -len("index.html")]


def exists(url):
    u = urlparse(url)
    if u.netloc and u.netloc != urlparse(SITE).netloc:
        return True
    p = u.path.lstrip("/")
    full = os.path.join(ROOT, p)
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))


def main():
    pages = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if not set(os.path.relpath(p, ROOT).split(os.sep)) & SKIP]
    sitemap = set(re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml")).read()))
    issues, indexable = [], set()
    for path in sorted(pages):
        url = url_for(path)
        pg = Page()
        pg.feed(open(path, encoding="utf-8").read())
        noindex = "noindex" in pg.meta.get("robots", "")
        tag = os.path.relpath(path, ROOT)
        if not noindex and tag != "404.html":
            indexable.add(url)
            t, d = pg.title.strip(), pg.meta.get("description", "")
            if not 25 <= len(t) <= 65:
                issues.append((tag, f"title length {len(t)}: {t}"))
            if not 110 <= len(d) <= 165:
                issues.append((tag, f"description length {len(d)}"))
            if pg.h1 != 1:
                issues.append((tag, f"{pg.h1} h1 tags"))
            if pg.canonical != url:
                issues.append((tag, f"canonical {pg.canonical} != {url}"))
            og = pg.meta.get("og:image", "")
            if not og or not exists(og):
                issues.append((tag, f"og:image missing or not found: {og}"))
            if not pg.lang:
                issues.append((tag, "no lang attribute"))
            if url not in sitemap:
                issues.append((tag, "not in sitemap"))
        for raw in pg.ld:
            try:
                json.loads(raw)
            except Exception as e:
                issues.append((tag, f"invalid JSON-LD: {e}"))
        for href, target in pg.hreflang:
            if not exists(target):
                issues.append((tag, f"hreflang {href} target missing: {target}"))
        for img in pg.imgs:
            if "alt" not in img:
                issues.append((tag, f"img without alt: {img.get('src', '')[:60]}"))
        for href in pg.links:
            if href.startswith(("mailto:", "tel:", "#", "javascript:")):
                continue
            full = urljoin(url, href.split("#")[0])
            if urlparse(full).netloc in ("", urlparse(SITE).netloc) and not exists(full):
                issues.append((tag, f"broken link {href}"))
    for u in sorted(sitemap - indexable):
        issues.append(("sitemap.xml", f"lists non-indexable or missing page {u}"))
    seen = set()
    for tag, msg in issues:
        if (tag, msg) not in seen:
            seen.add((tag, msg))
            print(f"{tag}: {msg}")
    print(f"\n{len(pages)} pages checked, {len(indexable)} indexable, {len(seen)} issues")


if __name__ == "__main__":
    main()
