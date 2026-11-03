"""Tiny, dependency-free Markdown subset for blog posts.

Supports: front matter (key: value), ## / ### headings, paragraphs,
- and 1. lists, > blockquotes, **bold**, *italic*, [links](url), raw HTML
lines (start with "<"), and `:::note` ... `:::` callouts.
A "## Frequently asked questions" section of "### Question" + answer
paragraphs is split out so it can be rendered and marked up as FAQPage.
"""
import datetime
import glob
import os
import re
from html import escape

FAQ_HEADING = "frequently asked questions"


def inline(t):
    t = escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
    return t


def to_html(src):
    out, para, lst, ltype = [], [], [], None

    def flush():
        nonlocal para, lst, ltype
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            out.append(f"<{ltype}>" + "".join(f"<li>{inline(i)}</li>" for i in lst) + f"</{ltype}>")
            lst, ltype = [], None

    lines = src.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            flush()
        elif s.startswith(":::note"):
            flush()
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                body.append(lines[i].strip())
                i += 1
            out.append('<div class="note">' + inline(" ".join(body)) + "</div>")
        elif s.startswith("<"):
            flush()
            out.append(s)
        elif s.startswith("### "):
            flush()
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            flush()
            h = s[3:]
            slug = re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")
            out.append(f'<h2 id="{slug}">{inline(h)}</h2>')
        elif s.startswith("> "):
            flush()
            out.append(f"<blockquote><p>{inline(s[2:])}</p></blockquote>")
        elif re.match(r"^[-*] ", s):
            if para:
                flush()
            if ltype not in (None, "ul"):
                flush()
            ltype = "ul"
            lst.append(s[2:])
        elif re.match(r"^\d+\. ", s):
            if para:
                flush()
            if ltype not in (None, "ol"):
                flush()
            ltype = "ol"
            lst.append(re.sub(r"^\d+\. ", "", s))
        else:
            if lst:
                flush()
            para.append(s)
        i += 1
    flush()
    return "\n".join(out)


def parse_front(text):
    if not text.startswith("---"):
        raise ValueError("missing front matter")
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, body.strip()


def split_faq(body):
    """Return (main_body, [(q, a_markdown)])."""
    m = re.search(r"^## +" + FAQ_HEADING + r"\s*$", body, re.I | re.M)
    if not m:
        return body, []
    main, faq_src = body[: m.start()], body[m.end():]
    faqs = []
    for block in re.split(r"^### +", faq_src, flags=re.M)[1:]:
        q, _, a = block.partition("\n")
        faqs.append((q.strip(), a.strip()))
    return main.strip(), faqs


REQUIRED = ["title", "slug", "date", "description", "keyword", "category"]


def load_posts(folder, today):
    """All posts, with `published` set from the date (future = scheduled)."""
    posts = []
    for path in sorted(glob.glob(os.path.join(folder, "*.md"))):
        meta, body = parse_front(open(path).read())
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            raise ValueError(f"{os.path.basename(path)}: missing {missing}")
        d = datetime.date.fromisoformat(meta["date"])
        main, faqs = split_faq(body)
        words = len(re.findall(r"\w+", body))
        posts.append({
            **meta,
            "file": os.path.basename(path),
            "date_obj": d,
            "published": d <= today and meta.get("draft", "false") != "true",
            "html": to_html(main),
            "faqs": [(q, to_html(a)) for q, a in faqs],
            "faqs_text": [(q, re.sub(r"\s+", " ", re.sub(r"[*\[\]]|\(http[^)]*\)|\(~/[^)]*\)", "", a))) for q, a in faqs],
            "words": words,
            "minutes": max(3, round(words / 220)),
            "related": [r.strip() for r in meta.get("related", "").split(",") if r.strip()],
        })
    posts.sort(key=lambda p: p["date_obj"], reverse=True)
    return posts
