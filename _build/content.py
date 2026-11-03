"""Structured content: procedures, locations and practice facts.

Facts here must be verifiable. Anything marked TODO needs confirming with
Mr Ullah's office before it is relied on.
"""

IWGC = "https://www.iwantgreatcare.org/doctors/mr-md-zaker-ullah"

INSURERS = ["Bupa", "Bupa Global", "AXA Health", "Aviva", "Vitality", "WPA", "Cigna", "Healix", "Health-on-Line"]

# Private secretary (Nuffield Health The Holly) — source: Bupa Finder profile.
# TODO confirm number/email with the office before launch.
SEC_PHONE = "020 8936 1263"
SEC_TEL = "+442089361263"
SEC_EMAIL = "juliet.willes@nuffieldhealth.com"
PHONE_LABEL = "Private secretary: 020 8936 1263"
PHONE_TEL = SEC_TEL

LOCATIONS = [
    {
        "slug": "harley-street",
        "name": "The Harley Street Clinic",
        "short": "Harley Street",
        "area": "Marylebone, London W1",
        "street": "35 Weymouth Street",
        "locality": "London",
        "region": "Greater London",
        "postcode": "W1G 8BJ",
        "phone": None,  # no Mr Ullah-specific HCA line verified; book via secretary
        "tel": None,
        "operator": "HCA Healthcare UK",
        "kw": "Breast Surgeon Harley Street",
        "h1": "Breast surgeon on <em>Harley Street</em>",
        "title": "Breast Surgeon Harley Street, London W1 | Mr Zaker Ullah",
        "desc": "Consultant oncoplastic breast surgeon at The Harley Street Clinic, London W1. Breast lump assessment, breast cancer surgery, reconstruction and reduction with Mr Zaker Ullah FRCS.",
        "travel": "A short walk from Regent's Park, Great Portland Street and Oxford Circus stations, in the heart of London's historic medical district.",
        "serves": ["Marylebone", "Fitzrovia", "Mayfair", "Westminster", "Camden", "St John's Wood", "Kensington", "Paddington", "Central London"],
        "intro": "The Harley Street Clinic is one of London's best-known private hospitals, with dedicated cancer, imaging and surgical facilities under one roof. Mr Ullah consults and operates here for patients who live or work in central and west London, and for those travelling into the capital for a specialist opinion.",
        "why": [
            "Consultation, mammography, ultrasound and biopsy available on site",
            "Full inpatient and day-case operating theatres for breast cancer, reconstruction and reduction surgery",
            "Access to HCA's specialist oncology and multidisciplinary teams",
            "Convenient for patients travelling from across the UK and overseas",
        ],
    },
    {
        "slug": "city-of-london",
        "name": "Nuffield Health at St Bartholomew's Hospital",
        "short": "City of London",
        "area": "Smithfield, London EC1",
        "street": "38 Giltspur Street",
        "locality": "London",
        "region": "Greater London",
        "postcode": "EC1A 7BS",
        "phone": "020 3386 9000",  # Nuffield St Bartholomew's main line — confirm
        "tel": "+442033869000",
        "operator": "Nuffield Health",
        "kw": "Breast Surgeon City of London",
        "h1": "Breast surgeon in the <em>City of London</em>",
        "title": "Breast Surgeon City of London EC1 | Mr Zaker Ullah FRCS",
        "desc": "Private breast surgeon in the City of London at Nuffield Health St Bartholomew's. Rapid breast lump clinics, breast cancer surgery and second opinions with Mr Zaker Ullah FRCS.",
        "travel": "Within the historic St Bartholomew's Hospital site, a few minutes from Farringdon, Barbican and St Paul's stations — easy to reach from the City, Canary Wharf and the Elizabeth line.",
        "serves": ["The City", "Clerkenwell", "Islington", "Shoreditch", "Canary Wharf", "Southwark", "Hackney", "Tower Hamlets", "Holborn"],
        "intro": "Nuffield Health's private hospital at St Bartholomew's sits within Britain's oldest hospital site, alongside one of Europe's leading cancer centres. It is ideal for patients who work in the City or East London and want a specialist appointment that fits around their day.",
        "why": [
            "Private hospital inside the St Bartholomew's campus",
            "Ideal for City and Canary Wharf workers — appointments that fit around the working day",
            "Consultation, imaging and day-case surgery",
            "Corporate and insured patients welcome; self-pay packages available",
        ],
    },
    {
        "slug": "buckhurst-hill-essex",
        "name": "Nuffield Health The Holly Hospital",
        "short": "The Holly, Essex",
        "area": "Buckhurst Hill, Essex IG9",
        "street": "High Road",
        "locality": "Buckhurst Hill",
        "region": "Essex",
        "postcode": "IG9 5HX",
        "phone": "020 8505 3311",
        "tel": "+442085053311",
        "operator": "Nuffield Health",
        "kw": "Breast Surgeon Essex",
        "h1": "Breast surgeon in <em>Essex</em> at The Holly",
        "title": "Breast Surgeon Essex, Buckhurst Hill | Mr Zaker Ullah FRCS",
        "desc": "Private breast surgeon in Essex at The Holly Private Hospital, Buckhurst Hill IG9. One-stop breast clinics, breast cancer surgery, reconstruction, reduction and gynaecomastia with Mr Zaker Ullah FRCS.",
        "travel": "On the High Road in Buckhurst Hill on the edge of Epping Forest, with on-site parking and Buckhurst Hill Central line station nearby. Easily reached from the M11 and M25.",
        "serves": ["Buckhurst Hill", "Loughton", "Chigwell", "Woodford", "Epping", "Theydon Bois", "Waltham Abbey", "Harlow", "Brentwood", "Chingford", "Walthamstow", "Romford"],
        "intro": "Nuffield Health The Holly Hospital is Mr Ullah's principal private base — where his private secretary is based and where the photograph on this site was taken. A calm, well-equipped hospital on the London–Essex border, it serves patients from across Essex, Hertfordshire and north-east London, and runs a Rapid Access Breast Clinic with Mr Ullah on Tuesday afternoons.",
        "clinics": "Tuesday afternoons (Rapid Access Breast Clinic) and Thursday mornings",
        "why": [
            "Rapid Access Breast Clinic with Mr Ullah on Tuesday afternoons",
            "On-site parking and easy access from the M11 and M25",
            "Outpatient clinics, imaging and full operating theatres",
            "Consultations available in English and Bengali",
        ],
    },
]

