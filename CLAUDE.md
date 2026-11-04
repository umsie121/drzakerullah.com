# drzakerullah.com: instructions for Claude

Private-practice website for **Mr Md Zaker Ullah FRCS**, consultant oncoplastic breast & general
surgeon (London & Essex). Goal: rank for "breast surgeon near me / London / Essex / Harley Street"
and treatment queries, and convert visitors into consultations. It is a YMYL medical site, so
accuracy and GMC/ASA compliance outrank everything else.

## How the site works

- Static site, no dependencies. **Generated HTML lives in the repo root and is the deployed site.**
- Source: `_build/content.py` (facts, treatments, clinics, reviews, podcast), `_build/build.py`
  (page templates), `_build/layout.py` (header/footer/head), `content/blog/*.md` (posts).
- Build: `python3 _build/build.py` · Validate posts: `python3 _build/validate.py`
- Preview: `python3 -m http.server 8765` (or the `site` launch config).
- Never hand-edit generated `index.html` files, edit the source and rebuild.
- Deploy: push to `main`. GitHub Actions validates, builds and deploys to GitHub Pages, and
  **re-runs daily at 06:00 UTC**, so posts with a future `date` go live automatically on that day.

## "Write & schedule N weeks of blogs"

When asked for blog posts:

1. Read `content/BLOG-RULES.md` (mandatory) and `content/content-plan.md`.
2. Pick the next N backlog topics, balancing categories per the rules (§8). Skip any whose
   keyword overlaps an existing post.
3. Dates: one post per week on **Tuesdays**, starting from the first Tuesday after the latest
   scheduled post (or after today if none).
4. Write each post to `content/blog/YYYY-MM-DD-slug.md` following the rules exactly, "In short"
   answer first, Mr Ullah's first-person voice, 900 to 1,600 words, ≥3 internal links, FAQ section.
5. Update each topic's status in `content/content-plan.md` to `scheduled YYYY-MM-DD`.
6. Run `python3 _build/validate.py` and fix **all** errors (and word-count warnings), then
   `python3 _build/build.py`. Scheduled posts are validated but not built until their date.
7. Commit ("Schedule blog posts: <first date> to <last date>") and push to `main`.
8. Report the schedule as a table (date · title · keyword).

Medical facts: if unsure, leave it out. Never invent statistics, prices, study results, patient
stories or facts about Mr Ullah.

## Positioning

- Lead with The Holly, Buckhurst Hill, for Woodford Green, Loughton and Chigwell; then Harley Street and St Bartholomew's.
- Mention Bupa Platinum consultant (fee-assured, Open Referral network) wherever insurance comes up.
- Show review quality as "5.0, 100% five-star", never the raw review count.

## Facts still to confirm with the practice (do not "fix" by guessing)

- Private secretary phone/email (from Bupa Finder; name spelling Wiles/Willes unconfirmed).
- Direct booking numbers for The Harley Street Clinic and Nuffield St Bartholomew's.
- Secretary email: old site gave juliet.willes@nhs.net, Bupa gives juliet.willes@nuffieldhealth.com (used).
- He no longer consults at Spire London East (confirmed). Do not list it.
- Fees are not published anywhere (not on PHIN, Bupa, Nuffield, Doctify or Top Doctors). Do not invent prices; booking goes via partners who quote them. If he submits fees to PHIN, add a fees table.
- No ICO registration number is shown on the privacy policy; add it once confirmed.
- He does not offer breast augmentation. Never write about it as a service.
- Always "Mr" Ullah, never "Dr", except in verbatim reviews.
- Fee-assured status per insurer; insurer list is from his Nuffield profile.
