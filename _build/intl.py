"""Translated landing pages: /bn/ (Bangla) and /ar/ (Arabic).

Separate, self-contained pages reached from the footer, the language selector and Google
(hreflang). Facts mirror _build/content.py; keep both in step when anything changes.
"""
import json
import os
from html import escape

import content as C
from layout import POSTNOM, ROOT, SITE, SITEMAP, asset_v, picture

LANGS = {
    "en": ("English", "/"),
    "bn": ("বাংলা", "/bn/"),
    "ar": ("العربية", "/ar/"),
}

FONTS = {
    "bn": "family=Noto+Sans+Bengali:wght@400..900",
    "ar": "family=Noto+Naskh+Arabic:wght@400..700&family=Noto+Sans+Arabic:wght@300..700",
}

T = {
    "bn": {
        "title": "মি. জাকের উল্লাহ | লন্ডনের কনসালটেন্ট ব্রেস্ট সার্জন",
        "desc": "লন্ডন ও এসেক্সের কনসালটেন্ট অনকোপ্লাস্টিক ব্রেস্ট সার্জন মি. মোঃ জাকের উল্লাহ FRCS। বাংলা, ইংরেজি ও আরবিতে কনসালটেশন। একই দিনে পরীক্ষা ও প্রাথমিক ফলাফল।",
        "brand": "মি. জাকের উল্লাহ", "brand_sub": "কনসালটেন্ট ব্রেস্ট সার্জন",
        "call": "কল করুন",
        "eyebrow": "কনসালটেন্ট অনকোপ্লাস্টিক ব্রেস্ট সার্জন · লন্ডন",
        "h1": "মি. মোঃ জাকের উল্লাহ",
        "sub": "লন্ডনের হুইপস ক্রস ইউনিভার্সিটি হাসপাতালের ব্রেস্ট ইউনিটের ক্লিনিক্যাল লিড। তিনি বাংলা, ইংরেজি ও আরবিতে রোগী দেখেন।",
        "cta_call": "অ্যাপয়েন্টমেন্টের জন্য কল করুন", "cta_mail": "ইমেইল করুন",
        "say": "স্তনের বেশিরভাগ সমস্যা গুরুতর কিছু নয়। মি. উল্লাহর ওয়ান-স্টপ ক্লিনিকে একই দিনে পরীক্ষা, ইমেজিং ও প্রাথমিক ফলাফল পাওয়া যায়, এবং যিনি আপনাকে দেখেন, পুরো চিকিৎসায় তিনিই আপনার পাশে থাকেন।",
        "about_h": "মি. উল্লাহর পরিচয়",
        "about": "মি. উল্লাহ ৩০ বছরেরও বেশি সময় ধরে সার্জারিতে কাজ করছেন। তিনি লন্ডনের দ্য রয়্যাল মার্সডেন, সেন্ট মেরি'স ও দ্য রয়্যাল ফ্রি হাসপাতালে প্রশিক্ষণ নিয়েছেন এবং ২০১২ সাল থেকে বার্টস হেলথ এনএইচএস ট্রাস্টের কনসালটেন্ট। হুইপস ক্রস হাসপাতালে তিনি ওয়ান-স্টপ ব্রেস্ট ক্লিনিক চালু করেছেন। তিনি FRCS ডিগ্রিধারী এবং জেনারেল মেডিক্যাল কাউন্সিলে (GMC 4368515) নিবন্ধিত।",
        "facts": [("৩০+", "বছর সার্জারিতে"), ("৫.০", "রোগীদের রেটিং, iWantGreatCare"), ("Bupa", "প্ল্যাটিনাম কনসালটেন্ট")],
        "tx_h": "তিনি কী চিকিৎসা করেন",
        "tx": [
            ("স্তনের উপসর্গ", "নতুন চাকা (লাম্প), ব্যথা বা অন্য কোনো পরিবর্তন: ওয়ান-স্টপ ক্লিনিকে দ্রুত পরীক্ষা।"),
            ("স্তন ক্যান্সার", "স্তন সংরক্ষণকারী সার্জারি, ম্যাস্টেক্টমি ও লিম্ফ নোড সার্জারি, শুরু থেকেই চূড়ান্ত আকৃতির কথা মাথায় রেখে পরিকল্পিত।"),
            ("পুনর্গঠন ও আকৃতি", "ক্যান্সার চিকিৎসার সময় বা পরে স্তন পুনর্গঠন, স্তন ছোট করা (রিডাকশন) ও ফ্যাট গ্রাফটিং।"),
            ("পুরুষদের ও সাধারণ সার্জারি", "পুরুষের স্তন বৃদ্ধি (গাইনোকোমাস্টিয়া), ল্যাপারোস্কোপিক হার্নিয়া ও পিত্তথলির সার্জারি, এবং চামড়ার নিচের চাকা।"),
        ],
        "cl_h": "তিনটি প্রাইভেট ক্লিনিক",
        "cl": {"buckhurst-hill-essex": "বাকহার্স্ট হিল, এসেক্স। উডফোর্ড গ্রিন, লাফটন ও চিগওয়েলের কাছে, সাইটে পার্কিং আছে।",
               "harley-street": "হার্লি স্ট্রিট, সেন্ট্রাল লন্ডন।",
               "city-of-london": "সিটি অফ লন্ডন, সেন্ট বার্থোলোমিউ'স হাসপাতালের পাশে।"},
        "vid_h": "ভিডিও কনসালটেশন ও দ্বিতীয় মতামত",
        "vid": "যুক্তরাজ্যের যেকোনো জায়গা থেকে, এমনকি বিদেশ থেকেও, আপনি ভিডিও বা টেলিফোনে মি. উল্লাহর সাথে কথা বলতে পারেন, সাধারণত ২৪ থেকে ৪৮ ঘণ্টার মধ্যে। আপনার রিপোর্ট ও স্ক্যান দেখে তিনি লিখিত মতামত দেন, যা আপনি আপনার নিজের ডাক্তারকে দেখাতে পারেন।",
        "bk_h": "কীভাবে অ্যাপয়েন্টমেন্ট নেবেন",
        "bk": ["প্রাইভেট সেক্রেটারিকে কল বা ইমেইল করুন।",
               "ইনস্যুরেন্স থাকলে সাধারণত জিপির রেফারেল ও ইনস্যুরারের অনুমোদন লাগে। নিজে খরচ দিলে সরাসরি বুক করতে পারেন।",
               "আপনার পছন্দের ক্লিনিকে, বা ভিডিওতে, মি. উল্লাহর সাথে দেখা করুন।"],
        "bk_note": "বুক করার সময় জানিয়ে দিন যে আপনি বাংলায় কথা বলতে চান।",
        "sec": "প্রাইভেট সেক্রেটারি",
        "faq_h": "সাধারণ প্রশ্ন",
        "faq": [
            ("আমি কি বাংলায় কথা বলতে পারব?", "হ্যাঁ। মি. উল্লাহ বাংলা, ইংরেজি ও আরবিতে কনসালটেশন করেন। বুক করার সময় জানিয়ে দিন।"),
            ("তাঁকে 'ডাক্তার' না বলে 'মিস্টার' বলা হয় কেন?", "যুক্তরাজ্যে যেসব ডাক্তার রয়্যাল কলেজ অফ সার্জনসের ফেলোশিপ (FRCS) অর্জন করেন, তাঁদের ঐতিহ্যগতভাবে 'মিস্টার' বলা হয়। এটি উচ্চতর সার্জিক্যাল প্রশিক্ষণ সম্পন্ন করার চিহ্ন।"),
            ("জিপির রেফারেল কি লাগবে?", "ইনস্যুরেন্স ব্যবহার করলে সাধারণত লাগে। নিজে খরচ দিলে রেফারেল ছাড়াই বুক করা যায়।"),
            ("ফলাফল কি একই দিনে পাওয়া যায়?", "ওয়ান-স্টপ ক্লিনিকে ইমেজিং ও প্রাথমিক ফলাফল সাধারণত একই দিনে দেওয়া হয়। বায়োপসি লাগলে তার ফলাফল কয়েক দিন পরে আসে।"),
            ("তিনি কি এনএইচএস রোগীও দেখেন?", "হ্যাঁ। তিনি হুইপস ক্রস ইউনিভার্সিটি হাসপাতালের এনএইচএস ব্রেস্ট ইউনিটের ক্লিনিক্যাল লিড। এনএইচএস রেফারেল আপনার জিপির মাধ্যমে হয়।"),
        ],
        "en_link": "সম্পূর্ণ ওয়েবসাইট (ইংরেজি)", "privacy": "গোপনীয়তা নীতি",
        "legal": "এই পৃষ্ঠার তথ্য সাধারণ তথ্য, কনসালটেশনের বিকল্প নয়। জরুরি অবস্থায় 999 নম্বরে কল করুন।",
    },
    "ar": {
        "title": "الجرّاح محمد ذاكر الله | استشاري جراحة الثدي في لندن",
        "desc": "الجرّاح محمد ذاكر الله FRCS، استشاري جراحة الثدي الأورامية التجميلية في لندن. استشارات بالعربية والإنجليزية والبنغالية، واستشارات بالفيديو للمرضى من الخارج.",
        "brand": "محمد ذاكر الله", "brand_sub": "استشاري جراحة الثدي",
        "call": "اتصل",
        "eyebrow": "استشاري جراحة الثدي الأورامية التجميلية · لندن",
        "h1": "الجرّاح محمد ذاكر الله",
        "sub": "القائد السريري لوحدة الثدي في مستشفى ويبس كروس الجامعي في لندن. يستقبل المرضى بالعربية والإنجليزية والبنغالية.",
        "cta_call": "اتصل لحجز موعد", "cta_mail": "راسلنا بالبريد الإلكتروني",
        "say": "معظم أعراض الثدي لا تكون خطيرة. في عيادات الجرّاح ذاكر الله ذات الزيارة الواحدة تُجرى الفحوصات والتصوير وتحصل على النتائج الأولية في اليوم نفسه، ويتابعك الجرّاح نفسه طوال فترة علاجك.",
        "about_h": "نبذة عن الجرّاح",
        "about": "يعمل الجرّاح ذاكر الله في الجراحة منذ أكثر من ثلاثين عاماً. تدرّب في لندن في مستشفيات رويال مارسدن وسانت ماري ورويال فري، ويعمل استشارياً في هيئة بارتس الصحية التابعة لهيئة الخدمات الصحية الوطنية البريطانية (NHS) منذ عام 2012. أسّس عيادة الثدي ذات الزيارة الواحدة في مستشفى ويبس كروس. حاصل على زمالة الكلية الملكية للجرّاحين (FRCS)، ومسجّل لدى المجلس الطبي العام البريطاني برقم GMC 4368515.",
        "facts": [("+30", "عاماً في الجراحة"), ("5.0", "تقييم المرضى على iWantGreatCare"), ("Bupa", "استشاري بلاتيني")],
        "tx_h": "مجالات العلاج",
        "tx": [
            ("أعراض الثدي", "كتلة جديدة أو ألم أو أي تغيّر، يُقيَّم بسرعة في عيادة الزيارة الواحدة."),
            ("سرطان الثدي", "جراحة الحفاظ على الثدي، واستئصال الثدي، وجراحة الغدد الليمفاوية، مع التخطيط للشكل النهائي منذ البداية."),
            ("إعادة البناء والتشكيل", "إعادة بناء الثدي وتصغيره وحقن الدهون الذاتية، أثناء علاج السرطان أو بعده."),
            ("جراحة الرجال والجراحة العامة", "تضخّم الثدي عند الرجال (التثدّي)، وجراحة الفتق والمرارة بالمنظار، وإزالة الكتل تحت الجلد."),
        ],
        "cl_h": "ثلاث عيادات خاصة",
        "cl": {"buckhurst-hill-essex": "باكهرست هيل، إسكس، على أطراف لندن، مع موقف للسيارات.",
               "harley-street": "شارع هارلي في وسط لندن، الحي الطبي المعروف في العاصمة.",
               "city-of-london": "مدينة لندن، بجوار مستشفى سانت بارثولوميو."},
        "vid_h": "للمرضى من المملكة العربية السعودية ودول الخليج",
        "vid": "يمكنك التحدث مع الجرّاح ذاكر الله بالفيديو أو الهاتف قبل السفر، وعادةً خلال 24 إلى 48 ساعة. يراجع تقاريرك وصور الأشعة ويقدّم رأياً مكتوباً يمكنك مشاركته مع أطبائك. وإذا قررت العلاج في لندن، يساعدك فريق العيادة في تنظيم مواعيد الاستشارة والفحوصات والجراحة.",
        "bk_h": "كيف تحجز موعداً",
        "bk": ["اتصل بالسكرتيرة الخاصة أو راسلها بالبريد الإلكتروني.",
               "إذا كان لديك تأمين صحي، تحتاج عادةً إلى إحالة من طبيبك وموافقة شركة التأمين. ويمكن لمن يدفع بنفسه الحجز مباشرة.",
               "قابل الجرّاح ذاكر الله في العيادة التي تختارها، أو عبر الفيديو."],
        "bk_note": "اذكر عند الحجز أنك تفضّل التحدث بالعربية.",
        "sec": "السكرتيرة الخاصة",
        "faq_h": "أسئلة شائعة",
        "faq": [
            ("هل يمكنني التحدث بالعربية؟", "نعم. يجري الجرّاح ذاكر الله الاستشارات بالعربية والإنجليزية والبنغالية. يُرجى ذكر ذلك عند الحجز."),
            ("لماذا يُلقّب بـ Mr وليس Dr؟", "في بريطانيا يُلقّب الأطباء الحاصلون على زمالة الكلية الملكية للجرّاحين (FRCS) بلقب Mr بدلاً من Dr، وهو تقليد يدلّ على إتمام التدريب الجراحي المتقدّم."),
            ("هل يمكنني الحصول على رأي طبي ثانٍ من خارج بريطانيا؟", "نعم. أرسل التقارير وصور الأشعة وتقارير الخزعة، ويناقشها معك الجرّاح ذاكر الله عبر الفيديو ثم يرسل لك رأياً مكتوباً. يُفضّل أن تكون التقارير بالإنجليزية أو مترجمة."),
            ("هل أحصل على النتائج في اليوم نفسه؟", "في عيادة الزيارة الواحدة تُعطى نتائج التصوير والنتائج الأولية عادةً في اليوم نفسه. أما نتائج الخزعة، إن لزمت، فتصدر بعد أيام قليلة."),
        ],
        "en_link": "الموقع الكامل (بالإنجليزية)", "privacy": "سياسة الخصوصية",
        "legal": "المعلومات في هذه الصفحة عامة ولا تغني عن الاستشارة الطبية. في حالات الطوارئ في بريطانيا اتصل بالرقم 999.",
    },
}