NHS_BASE = {
    "name": "Whipps Cross University Hospital",
    "trust": "Barts Health NHS Trust",
    "street": "Whipps Cross Road",
    "locality": "Leytonstone, London",
    "postcode": "E11 1NR",
}

# ------------------------------------------------------------- procedures
PROCEDURES = [
    {
        "slug": "benign-breast-conditions",
        "nav": "Breast lumps &amp; pain",
        "navdesc": "One-stop assessment of new breast symptoms",
        "tags": ["Breast lump", "Breast pain", "Cysts", "Nipple discharge"],
        "title": "Private Breast Lump Clinic London & Essex | Mr Zaker Ullah",
        "desc": "Found a breast lump or have breast pain? Private one-stop breast clinic in London & Essex: examination, mammogram/ultrasound and biopsy in a single visit with consultant breast surgeon Mr Zaker Ullah FRCS.",
        "h1": "Breast lumps, pain &amp; <em>benign breast conditions</em>",
        "lede": "Most breast symptoms turn out to be benign — but every new symptom deserves a proper answer, quickly. Mr Ullah introduced the one-stop clinic at Whipps Cross, and runs his private clinics the same way: examination, imaging and, if needed, biopsy at a single visit.",
        "glance": [("Appointment", "Usually 45–90 minutes"), ("Tests", "Examination, ultrasound and/or mammogram, biopsy if needed"), ("Results", "Imaging on the day; biopsy typically within days"), ("Referral", "GP letter needed for most insurers")],
        "sections": """
<h2>Symptoms Mr Ullah assesses</h2>
<p>Patients are most commonly seen with:</p>
<ul>
<li>A new lump or area of thickening in the breast or armpit</li>
<li>Breast pain (mastalgia) — cyclical, constant, or in one spot</li>
<li>Nipple discharge, nipple inversion or a rash on the nipple</li>
<li>Skin dimpling, puckering or redness</li>
<li>Breast cysts and fibroadenomas</li>
<li>A change in breast size or shape</li>
<li>A family history of breast cancer, and questions about personal risk</li>
</ul>
<h2>The one-stop approach</h2>
<p>The traditional route to a diagnosis — clinic, then a separate scan, then another appointment for results — stretches an anxious wait across weeks. At a one-stop clinic Mr Ullah takes a full history and examines you, arranges imaging (ultrasound and/or mammography, depending on your age and symptoms) at the same visit, and performs a needle biopsy there and then if anything needs sampling.</p>
<p>This is <strong>triple assessment</strong> — the UK gold standard for breast symptoms. Most patients leave their first appointment either fully reassured or with a clear plan.</p>
<h2>If treatment is needed</h2>
<p>Many benign conditions need no treatment once a firm diagnosis is made. Where treatment helps, Mr Ullah offers cyst aspiration, excision of symptomatic fibroadenomas or other benign lumps, duct surgery for troublesome nipple discharge, and structured, evidence-based advice for breast pain.</p>
<p>If a biopsy does show cancer, you are already under the care of an experienced <a href="~/procedures/breast-cancer-surgery/">oncoplastic breast cancer surgeon</a> — the plan moves forward without changing hands.</p>
""",
        "faqs": [
            ("Is a breast lump usually cancer?", "No. The large majority of breast lumps are benign — cysts, fibroadenomas or normal nodular tissue. But there is no reliable way to tell by touch alone, which is why every new lump should be assessed with examination and imaging, and biopsied if needed."),
            ("What is triple assessment?", "Triple assessment is the standard of care for breast symptoms: clinical examination, imaging (mammogram and/or ultrasound), and a needle biopsy where indicated. When all three agree, the diagnosis is highly reliable. A one-stop clinic delivers all three in a single visit."),
            ("How quickly can I be seen privately?", "Patients with new breast symptoms are prioritised. Appointments are booked directly with the hospital you choose, and can often be arranged within days."),
            ("Should I worry about breast pain?", "Breast pain on its own is very rarely a sign of cancer, and is one of the most common reasons women see a breast specialist. Pain that is persistent and in one specific spot is still worth assessing, and a clear diagnosis is often the most effective treatment of all."),
            ("Do I need a GP referral?", "Insured patients usually need a GP referral for their insurer to authorise the appointment. Self-funding patients can generally book directly with the hospital."),
        ],
        "related": ["breast-cancer-surgery", "gynaecomastia"],
    },
    {
        "slug": "breast-cancer-surgery",
        "nav": "Breast cancer surgery",
        "navdesc": "Oncoplastic conservation, mastectomy, lymph nodes",
        "tags": ["Lumpectomy", "Mastectomy", "Sentinel node", "Oncoplastic"],
        "title": "Breast Cancer Surgery London | Oncoplastic Surgeon Mr Ullah",
        "desc": "Private breast cancer surgery in London & Essex with oncoplastic surgeon Mr Zaker Ullah FRCS: breast-conserving surgery, therapeutic mammoplasty, mastectomy with immediate reconstruction and sentinel node biopsy.",
        "h1": "Breast cancer surgery, <em>planned twice</em>",
        "lede": "Surgery is usually the cornerstone of breast cancer treatment. Mr Ullah's oncoplastic training means every operation is planned twice over: once to remove the cancer completely, and once for the breast — and the person — that remains.",
        "glance": [("Anaesthetic", "General"), ("Hospital stay", "Day case to 1–2 nights, depending on operation"), ("Team", "Every case reviewed by a multidisciplinary team"), ("Timing", "Private surgery commonly within 1–2 weeks of the plan")],
        "sections": """
<h2>Breast-conserving surgery</h2>
<p>Where the tumour and breast size allow, the preferred operation is usually a <strong>wide local excision</strong> (lumpectomy) — removing the cancer with a margin of healthy tissue while keeping the breast. Oncoplastic techniques allow Mr Ullah to remove larger areas than conventional surgery would permit, then reshape the remaining tissue so the breast keeps a natural form.</p>
<p>In women with larger breasts this can take the form of a <strong>therapeutic mammoplasty</strong> — removing the cancer using breast reduction techniques, so the patient leaves with the cancer treated and a lighter, lifted breast. The <a href="~/procedures/breast-reduction/">other breast can be matched</a> at the same time or later.</p>
<h2>Mastectomy</h2>
<p>Some cancers — and some patients' preferences — are better served by <strong>mastectomy</strong>. Where appropriate, this can be a skin-sparing or nipple-sparing operation with <a href="~/procedures/breast-reconstruction/">immediate reconstruction</a>, so you wake from surgery with the breast shape already restored. Mr Ullah discusses reconstruction <em>before</em> mastectomy, never after.</p>
<h2>The lymph nodes</h2>
<p>Staging the armpit (axilla) is part of almost every breast cancer operation. For most patients this means a <strong>sentinel lymph node biopsy</strong> — removing only the first one to three nodes that drain the breast, identified with a tracer — rather than clearing the whole axilla. This gives your oncologists the information they need while greatly reducing the risk of arm swelling (lymphoedema).</p>
<h2>A team decision</h2>
<p>Every cancer case is reviewed by a multidisciplinary team — radiologists, pathologists, oncologists and specialist nurses — before and after surgery, in line with UK best practice. Chemotherapy, radiotherapy and hormone therapy are coordinated around the operation so that each part of treatment supports the others.</p>
""",
        "faqs": [
            ("How soon after diagnosis will I have surgery?", "Once the multidisciplinary team has confirmed the plan, private surgery can usually be scheduled promptly — commonly within one to two weeks, depending on the operation and any tests still needed. Some patients have chemotherapy before surgery; if so, that is a deliberate part of the plan, not a delay."),
            ("Will I lose my breast?", "Most breast cancers today are treated with breast-conserving surgery, and oncoplastic techniques have widened who is eligible. Where mastectomy is the safer choice, immediate reconstruction is usually possible. The decision is always made with you, with every option on the table."),
            ("What is oncoplastic breast surgery?", "Oncoplastic surgery combines complete removal of the cancer with plastic surgical techniques to preserve or restore the shape of the breast, in the same operation. Evidence shows cancer control is at least as good as standard surgery. <a href=\"~/news/what-is-oncoplastic-breast-surgery/\">Read Mr Ullah's guide</a>."),
            ("What are the risks of breast cancer surgery?", "As with any operation there are risks of bleeding, infection, seroma (fluid collection) and scarring, plus procedure-specific risks such as changes in sensation or, after axillary surgery, lymphoedema. Mr Ullah goes through the risks relevant to your operation in detail before you consent."),
            ("Can I have a second opinion before surgery?", "Yes — and it is your right. Many patients see Mr Ullah for a second opinion on a diagnosis or a proposed operation. Bring any imaging, biopsy results and clinic letters. <a href=\"~/second-opinion/\">More on second opinions</a>."),
        ],
        "related": ["breast-reconstruction", "benign-breast-conditions"],
    },
    {
        "slug": "breast-reconstruction",
        "nav": "Breast reconstruction",
        "navdesc": "Implant, flap, nipple and symmetry surgery",
        "tags": ["Immediate", "Delayed", "LD flap", "Implant"],
        "title": "Breast Reconstruction London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Breast reconstruction in London & Essex after mastectomy or lumpectomy: immediate and delayed, implant-based, latissimus dorsi and Grisotti flaps, fat grafting and nipple reconstruction with Mr Zaker Ullah FRCS.",
        "h1": "Breast <em>reconstruction</em>",
        "lede": "Reconstruction restores the shape of the breast after cancer surgery — at the same operation or years later. Mr Ullah offers the full range of implant-based and flap techniques, and is equally clear when no reconstruction is the right answer.",
        "glance": [("Timing", "Immediate (with mastectomy) or delayed — no time limit"), ("Techniques", "Implant, LD flap, Grisotti flap, fat grafting"), ("Hospital stay", "Typically 1–3 nights"), ("Insurance", "Usually covered as part of cancer treatment")],
        "sections": """
<h2>Immediate or delayed</h2>
<p><strong>Immediate reconstruction</strong> is performed during the same operation as the mastectomy, so the breast mound is restored before you wake. <strong>Delayed reconstruction</strong> can be done months or years later — there is no expiry date. The right choice depends on the cancer treatment planned (radiotherapy in particular), your health and your own preference. Some women choose no reconstruction at all; that is a valid choice, and Mr Ullah will say so.</p>
<h2>Implant-based reconstruction</h2>
<p>The most common technique in the UK uses a silicone implant, sometimes supported by a mesh or tissue matrix, to recreate the breast mound. It avoids surgery elsewhere on the body and has a shorter recovery, at the cost of a less natural feel and the likelihood of maintenance surgery over a lifetime.</p>
<h2>Flap reconstruction</h2>
<p>Reconstruction with your own tissue gives a warm, natural breast that ages with you. Mr Ullah performs <strong>latissimus dorsi (LD) flap</strong> reconstruction, which brings muscle and skin from the back around to the chest, often combined with an implant. For suitable central tumours he also uses the <strong>Grisotti flap</strong>, an elegant technique that reconstructs the nipple area using the breast's own tissue at the time of cancer surgery.</p>
<h2>Finishing touches</h2>
<p>Reconstruction is often completed in stages: <a href="~/procedures/fat-grafting/">fat grafting</a> to refine contour, nipple reconstruction with a small local flap, and symmetrisation surgery to the other breast — a <a href="~/procedures/breast-reduction/">reduction</a>, uplift or <a href="~/procedures/breast-augmentation/">augmentation</a> — so that the pair sit naturally together.</p>
""",
        "faqs": [
            ("Will a reconstructed breast look and feel natural?", "Reconstruction restores shape and symmetry in clothing very reliably, and modern techniques can look natural out of clothing too. Sensation is usually reduced. Tissue-based reconstructions generally feel more natural than implants; Mr Ullah will show you representative outcomes for each option."),
            ("Is reconstruction safe if I need radiotherapy?", "Radiotherapy increases complication rates for some reconstruction types, particularly implants. If radiotherapy is likely, that shapes the recommended technique or timing — one reason reconstruction is planned alongside cancer treatment rather than separately."),
            ("Can I have reconstruction years after my mastectomy?", "Yes. Delayed reconstruction is routine and there is no time limit. Patients treated a decade or more ago still have options, subject to fitness and previous treatment."),
            ("Is breast reconstruction covered by insurance?", "Reconstruction after breast cancer is normally covered as part of cancer treatment by UK private medical insurers, including symmetrising surgery to the other breast. Always confirm with your insurer in advance."),
        ],
        "related": ["breast-cancer-surgery", "fat-grafting"],
    },
    {
        "slug": "breast-reduction",
        "nav": "Breast reduction",
        "navdesc": "Reduction mammoplasty &amp; symmetrisation",
        "tags": ["Reduction", "Uplift", "Symmetry"],
        "title": "Breast Reduction London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Breast reduction surgery (reduction mammoplasty) in London & Essex with consultant oncoplastic surgeon Mr Zaker Ullah FRCS — for comfort, proportion, or symmetry after breast cancer surgery. Recovery, scars and FAQs.",
        "h1": "Breast reduction <em>&amp; symmetrisation</em>",
        "lede": "Reduction mammoplasty reshapes heavy breasts to a lighter, higher, more comfortable form — for relief of symptoms, for proportion, or to balance the breasts after cancer surgery.",
        "glance": [("Anaesthetic", "General"), ("Operation", "Around 2–3 hours"), ("Hospital stay", "Day case or one night"), ("Recovery", "Desk work 1–2 weeks · exercise ~6 weeks")],
        "sections": """
<h2>Who benefits</h2>
<p>Heavy breasts are a physical burden: neck, shoulder and back pain, bra-strap grooving, skin irritation beneath the breast fold and real limits on exercise. A reduction removes excess tissue and skin, lifts the breast and repositions the nipple — exchanging weight and discomfort for scars that fade substantially over the first one to two years.</p>
<h2>Symmetrisation after cancer surgery</h2>
<p>As an oncoplastic surgeon, a large part of Mr Ullah's reduction practice is <strong>symmetrisation</strong> — reducing, lifting or reshaping the opposite breast so it matches a breast treated for cancer or reconstructed. This is a routine part of the reconstructive pathway and is usually covered by insurers as part of cancer treatment.</p>
<h2>The operation and recovery</h2>
<p>Breast reduction is performed under general anaesthetic and typically takes two to three hours, as a day case or with a single night in hospital. Most patients are back at desk work within one to two weeks and exercising fully at around six weeks. Mr Ullah discusses scar patterns, nipple sensation and the implications for breastfeeding candidly before any decision is made.</p>
""",
        "faqs": [
            ("Will breast reduction affect nipple sensation or breastfeeding?", "Both can be affected. Some change in nipple sensation is common early on and usually improves, though it can be permanent. Many women can still breastfeed after a reduction, but it cannot be guaranteed — if future breastfeeding matters to you, say so, as it influences technique and timing."),
            ("What scars does a breast reduction leave?", "The usual pattern is a scar around the areola, a vertical line down to the breast fold, and often a line within the fold itself (the ‘anchor’ pattern). Scars are typically red and firm at first and fade substantially over 12–24 months."),
            ("Is breast reduction covered by insurance?", "Cosmetic reduction generally is not, but symmetrisation after breast cancer surgery is usually treated as part of the reconstruction pathway. Your insurer confirms cover in advance either way."),
            ("How long is recovery after breast reduction?", "Most women return to desk work within one to two weeks, drive at around two weeks once comfortable, and return to full exercise at about six weeks. A supportive bra is worn day and night for several weeks."),
        ],
        "related": ["breast-reconstruction", "breast-augmentation"],
    },
    {
        "slug": "breast-augmentation",
        "nav": "Breast augmentation",
        "navdesc": "Implants for size, shape or symmetry",
        "tags": ["Implants", "Symmetry"],
        "title": "Breast Augmentation London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Breast augmentation with implants in London & Essex with consultant breast surgeon Mr Zaker Ullah FRCS: honest consultation, implant choices, recovery, safety and augmentation for symmetry after cancer surgery.",
        "h1": "Breast <em>augmentation</em>",
        "lede": "Augmentation uses an implant to increase the size or restore the fullness of the breast. Mr Ullah brings an oncoplastic surgeon's perspective: the same operation he uses to rebuild symmetry after cancer, applied with the same care to cosmetic goals.",
        "glance": [("Anaesthetic", "General"), ("Operation", "Around 1 hour"), ("Hospital stay", "Usually day case"), ("Recovery", "Desk work ~1 week · exercise 4–6 weeks")],
        "sections": """
<h2>An honest consultation</h2>
<p>A good augmentation begins with an honest conversation about proportion — what an implant can and cannot do for your frame, how size, profile and placement (over or under the muscle) change the result, and how breast and implant will change over years, not months. Mr Ullah has no interest in overselling: you receive the same measured advice he gives every patient.</p>
<h2>Augmentation in the cancer setting</h2>
<p>Augmentation is also a reconstructive tool. After breast-conserving surgery or reconstruction, an implant on one or both sides can restore volume and symmetry. Patients with a personal or family history of breast cancer receive specific advice on imaging and follow-up with implants in place.</p>
<h2>The operation and aftercare</h2>
<p>The procedure takes around an hour under general anaesthetic, usually as a day case. Expect to be back at desk work within about a week and exercising fully at four to six weeks. Implants are not lifetime devices: most patients should expect further surgery at some point, and Mr Ullah explains the realistic long-term picture — including rare implant-associated conditions — before you decide.</p>
""",
        "faqs": [
            ("How long do breast implants last?", "Implants do not need replacing on a fixed schedule, but neither do they last forever — many patients have revision surgery within 10–15 years for wear, capsular contracture or a change of preference. Plan for maintenance over a lifetime, not a one-off operation."),
            ("Are breast implants safe?", "Modern implants are well studied and serious complications are rare, but not zero — including capsular contracture, rupture and BIA-ALCL, a rare lymphoma associated with certain textured implants. Mr Ullah covers the current evidence so your decision is genuinely informed."),
            ("Can I still have mammograms with implants?", "Yes. Screening remains effective, though implants can obscure some breast tissue and radiographers use additional views. Always tell the screening service you have implants when booking."),
        ],
        "related": ["breast-reduction", "fat-grafting"],
    },
    {
        "slug": "fat-grafting",
        "nav": "Fat grafting (lipofilling)",
        "navdesc": "Refining shape with your own tissue",
        "tags": ["Lipofilling", "Contour"],
        "title": "Breast Fat Grafting & Lipofilling London | Mr Zaker Ullah",
        "desc": "Fat grafting (lipofilling) to the breast in London & Essex: correcting dents after lumpectomy, refining reconstruction and softening radiotherapy changes, with consultant oncoplastic surgeon Mr Zaker Ullah FRCS.",
        "h1": "Fat grafting <em>to the breast</em>",
        "lede": "Fat grafting — lipofilling — moves a small amount of your own fat, harvested by gentle liposuction, into the breast to smooth contours, fill defects and soften scarred tissue.",
        "glance": [("Anaesthetic", "Usually general"), ("Hospital stay", "Day case"), ("Sessions", "1–3, about 3 months apart"), ("Final result", "Judged at around 3 months")],
        "sections": """
<h2>What it is used for</h2>
<p>In breast surgery, fat grafting is chiefly a refining tool: filling a dent left by breast-conserving cancer surgery, smoothing the edges of an implant reconstruction, softening tissue damaged by radiotherapy and correcting small asymmetries. It uses no foreign material and leaves only tiny marks at the donor and recipient sites.</p>
<h2>How it works</h2>
<p>Fat is harvested by gentle liposuction — usually from the abdomen or thighs — purified, and injected into the breast in fine threads so that each droplet gains a blood supply. A proportion of grafted fat (commonly 30–50%) is naturally resorbed in the first months, which is why larger corrections are often staged over two or three sessions a few months apart.</p>
<h2>Recovery</h2>
<p>Fat grafting is usually a day-case procedure. Bruising at the donor site is the main after-effect; most patients are back to normal activities within days. The final result is judged at around three months, once swelling has settled.</p>
""",
        "faqs": [
            ("Is fat grafting safe after breast cancer?", "Current evidence has not shown lipofilling to increase the risk of cancer recurrence, and it is widely used in reconstructive practice. Grafted fat can cause benign changes on mammograms (oil cysts, calcification) which specialists recognise; your imaging team should always know you have had lipofilling."),
            ("How many sessions will I need?", "Small refinements are often achieved in one session. Larger corrections typically need two or three sessions, spaced roughly three months apart, because a proportion of each graft is resorbed."),
            ("Does the transferred fat behave like normal fat?", "Yes — once it has taken, grafted fat is living tissue. It feels natural and will gain and lose volume with your weight like fat anywhere else."),
        ],
        "related": ["breast-reconstruction", "breast-cancer-surgery"],
    },
    {
        "slug": "gynaecomastia",
        "nav": "Gynaecomastia (men)",
        "navdesc": "Male breast assessment &amp; reduction",
        "tags": ["Men", "Liposuction", "Gland excision"],
        "title": "Gynaecomastia Surgery London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Gynaecomastia (male breast reduction) in London & Essex with a consultant breast surgeon: specialist assessment, liposuction and gland excision, recovery and results with Mr Zaker Ullah FRCS.",
        "h1": "Gynaecomastia — <em>male breast reduction</em>",
        "lede": "Enlargement of male breast tissue is common, benign in the vast majority of cases, and very treatable. It still deserves a specialist assessment — both to rule out the rare serious cause and to get a result worth having.",
        "glance": [("Anaesthetic", "General"), ("Hospital stay", "Day case"), ("Garment", "Compression vest for a few weeks"), ("Recovery", "Desk work ~1 week · exercise 4–6 weeks")],
        "sections": """
<h2>First, a diagnosis</h2>
<p>Gynaecomastia has many triggers: hormonal changes in adolescence and later life, weight, certain medications and occasionally underlying medical conditions. Male breast cancer is rare but real, which is why assessment by a <strong>breast specialist</strong> — with imaging and biopsy where indicated — comes before any discussion of surgery. Some gynaecomastia, particularly in teenagers, resolves on its own; some responds to treating the underlying cause.</p>
<h2>Surgery</h2>
<p>Where the tissue is established and troubling, surgery removes it. Depending on the balance of glandular tissue and fat, Mr Ullah uses liposuction, direct excision of the gland through a small incision at the edge of the areola, or both. Significant skin excess occasionally needs additional techniques, which he will discuss openly if they apply to you.</p>
<h2>Recovery and results</h2>
<p>The operation is usually a day case under general anaesthetic. A compression garment is worn for a few weeks; most men return to desk work within a week and full exercise at four to six weeks. Once mature, the result is usually permanent, provided weight and any causative medication are managed.</p>
""",
        "faqs": [
            ("Is gynaecomastia dangerous?", "Almost always no — it is benign glandular enlargement. But one-sided, firm or rapidly changing male breast tissue, or nipple discharge, should be assessed promptly to exclude male breast cancer, which although rare does occur."),
            ("Will exercise get rid of gynaecomastia?", "Exercise and weight loss reduce the fatty component, but true glandular tissue does not respond to exercise. That is why chest exercises often make no visible difference — and why gland excision is part of the operation where gland predominates."),
            ("What scars are left after gynaecomastia surgery?", "Liposuction leaves a few millimetre-scale marks. Gland excision usually adds a fine scar along the lower edge of the areola, where it tends to fade well."),
            ("Is gynaecomastia surgery covered by insurance?", "Usually not when it is cosmetic, though insurers may cover assessment of a new lump or suspicious change. Self-pay prices are confirmed in writing by the hospital before you commit."),
        ],
        "related": ["benign-breast-conditions", "general-laparoscopic-surgery"],
    },
    {
        "slug": "general-laparoscopic-surgery",
        "nav": "Hernia &amp; gallbladder",
        "navdesc": "Keyhole general surgery",
        "tags": ["Gallbladder", "Hernia", "Appendix"],
        "title": "Keyhole Hernia & Gallbladder Surgery London | Mr Ullah FRCS",
        "desc": "Keyhole (laparoscopic) general surgery in London & Essex: gallbladder removal, inguinal, umbilical and incisional hernia repair and appendicectomy with consultant general surgeon Mr Zaker Ullah FRCS.",
        "h1": "General &amp; <em>laparoscopic</em> surgery",
        "lede": "Alongside his breast practice, Mr Ullah maintains a general surgical practice in laparoscopic — keyhole — surgery: gallbladder removal, hernia repair and appendicectomy.",
        "glance": [("Approach", "Keyhole wherever suitable"), ("Hospital stay", "Usually day case or one night"), ("Recovery", "Most back to normal within 2 weeks"), ("Published", "Research on laparoscopic hernia repair")],
        "sections": """
<h2>Gallstones &amp; gallbladder removal</h2>
<p>Gallstones that cause pain, inflammation or pancreatitis are best treated by removing the gallbladder — <strong>laparoscopic cholecystectomy</strong>. Performed through four small incisions, it is one of the most common operations in the UK; most patients go home the same day or after one night and are back to normal activity within a fortnight. You can live entirely normally without a gallbladder.</p>
<h2>Hernia repair</h2>
<p>A hernia — in the groin (inguinal), at the navel (umbilical) or through a previous scar (incisional) — will not repair itself. Mr Ullah repairs hernias laparoscopically and by open surgery, usually reinforced with mesh, choosing the approach that suits the hernia and the patient. He has published research on laparoscopic hernia repair techniques.</p>
<h2>Appendicectomy</h2>
<p>Suspected appendicitis needs urgent assessment. Where surgery is required, laparoscopic appendicectomy allows both confirmation of the diagnosis and treatment through keyhole incisions, with a faster recovery than open surgery.</p>
""",
        "faqs": [
            ("What are the advantages of keyhole surgery?", "Smaller incisions mean less pain after surgery, shorter hospital stays, faster return to work and smaller scars. Not every patient or condition is suitable, and a small proportion of keyhole operations need conversion to open surgery for safety — that possibility is always part of consent."),
            ("How long does hernia repair recovery take?", "Most patients return to desk work within one to two weeks after laparoscopic repair, and to heavy lifting at around four to six weeks. Open repair recovery is somewhat longer. You can drive once you can perform an emergency stop comfortably."),
            ("Do gallstones always need surgery?", "No. Stones found incidentally that cause no symptoms can usually be left alone. Surgery is advised once stones cause pain or complications, because further attacks are then likely."),
        ],
        "related": ["gynaecomastia", "benign-breast-conditions"],
    },
]

