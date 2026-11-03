"""Lint blog posts against content/BLOG-RULES.md.   python3 _build/validate.py

Errors fail the build (CI blocks the deploy); warnings are advisory.
"""
import datetime
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402
import md  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = [r"\bbest (breast )?surgeon\b", r"\bleading\b", r"\bworld[- ]class\b", r"\bguarantee[ds]? (results?|outcomes?|success)\b", r"\bpain[- ]free (surgery|procedure|recovery)\b",
          r"\b100% (success|safe)\b", r"\bno risk\b", r"\brisk[- ]free\b", r"\bnumber one\b", r"\b#1\b", r"\btop surgeon\b",
          r"\bmiracle\b", r"\brevolutionary\b", r"\bcutting[- ]edge\b"]
STANDARD_FROM = datetime.date(2026, 11, 4)  # posts dated from here must meet the full standard
VALID_LINKS = ({f"~/procedures/{p['slug']}/" for p in C.PROCEDURES} | {f"~/locations/{l['slug']}/" for l in C.LOCATIONS} |
               {"~/", "~/procedures/", "~/locations/", "~/biography/", "~/reviews/", "~/podcast/", "~/booking/", "~/second-opinion/", "~/news/"})


def main():
    today = datetime.date.fromisoformat(os.environ.get("BUILD_DATE", datetime.date.today().isoformat()))
    posts = md.load_posts(os.path.join(ROOT, "content", "blog"), today)
    slugs = {p["slug"] for p in posts}
    errors, warns = [], []
    for slug, n in Counter(p["slug"] for p in posts).items():
        if n > 1:
            errors.append(f"duplicate slug {slug}")
    for p in posts:
        f = p["file"]
        src = open(os.path.join(ROOT, "content", "blog", f)).read()
        body = src.split("---", 2)[2]
        E = lambda m: errors.append(f"{f}: {m}")  # noqa: E731
        W = lambda m: warns.append(f"{f}: {m}")  # noqa: E731
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["slug"]):
            E("slug must be lowercase-hyphenated")
        if not f.startswith(p["date"]):
            E(f"filename must start with the date {p['date']}")
        if not 30 <= len(p["title"]) <= 70:
            E(f"title is {len(p['title'])} chars (30–70)")
        if not 120 <= len(p["description"]) <= 160:
            E(f"description is {len(p['description'])} chars (120–160)")
        kw = p["keyword"].lower()
        first = body.strip().split("\n\n")[0].lower()
        if not any(w in p["title"].lower() for w in kw.split() if len(w) > 3):
            E("title should contain the main words of the target keyword")
        if not first.startswith("**in short:**") and p["date_obj"] >= datetime.date(2026, 10, 1):
            E("first paragraph must be an '**In short:**' direct answer (40–60 words)")
        links = re.findall(r"\]\((~/[^)]*)\)", body)
        if len(set(links)) < 3:
            E(f"needs ≥3 distinct internal links (has {len(set(links))})")
        for l in links:
            if l not in VALID_LINKS and not (l.startswith("~/news/") and l[7:-1] in slugs):
                E(f"broken internal link {l}")
        if not any(l.startswith("~/procedures/") for l in links):
            E("must link to at least one treatment page")
        for r in p["related"]:
            if r not in {x["slug"] for x in C.PROCEDURES}:
                E(f"related: unknown procedure '{r}'")
        if len(p["faqs"]) < 2:
            E("needs a '## Frequently asked questions' section with ≥2 '### ' questions")
        if p["words"] < 650:
            (E if p["date_obj"] >= STANDARD_FROM else W)(f"only {p['words']} words (min 650)")
        elif p["words"] < 900 and p["date_obj"] > today:
            W(f"{p['words']} words — aim for 900–1,600")
        if p["words"] > 2200:
            W(f"{p['words']} words — consider splitting")
        for b in BANNED:
            if re.search(b, body, re.I):
                E(f"banned claim/superlative matches /{b}/ (GMC/ASA rules)")
        if "Mr Ullah" in body and " I " not in body:
            W("write in Mr Ullah's first person ('I'), not third person")
        if src.count("\n## ") < 3:
            E("needs ≥3 H2 sections")
    by_week = Counter(p["date_obj"].isocalendar()[:2] for p in posts if p["date_obj"] > today)
    for wk, n in by_week.items():
        if n > 2:
            warns.append(f"{n} posts scheduled in ISO week {wk[1]} — spread them out")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    live = sum(p["published"] for p in posts)
    print(f"{len(posts)} posts ({live} live, {len(posts) - live} scheduled) · {len(errors)} errors · {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
