# Blog rules for drzakerullah.com

Every post on this site is published under the name of a practising GMC-registered surgeon
and is a "Your Money or Your Life" (YMYL) medical page. Google holds these to the highest
standard of E-E-A-T, and the GMC and ASA/CAP code apply to everything we say. These rules
exist so posts rank **and** stay safe. `python3 _build/validate.py` enforces the
mechanical ones; the build fails if any error remains.

## 1. File & front matter

One file per post: `content/blog/YYYY-MM-DD-short-slug.md` (filename starts with the publish date).

```yaml
---
title: Lumpectomy or mastectomy? How the decision is really made   # 30 to 70 chars, contains keyword words
slug: lumpectomy-vs-mastectomy                                      # lowercase-hyphen, keyword-led, never changes once live
date: 2026-11-10                                                    # publish date, future = scheduled
reviewed: 2026-11-03                                                # date the content was medically checked
description: 120 to 160 chars. Answers the query + says who is answering. No clickbait.
keyword: lumpectomy vs mastectomy                                   # ONE primary target query
category: Breast cancer                                             # see categories below
related: breast-cancer-surgery, breast-reconstruction               # procedure slugs from _build/content.py
featured: West Essex Life                                            # optional: only if the article really appeared in that publication
image_query: doctor patient conversation                             # Unsplash search for the header photo: calm, non-clinical, no bodies or ribbons
---
```

Optional: `updated: YYYY-MM-DD` (when meaningfully revised), `draft: true` (never publish).

**Categories** (use these exactly): Breast symptoms · Breast cancer · Reconstruction & cosmetic ·
Men's breast health · Private care explained · Local clinics · General surgery · Living with & after.

## 2. Structure (in this order)

1. **`**In short:**` paragraph**, 40 to 60 words that fully answer the query. This is what Google's
   AI Overviews and LLMs quote. No preamble.
2. One or two short paragraphs of context in Mr Ullah's voice ("In clinic I often see…").
3. **3 to 6 `##` sections**, question-shaped or task-shaped where natural ("What happens on the day",
   "Is it safe?"). Use `###` sparingly. Lists for symptoms, steps and options.
4. Optional `:::note` callout for safety-netting or a local pointer.
5. **`## Frequently asked questions`**, 2 to 4 `### Question?` + 1 to 3 sentence answers. Real
   "People also ask" phrasings. These become FAQPage schema automatically.

Do **not** add a disclaimer, author box or CTA, the template adds them.

## 3. Length & depth

- New posts: **900 to 1,600 words** (hard minimum 650). Depth beats length, never pad.
- Must contain at least one thing a generic health site would not: a clinical nuance, a UK
  pathway detail (NHS two-week wait, insurer pre-authorisation, NICE), a local detail
  (clinic days, parking, which hospital), or a "what I tell patients" insight.

## 4. Voice

- **First person as Mr Ullah** ("I", "my patients"), calm, warm, precise. Plain English at about
  a reading age of 12; explain every medical term the first time.
- Always "Mr Ullah" or "Mr Zaker Ullah", never "Dr". He does not offer breast augmentation.
- British English (tumour, oesophagus, anaesthetic, centre, organise, programme).
- Reassure honestly: lead with the likely benign answer where true, but always safety-net.
- Short sentences. No hype, no fear-mongering, no exclamation marks.
- **No em dashes or en dashes, ever.** Use a comma, colon or full stop instead, and "to" for ranges
  ("two to three weeks"). The validator rejects any post containing them.

## 5. Medical accuracy (non-negotiable)

- Only state facts that are consistent with NHS, NICE, Cancer Research UK, Breast Cancer Now
  or the Association of Breast Surgery guidance. Use ranges and "usually", not false precision.
- **Never** invent statistics, studies, patient stories, quotes, prices or waiting times.
  If a number matters and you are not certain of it, leave it out or say "most" / "a minority".
- Never give individual advice. Every post must push readers with symptoms towards assessment.
- Do not quote prices (they are set by each hospital and change).
- Facts about Mr Ullah himself must come from `_build/content.py` or the biography page only.

## 6. Compliance (GMC Good Medical Practice & ASA/CAP)

Banned (validator enforces): "best surgeon", "leading", "world-class", "number one/#1",
"top surgeon", "guaranteed results", "pain-free surgery", "100% success/safe", "no risk",
"risk-free", "miracle", "revolutionary", "cutting-edge". Also never:
- disparage other doctors or hospitals;
- use patient testimonials inside posts (reviews live on /reviews/ only, verbatim, from iWGC);
- promote cosmetic surgery with time-limited offers, or target under-18s for cosmetic procedures;
- use before/after images.

## 7. SEO

- **One primary keyword per post**, and no two posts may target the same keyword (check
  `content/content-plan.md` and existing posts). Put it in the title, slug, description,
  `In short` paragraph and one `##` heading, naturally.
- **≥3 internal links** using site-root paths `[text](~/procedures/slug/)`, including
  **at least one treatment page**, plus where relevant a clinic page (`~/locations/…/`),
  `~/second-opinion/`, `~/booking/`, `~/podcast/` or an earlier post (`~/news/slug/`).
  Descriptive anchor text, never "click here".
- Local intent: mention the real clinic(s) where it helps the reader, Bupa Wharfside Health Centre, Canary Wharf E14,
  Nuffield Health St Bartholomew's EC1, Nuffield Health The Holly, Buckhurst Hill IG9.
  **Never** create pages or posts for places he does not practise (doorway pages).
- No external links needed; if used, only to NHS, NICE, CRUK, Breast Cancer Now or ABS.

## 8. Scheduling

- Default cadence: **one post per week, Tuesday**, unless asked otherwise. Max two per ISO week.
- Mix each month: ≥1 symptom/worry post, ≥1 treatment/recovery post, ≥1 commercial or local
  post (private care, clinic guide, second opinion), and a men's health or general surgery
  post at least every 6 weeks.
- Pick topics from `content/content-plan.md` (top of the backlog first) and mark them
  `scheduled` with the date when written.