# ------------------------------------------------------------- reviews
# Verbatim excerpts from iWantGreatCare (checked 2026-11-03). Do not edit wording.
IWGC_RATING = "5.0"
IWGC_COUNT = 22
REVIEWS = [
    ("Mr Z Ullah is supremely the best surgeon. In him I trust completely and feel so lucky to have had him as my surgeon. His attention, professionalism and care is exemplary.", "27 Nov 2025", "The Holly"),
    ("Thanks to Mr Ullah's care and skills - I am still here 3 years later… His kindness and compassion is everything a doctor should have.", "30 Apr 2024", "The Holly"),
    ("He explains things thoroughly to you and takes the time to listen to patients, asking many questions and showing genuine concern. He never rushes his consultations and is a highly empathetic Doctor.", "18 Jul 2024", "Whipps Cross"),
    ("I have had two surgeries with dr ullah and both experiences have been stress free and easy recoveries with minimal scarring. I can honestly say I am in the best hands.", "4 Jul 2024", "The Holly"),
    ("Had the greatest pleasure to meet Mr Ullah today and his amazing nurse Beverly. From the moment I sat down, i felt completely comfortable and in safe hands.", "4 Dec 2025", "The Holly"),
    ("Mr. Ullah was patient and attentive to my needs. I am very happy with the reconstruction of my breast… A safe pair of hands.", "16 Mar 2023", "The Holly"),
    ("Dr Ullah saved me and my sanity with an incredibly well organised and executed breast surgery. I'm so grateful to have met him and his experienced, friendly team.", "2 Mar 2023", "The Holly"),
    ("He listens intently to all questions and concerns and makes you feel heard… All this being said his skill as a surgeon is outstanding.", "24 Feb 2022", "Whipps Cross"),
    ("Mr Ullah has been my surgeon since I was diagnosed with Breast cancer in 2016. He is kind and compassionate…", "10 Jul 2024", "Whipps Cross"),
]