def hreflang():
    return "".join(f'<link rel="alternate" hreflang="{k}" href="{SITE}{u}">' for k, (_, u) in LANGS.items()) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'


def page(lang):
    t = T[lang]
    rtl = lang == "ar"
    path = f"{lang}/"
    canonical = f"{SITE}/{path}"
    cur = ' aria-current="page"'
    langs = "".join(f'<a href="{"../" if k == "en" else "../" + k + "/"}" hreflang="{k}" lang="{k}"{cur if k == lang else ""}>{n}</a>' for k, (n, _) in LANGS.items())
    clinics = "".join(f'<div class="ic"><h3 dir="ltr">{escape(l["name"])}</h3><p>{t["cl"][l["slug"]]}</p><p class="ad" dir="ltr">{l["street"]}, {l["locality"]} {l["postcode"]}</p></div>' for l in C.LOCATIONS)
    tx = "".join(f'<div class="pc" data-r style="--d:{i}"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(t["tx"]))
    facts = "".join(f'<div><dt dir="ltr">{a}</dt><dd>{b}</dd></div>' for a, b in t["facts"])
    steps = "".join(f'<li><span class="n" dir="ltr">{i + 1}</span><p>{s}</p></li>' for i, s in enumerate(t["bk"]))
    faqs = "".join(f'<details class="iq"><summary>{q}</summary><p>{a}</p></details>' for q, a in t["faq"])
    contact = f'''<div class="icontact"><span class="k">{t["sec"]}</span><a class="big" href="tel:{C.SEC_TEL}" dir="ltr">{C.SEC_PHONE}</a><a href="mailto:{C.SEC_EMAIL}" dir="ltr">{C.SEC_EMAIL}</a></div>'''
    schema = [
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": canonical, "inLanguage": lang, "name": t["title"], "description": t["desc"],
         "about": {"@type": "Physician", "@id": SITE + "/#physician"}, "isPartOf": {"@type": "WebSite", "url": SITE + "/"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    img = f"assets/og/{lang}.jpg" if os.path.exists(os.path.join(ROOT, "assets", "og", f"{lang}.jpg")) else "assets/img/og-card.jpg"
    html = f'''<!DOCTYPE html>
<html lang="{lang}" dir="{"rtl" if rtl else "ltr"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(t["title"])}</title>
<meta name="description" content="{escape(t["desc"])}">
<link rel="canonical" href="{canonical}">
{hreflang()}
<meta name="theme-color" content="#1a0f08">
<meta property="og:title" content="{escape(t["title"])}"><meta property="og:description" content="{escape(t["desc"])}">
<meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="{"ar_SA" if rtl else "bn_BD"}">
<meta property="og:image" content="{SITE}/{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/img/icon-32.png"><link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[lang]}&display=swap">
<link rel="stylesheet" href="../assets/css/main.css?v={asset_v("assets/css/main.css")}">
{blocks}
</head>
<body class="intl intl-{lang}">
<header class="ih"><div class="wrap ih-in">
  <a class="ib" href="./"><span>{t["brand"]}</span><small>{t["brand_sub"]}</small></a>
  <nav class="langs" aria-label="Language">{langs}</nav>
  <a class="btn coral ih-call" href="tel:{C.SEC_TEL}">{t["call"]}</a>
</div></header>
<main id="main">
<section class="bio-hero" data-hero><div class="wrap"><div class="bh">
  <div class="bh-copy"><span class="ie">{t["eyebrow"]}</span><h1 class="h-anim">{t["h1"]}</h1><p class="bh-sub">{t["sub"]}</p>
    <div class="actions mt-3"><a class="btn coral" href="tel:{C.SEC_TEL}">{t["cta_call"]}</a><a class="btn glass" href="mailto:{C.SEC_EMAIL}">{t["cta_mail"]}</a></div></div>
  <figure class="bh-fig">{picture("zu-navy", t["h1"], "(min-width: 64rem) 44vw, 100vw", [600, 900, 1300], 1020, 1542, lazy=False).replace("~/", "../")}</figure>
</div></div></section>

<section class="say"><div class="wrap"><p class="say-t isay" data-r>{t["say"]}</p></div></section>

<section class="meet"><div class="wrap"><div class="meet-t" data-r><h2>{t["about_h"]}</h2><p class="lede mt-2">{t["about"]}</p><dl class="meet-k">{facts}</dl></div></div></section>

<section class="band white"><div class="wrap"><div class="sec-h" data-r><h2>{t["tx_h"]}</h2></div><div class="pcs">{tx}</div></div></section>

<section class="band"><div class="wrap"><div class="sec-h" data-r><h2>{t["cl_h"]}</h2></div><div class="ics" data-r>{clinics}</div></div></section>

<section class="band deep"><div class="wrap duo"><div data-r><h2>{t["vid_h"]}</h2><p class="lede mt-2" style="color:var(--on-deep-2)">{t["vid"]}</p></div>
  <figure class="duo-img" data-r><video class="lv" muted loop playsinline preload="none" poster="../assets/video/loop-podcast.jpg" data-lazy aria-hidden="true"><source data-src="../assets/video/loop-podcast.webm" type="video/webm"><source data-src="../assets/video/loop-podcast.mp4" type="video/mp4"></video></figure></div></section>

<section class="band peach"><div class="wrap duo"><div data-r><h2>{t["bk_h"]}</h2><ol class="isteps mt-3">{steps}</ol><p class="mt-2 stone">{t["bk_note"]}</p></div><div data-r>{contact}</div></div></section>

<section class="band white"><div class="wrap"><div class="sec-h" data-r><h2>{t["faq_h"]}</h2></div><div class="iqs">{faqs}</div></div></section>
</main>
<footer class="ifoot"><div class="wrap">
  <div class="ifoot-t"><b>{t["brand"]}</b> · <span dir="ltr">Mr Md Zaker Ullah {POSTNOM}</span> · <a href="https://www.gmc-uk.org/registrants/4368515" dir="ltr">GMC 4368515</a></div>
  <nav class="langs" aria-label="Language">{langs}</nav>
  <div class="ifoot-l"><a href="../">{t["en_link"]}</a> · <a href="../privacy/">{t["privacy"]}</a></div>
  <p class="small stone mt-2">{t["legal"]}</p>
</div></footer>
<script src="../assets/js/main.js?v={asset_v("assets/js/main.js")}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, lang, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    SITEMAP.append((canonical, "0.7"))


def build_intl():
    for lang in T:
        page(lang)