# ------------------------------------------------------------- podcast
PODCAST = {
    "show": "Everything Changed with Rosie Fawehimi",
    "host": "Rosie Fawehimi",
    "title": "5 Breast Cancer Questions Answered by a Surgeon",
    "season": 3, "episode": 2,
    "date": "2026-10-14", "date_label": "14 October 2026",
    "duration": "PT34M04S", "duration_label": "34 min",
    "youtube": "rYpUCW_EbTY",
    "spotify_episode": "5bFR1v4vIfJxn29kMQ4yn1",
    "spotify": "https://open.spotify.com/episode/5bFR1v4vIfJxn29kMQ4yn1",
    "apple": "https://podcasts.apple.com/us/podcast/5-breast-cancer-questions-answered-by-a-surgeon/id1843133154?i=1000796268423",
    "summary": "Recorded in front of a live audience, breast cancer survivor Rosie Fawehimi sits down with the surgeon who diagnosed her and later performed her double mastectomy and reconstruction — Mr Ullah — to answer the five questions she hears most.",
    "chapters": [
        "Lumpectomy or mastectomy — how is the decision made?",
        "Symptoms, self-checking and what to look for",
        "Is breast cancer rising in young women?",
        "Does everyone need radiotherapy?",
        "Triple-negative breast cancer, explained",
    ],
}
