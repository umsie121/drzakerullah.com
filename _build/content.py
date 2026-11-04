"""Structured content: procedures, locations and practice facts.

House style: British English, plain and assured, no em or en dashes
(use commas, colons, full stops, or "to" for ranges). Facts here must be
verifiable; anything marked TODO needs confirming with the practice.
"""

IWGC = "https://www.iwantgreatcare.org/doctors/mr-md-zaker-ullah"

INSURERS = ["Bupa", "Bupa Global", "AXA Health", "Aviva", "Vitality", "WPA", "Cigna", "Healix", "Health-on-Line"]

# Private secretary: Ms Juliet Willes. Name and number confirmed by the old Squarespace site;
# email from Bupa Finder (old site gave an nhs.net address). TODO confirm which email to use.
SEC_NAME = "Ms Juliet Willes"
FACEBOOK = "https://www.facebook.com/drzakerullah/"
LINKEDIN = "https://uk.linkedin.com/in/md-zaker-ullah-40a9b474"
# Areas of interest as listed on his Bupa Finder profile (used for schema knowsAbout / LLMs).
KNOWS_ABOUT = ["Breast pain", "Breast lump", "Nipple discharge", "Breast cancer", "DCIS", "Mastectomy", "Breast reduction",
               "Therapeutic mammoplasty", "Breast conserving surgery", "BRCA risk reducing surgery", "Sentinel lymph node biopsy",
               "Targeted axillary dissection", "Axillary clearance", "Implant breast reconstruction", "Chest wall perforator flaps (LICAP, MICAP)",
               "Latissimus dorsi flap reconstruction", "Benign breast disease", "Lipofilling", "Breast symmetrisation", "Nipple reconstruction",
               "Gynaecomastia", "Male breast cancer", "Skin lesion excision", "Sebaceous cyst excision", "Lipoma excision", "Mole removal",
               "Hernia repair", "Abscess incision and drainage", "One-stop breast clinic", "Family history breast cancer risk assessment"]
SEC_PHONE = "020 8936 1263"
SEC_TEL = "+442089361263"
SEC_EMAIL = "juliet.willes@nuffieldhealth.com"

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
        "phone": None,  # no line specific to Mr Ullah verified; book via secretary
        "tel": None,
        "operator": "HCA Healthcare UK",
        "h1": "Breast surgeon on Harley Street",
        "title": "Breast Surgeon Harley Street, London W1 | Mr Zaker Ullah",
        "desc": "Consultant oncoplastic breast surgeon at The Harley Street Clinic, London W1. Breast lump assessment, breast cancer surgery, reconstruction and reduction.",
        "travel": "A short walk from Regent's Park, Great Portland Street and Oxford Circus stations, in London's historic medical district.",
        "serves": ["Marylebone", "Fitzrovia", "Mayfair", "Westminster", "Camden", "St John's Wood", "Kensington", "Paddington", "Central London"],
        "intro": "The Harley Street Clinic is one of London's best known private hospitals, with cancer, imaging and surgical facilities under one roof. Mr Ullah consults and operates here for patients who live or work in central and west London, and for those travelling to London for a specialist opinion.",
        "why": [
            "Consultation, mammography, ultrasound and biopsy on site",
            "Inpatient and day case theatres for cancer, reconstructive and reduction surgery",
            "Access to HCA's oncology and multidisciplinary teams",
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
        "phone": "020 3386 9000",  # Nuffield St Bartholomew's main line, TODO confirm
        "tel": "+442033869000",
        "operator": "Nuffield Health",
        "h1": "Breast surgeon in the City of London",
        "title": "Breast Surgeon City of London EC1 | Mr Zaker Ullah FRCS",
        "desc": "Private breast surgeon in the City of London at Nuffield Health St Bartholomew's. Breast lump clinics, breast cancer surgery and second opinions.",
        "travel": "Inside the St Bartholomew's Hospital site, a few minutes on foot from Farringdon, Barbican and St Paul's, and easily reached from Canary Wharf on the Elizabeth line.",
        "serves": ["The City", "Clerkenwell", "Islington", "Shoreditch", "Canary Wharf", "Southwark", "Hackney", "Tower Hamlets", "Holborn"],
        "intro": "Nuffield Health's private hospital at St Bartholomew's sits within Britain's oldest hospital site, alongside one of Europe's leading cancer centres. It suits patients who work in the City or in east London and need an appointment that fits around the working day.",
        "why": [
            "Private hospital within the St Bartholomew's campus",
            "Appointments that fit around a City or Canary Wharf working day",
            "Consultation, imaging and day case surgery",
            "Corporate, insured and self-funding patients welcome",
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
        "h1": "Breast surgeon in Buckhurst Hill, for Woodford Green, Loughton and Chigwell",
        "title": "Breast Surgeon Buckhurst Hill & Woodford Green | Mr Ullah",
        "desc": "Private breast surgeon at Nuffield Health The Holly, Buckhurst Hill IG9, minutes from Woodford Green, Loughton and Chigwell. Same day one-stop breast clinic.",
        "travel": "On the High Road in Buckhurst Hill at the edge of Epping Forest, with parking on site. Buckhurst Hill Central line station is close by, and the M11 and M25 are a few minutes away.",
        "serves": ["Buckhurst Hill", "Woodford Green", "Woodford Wells", "South Woodford", "Loughton", "Chigwell", "Epping", "Theydon Bois", "Waltham Abbey", "Harlow", "Brentwood", "Chingford", "Walthamstow", "Romford", "Ilford", "Wanstead"],
        "intro": "Nuffield Health The Holly Hospital is Mr Ullah's principal private base, and the home of his private secretary. A calm and well equipped hospital on the border of London and Essex, it is a few minutes from Woodford Green, Loughton and Chigwell, and serves patients from across Essex, Hertfordshire and north east London. Mr Ullah runs its Rapid Access Breast Clinic on Tuesday afternoons, with consultation and imaging on the same day.",
        "local": "For most patients in Woodford Green, South Woodford, Loughton and Chigwell, The Holly is the nearest private hospital with a consultant-led breast clinic. It sits on the High Road between Woodford Green and Loughton, with parking on site and Buckhurst Hill Central line station a short walk away. Many of Mr Ullah's NHS patients at nearby Whipps Cross choose to see him here privately.",
        "clinics": "Tuesday afternoon (Rapid Access Breast Clinic) and Thursday morning",
        "why": [
            "Rapid Access Breast Clinic with Mr Ullah on Tuesday afternoons",
            "Parking on site, close to the M11 and M25",
            "Outpatient clinics, imaging and full operating theatres",
            "Consultations in English and Bengali",
        ],
    },
]

# Lead with The Holly (Buckhurst Hill / Woodford Green), then central London.
LOCATIONS = [LOCATIONS[2], LOCATIONS[0], LOCATIONS[1]]

NHS_BASE = {"name": "Whipps Cross University Hospital", "trust": "Barts Health NHS Trust",
            "street": "Whipps Cross Road", "locality": "Leytonstone, London", "postcode": "E11 1NR"}

# ------------------------------------------------------------- procedures
PROCEDURES = [
    {
        "slug": "benign-breast-conditions",
        "nav": "Breast lumps and pain",
        "short_desc": "One-stop assessment",
        "summary": "Examination, imaging and biopsy for a new breast symptom, usually at a single visit.",
        "title": "Private Breast Lump Clinic London & Essex | Mr Zaker Ullah",
        "desc": "Private one-stop breast clinic in London and Essex. Examination, ultrasound or mammogram and biopsy at a single visit with consultant breast surgeon Mr Zaker Ullah.",
        "h1": "Breast lumps, pain and benign breast conditions",
        "lede": "Most breast symptoms are benign. Every one of them still deserves a clear answer, and quickly. Mr Ullah introduced the one-stop breast clinic at Whipps Cross and runs his private clinics in the same way.",
        "glance": [("Appointment", "Usually 45 to 90 minutes"), ("Tests", "Examination, ultrasound or mammogram, and biopsy if needed"), ("Results", "Imaging on the day, biopsy within a few days"), ("Referral", "A GP letter is needed by most insurers")],
        "sections": """
<h2>Symptoms Mr Ullah assesses</h2>
<ul>
<li>A new lump or area of thickening in the breast or armpit</li>
<li>Breast pain (mastalgia), whether cyclical, constant or in one place</li>
<li>Nipple discharge, a newly inverted nipple or a rash on the nipple</li>
<li>Dimpling, puckering or redness of the skin</li>
<li>Breast cysts and fibroadenomas</li>
<li>A change in the size or shape of one breast</li>
<li>A family history of breast cancer, and questions about personal risk</li>
</ul>
<h2>The one-stop approach</h2>
<p>The traditional route to a diagnosis is a clinic appointment, then a separate scan, then a further appointment for results. It can stretch an anxious wait across several weeks. At a one-stop clinic Mr Ullah takes a full history and examines you, arranges ultrasound or mammography at the same visit according to your age and symptoms, and takes a needle biopsy there and then if anything needs sampling.</p>
<p>This is <strong>triple assessment</strong>, the standard of care for breast symptoms in the United Kingdom. Most patients leave the first appointment either reassured or with a clear plan.</p>
<h2>If treatment is needed</h2>
<p>Many benign conditions need no treatment once the diagnosis is certain. Where treatment helps, Mr Ullah offers drainage of cysts, removal of symptomatic fibroadenomas and other benign lumps, duct surgery for troublesome nipple discharge, and structured advice for breast pain.</p>
<h2>Family history and breast cancer risk</h2>
<p>If close relatives have had breast or ovarian cancer, Mr Ullah offers a personal risk assessment, with advice on screening, genetic testing and, for some women, risk reducing options. Most people with a family history are at only moderately raised risk, and a clear assessment is reassuring in itself.</p>
<p>If a biopsy shows cancer, you are already in the care of an experienced <a href="~/procedures/breast-cancer-surgery/">oncoplastic breast surgeon</a>, and your treatment continues with the same surgeon.</p>
""",
        "faqs": [
            ("Is a breast lump usually cancer?", "No. The large majority of breast lumps are benign: cysts, fibroadenomas or normal nodular tissue. There is no reliable way to tell them apart by touch, which is why every new lump should be examined, imaged and, if needed, biopsied."),
            ("What is triple assessment?", "Triple assessment is clinical examination, imaging (mammogram, ultrasound or both) and a needle biopsy where indicated. When all three agree, the diagnosis is highly reliable. A one-stop clinic provides all three at one visit."),
            ("How quickly can I be seen privately?", "New breast symptoms are given priority, and an appointment can often be arranged within days. Call the private secretary or send an enquiry."),
            ("Should I worry about breast pain?", "Breast pain on its own is very rarely a sign of cancer and is one of the most common reasons women see a breast specialist. Pain that persists in one particular spot should still be assessed. A clear diagnosis is often the most effective treatment."),
            ("Do I need a GP referral?", "Insured patients usually need a GP referral before their insurer will authorise the appointment. Self-funding patients can book directly."),
        ],
        "related": ["breast-cancer-surgery", "gynaecomastia"],
    },
    {
        "slug": "breast-cancer-surgery",
        "nav": "Breast cancer surgery",
        "short_desc": "Oncoplastic and conserving",
        "summary": "Breast conserving surgery, therapeutic mammoplasty, mastectomy and lymph node surgery.",
        "title": "Breast Cancer Surgery London | Oncoplastic Surgeon Mr Ullah",
        "desc": "Private breast cancer surgery in London and Essex: breast conserving surgery, therapeutic mammoplasty, mastectomy with reconstruction and sentinel node biopsy.",
        "h1": "Breast cancer surgery",
        "lede": "Surgery is usually the foundation of breast cancer treatment. As an oncoplastic surgeon, Mr Ullah plans the removal of the cancer and the appearance of the breast together, before the operation, so neither is an afterthought.",
        "glance": [("Anaesthetic", "General"), ("Hospital stay", "Day case to two nights, depending on the operation"), ("Team", "Every case reviewed by a multidisciplinary team"), ("Timing", "Often within one to two weeks of the plan")],
        "sections": """
<h2>Breast conserving surgery</h2>
<p>Where the size and position of the tumour allow, the preferred operation is usually a <strong>wide local excision</strong>, or lumpectomy. The cancer is removed with a margin of healthy tissue and the breast is kept. Oncoplastic techniques allow Mr Ullah to remove a larger area than conventional surgery would permit, then reshape the remaining tissue so the breast keeps a natural form.</p>
<p>In women with larger breasts this can be a <strong>therapeutic mammoplasty</strong>, in which the cancer is removed using the techniques of a breast reduction. The result is a lighter, lifted breast, and the <a href="~/procedures/breast-reduction/">other breast can be matched</a> at the same operation or later.</p>
<h2>Mastectomy</h2>
<p>Some cancers, and some patients' own preferences, are better served by <strong>mastectomy</strong>. Where appropriate it can be skin sparing or nipple sparing, with <a href="~/procedures/breast-reconstruction/">immediate reconstruction</a>, so that the shape of the breast is restored before you wake. Mr Ullah discusses reconstruction before mastectomy, not after it.</p>
<h2>The lymph nodes</h2>
<p>Assessing the armpit (axilla) is part of almost every breast cancer operation. For most patients this means a <strong>sentinel lymph node biopsy</strong>: only the first one to three nodes draining the breast are removed, located with a tracer. It gives the oncologists the information they need and greatly reduces the risk of arm swelling (lymphoedema). After chemotherapy, a <strong>targeted axillary dissection</strong> can remove the specific nodes that were affected, and where needed an <strong>axillary clearance</strong> is performed.</p>
<h2>DCIS and risk reducing surgery</h2>
<p><strong>DCIS</strong> (ductal carcinoma in situ) is an early, non-invasive change that is usually treated with breast conserving surgery. For women who carry a BRCA or other high-risk gene variant, Mr Ullah offers <strong>risk reducing mastectomy</strong> with reconstruction, after careful counselling.</p>
<h2>A team decision</h2>
<p>Every cancer case is discussed by a multidisciplinary team of radiologists, pathologists, oncologists and specialist nurses, before and after surgery. Chemotherapy, radiotherapy and hormone treatment are planned around the operation so that each part of treatment supports the others.</p>
""",
        "faqs": [
            ("How soon after diagnosis will I have surgery?", "Once the multidisciplinary team has agreed the plan, private surgery can usually be arranged within one to two weeks, depending on the operation and any tests still needed. Some patients have chemotherapy first. When that happens it is a deliberate part of the plan, not a delay."),
            ("Will I lose my breast?", "Most breast cancers are now treated with breast conserving surgery, and oncoplastic techniques have widened who is suitable. Where mastectomy is the safer choice, immediate reconstruction is usually possible. The decision is always made with you."),
            ("What is oncoplastic breast surgery?", "Oncoplastic surgery combines complete removal of the cancer with plastic surgical techniques that preserve or restore the shape of the breast, at the same operation. Cancer control is at least as good as with standard surgery. <a href=\"~/news/what-is-oncoplastic-breast-surgery/\">Read Mr Ullah's article</a>."),
            ("What are the risks of breast cancer surgery?", "As with any operation, there are risks of bleeding, infection, fluid collection (seroma) and scarring, along with risks particular to each procedure, such as altered sensation or, after surgery to the armpit, lymphoedema. Mr Ullah explains the risks of your operation in detail before you consent."),
            ("Can I have a second opinion before surgery?", "Yes, and it is your right to ask. Many patients see Mr Ullah for a second opinion on a diagnosis or a proposed operation. <a href=\"~/second-opinion/\">More about second opinions</a>."),
        ],
        "related": ["breast-reconstruction", "benign-breast-conditions"],
    },
    {
        "slug": "breast-reconstruction",
        "nav": "Breast reconstruction",
        "short_desc": "Implant and flap",
        "summary": "Immediate and delayed reconstruction with implants, your own tissue, chest wall perforator flaps and fat grafting.",
        "title": "Breast Reconstruction London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Breast reconstruction after mastectomy or lumpectomy in London and Essex: immediate and delayed, implant, LD flap and Grisotti flap, fat grafting and nipple reconstruction.",
        "h1": "Breast reconstruction",
        "lede": "Reconstruction restores the shape of the breast after cancer surgery, either at the same operation or years later. Mr Ullah offers the full range of implant and tissue techniques, and is equally clear when no reconstruction is the right choice.",
        "glance": [("Timing", "Immediate, with the mastectomy, or delayed with no time limit"), ("Techniques", "Implant, LD flap, LICAP and MICAP flaps, Grisotti flap, fat grafting"), ("Hospital stay", "Typically one to three nights"), ("Insurance", "Usually covered as part of cancer treatment")],
        "sections": """
<h2>Immediate or delayed</h2>
<p><strong>Immediate reconstruction</strong> takes place during the same operation as the mastectomy, so the shape of the breast is restored before you wake. <strong>Delayed reconstruction</strong> can be carried out months or years later; there is no time limit. The right choice depends on the cancer treatment planned, radiotherapy in particular, on your health and on your own preference. Some women choose not to have a reconstruction. That is a valid decision, and Mr Ullah will say so.</p>
<h2>Implant reconstruction</h2>
<p>The most common technique in the United Kingdom uses a silicone implant, sometimes supported by a mesh or tissue matrix, to recreate the breast. It avoids surgery elsewhere on the body and has a shorter recovery. In return, the breast feels less natural and is likely to need further surgery over a lifetime.</p>
<h2>Reconstruction with your own tissue</h2>
<p>A reconstruction made from your own tissue is warm and natural, and changes with you over time. Mr Ullah performs <strong>latissimus dorsi (LD) flap</strong> reconstruction, which brings muscle and skin from the back to the chest and is often combined with an implant. For suitable cancers near the nipple he also uses the <strong>Grisotti flap</strong>, which rebuilds the area from the breast's own tissue during the cancer operation.</p>
<h2>Chest wall perforator flaps</h2>
<p>After breast conserving surgery, a dent or loss of shape can be corrected with a <strong>chest wall perforator flap</strong> (LICAP or MICAP). Tissue from just beside the breast, on its own small blood supply, is moved into the defect, restoring natural shape without an implant and without surgery elsewhere on the body. It is an area of particular expertise for Mr Ullah.</p>
<h2>Completing the result</h2>
<p>Reconstruction is often completed in stages: <a href="~/procedures/fat-grafting/">fat grafting</a> to refine the contour, nipple reconstruction with a small local flap, and symmetrising surgery to the other breast, usually a <a href="~/procedures/breast-reduction/">reduction</a> or an uplift, so that the two sit naturally together.</p>
""",
        "faqs": [
            ("Will a reconstructed breast look and feel natural?", "Reconstruction restores shape and symmetry in clothes very reliably, and modern techniques can look natural without clothes too. Sensation is usually reduced. Reconstructions made from your own tissue generally feel more natural than implants."),
            ("Is reconstruction safe if I need radiotherapy?", "Radiotherapy increases the rate of complications for some types of reconstruction, implants in particular. If radiotherapy is likely, it shapes the recommended technique or timing, which is why reconstruction is planned alongside cancer treatment."),
            ("Can I have reconstruction years after my mastectomy?", "Yes. Delayed reconstruction is routine and there is no time limit. Women treated ten or more years ago still have options, depending on their health and previous treatment."),
            ("Is breast reconstruction covered by insurance?", "Reconstruction after breast cancer, including surgery to the other breast for symmetry, is normally covered by UK private medical insurers as part of cancer treatment. Confirm with your insurer beforehand."),
        ],
        "related": ["breast-cancer-surgery", "fat-grafting"],
    },
    {
        "slug": "breast-reduction",
        "nav": "Breast reduction",
        "short_desc": "Reduction and symmetry",
        "summary": "Reduction mammoplasty for comfort and proportion, or to balance the breasts after cancer surgery.",
        "title": "Breast Reduction London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Breast reduction surgery in London and Essex with consultant oncoplastic surgeon Mr Zaker Ullah, for comfort, proportion or symmetry after cancer surgery.",
        "h1": "Breast reduction and symmetrisation",
        "lede": "Reduction mammoplasty reshapes heavy breasts into a lighter, higher and more comfortable form: for relief of symptoms, for proportion, or to balance the breasts after cancer surgery.",
        "glance": [("Anaesthetic", "General"), ("Operation", "Around two to three hours"), ("Hospital stay", "Day case or one night"), ("Recovery", "Desk work at one to two weeks, exercise at about six")],
        "sections": """
<h2>Who benefits</h2>
<p>Heavy breasts are a physical burden. Women describe pain in the neck, shoulders and back, grooves from bra straps, irritated skin beneath the breast and real limits on exercise. A reduction removes excess tissue and skin, lifts the breast and repositions the nipple. The scars fade considerably over the following one to two years.</p>
<h2>Symmetry after cancer surgery</h2>
<p>As an oncoplastic surgeon, much of Mr Ullah's reduction work is <strong>symmetrisation</strong>: reducing, lifting or reshaping one breast so that it matches a breast treated for cancer or reconstructed. It is a routine part of the reconstructive pathway and is usually covered by insurers as part of cancer treatment.</p>
<h2>The operation and recovery</h2>
<p>A breast reduction is performed under general anaesthetic, takes around two to three hours, and is done as a day case or with one night in hospital. Most women return to desk work within one to two weeks and to full exercise at about six weeks. Before any decision, Mr Ullah talks plainly about scar patterns, nipple sensation and the effect on breastfeeding.</p>
""",
        "faqs": [
            ("Will breast reduction affect nipple sensation or breastfeeding?", "Both can be affected. Some change in nipple sensation is common at first and usually improves, although it can be permanent. Many women can breastfeed after a reduction, but it cannot be guaranteed. If future breastfeeding matters to you, say so, because it influences technique and timing."),
            ("What scars does a breast reduction leave?", "Usually a scar around the areola, a vertical line down to the fold beneath the breast, and often a line within the fold itself, known as the anchor pattern. Scars are red and firm at first and fade considerably over 12 to 24 months."),
            ("Is breast reduction covered by insurance?", "Cosmetic reduction generally is not. Symmetrisation after breast cancer surgery is usually treated as part of reconstruction. Your insurer will confirm cover in advance."),
            ("How long is recovery after breast reduction?", "Most women are back at desk work within one to two weeks, driving at around two weeks, and exercising fully at about six weeks. A supportive bra is worn day and night for several weeks."),
        ],
        "related": ["breast-reconstruction", "fat-grafting"],
    },
    {
        "slug": "fat-grafting",
        "nav": "Fat grafting",
        "short_desc": "Lipofilling",
        "summary": "Using your own fat to refine shape after surgery, correct contour and soften scar tissue.",
        "title": "Breast Fat Grafting & Lipofilling London | Mr Zaker Ullah",
        "desc": "Fat grafting (lipofilling) to the breast in London and Essex: correcting dents after lumpectomy, refining reconstruction and softening radiotherapy changes.",
        "h1": "Fat grafting to the breast",
        "lede": "Fat grafting, also called lipofilling, moves a small amount of your own fat into the breast by gentle liposuction, to smooth contours, fill defects and soften scarred tissue. Mr Ullah introduced the technique at Whipps Cross.",
        "glance": [("Anaesthetic", "Usually general"), ("Hospital stay", "Day case"), ("Sessions", "One to three, about three months apart"), ("Final result", "Judged at around three months")],
        "sections": """
<h2>What it is used for</h2>
<p>In breast surgery, fat grafting is above all a refining technique. It fills a dent left by breast conserving surgery, smooths the edges of an implant reconstruction, softens tissue affected by radiotherapy and corrects small differences between the breasts. No foreign material is used, and the marks left at the donor and treated sites are tiny.</p>
<h2>How it works</h2>
<p>Fat is taken by gentle liposuction, usually from the abdomen or thighs, then purified and placed in the breast in fine threads so that each droplet gains a blood supply. A proportion of the grafted fat, commonly 30 to 50 per cent, is naturally absorbed over the first few months. For that reason larger corrections are often carried out over two or three sessions.</p>
<h2>Recovery</h2>
<p>Fat grafting is usually a day case. Bruising where the fat was taken is the main after effect, and most patients return to normal activity within a few days. The final result is assessed at around three months, once swelling has settled.</p>
""",
        "faqs": [
            ("Is fat grafting safe after breast cancer?", "Current evidence has not shown that fat grafting increases the risk of cancer returning, and it is widely used in reconstruction. Grafted fat can produce benign changes on mammograms, such as oil cysts or calcification, which specialists recognise. Always tell your imaging team that you have had fat grafting."),
            ("How many sessions will I need?", "Small refinements often need a single session. Larger corrections usually need two or three sessions about three months apart, because some of each graft is absorbed."),
            ("Does the transferred fat behave like normal fat?", "Yes. Once established, grafted fat is living tissue. It feels natural and will gain and lose volume with your weight, like fat elsewhere."),
        ],
        "related": ["breast-reconstruction", "breast-cancer-surgery"],
    },
    {
        "slug": "gynaecomastia",
        "nav": "Gynaecomastia",
        "short_desc": "Male breast reduction",
        "summary": "Specialist assessment of the male breast, and surgery for established gynaecomastia.",
        "title": "Gynaecomastia Surgery London & Essex | Mr Zaker Ullah FRCS",
        "desc": "Gynaecomastia (male breast reduction) in London and Essex with a consultant breast surgeon: specialist assessment, liposuction and gland excision, recovery and results.",
        "h1": "Gynaecomastia, or male breast reduction",
        "lede": "Enlargement of the male breast is common, benign in nearly every case, and treatable. It still deserves a specialist assessment, both to exclude the rare serious cause and to achieve a result worth having.",
        "glance": [("Anaesthetic", "General"), ("Hospital stay", "Day case"), ("Garment", "Compression vest for a few weeks"), ("Recovery", "Desk work at a week, exercise at four to six")],
        "sections": """
<h2>First, a diagnosis</h2>
<p>Gynaecomastia has many causes: hormonal change in adolescence and later life, weight, some medicines and, occasionally, an underlying medical condition. Male breast cancer is rare but does occur. For that reason assessment by a <strong>breast specialist</strong>, with imaging and biopsy where needed, comes before any discussion of surgery. Gynaecomastia in teenagers often settles without treatment, and some settles once the underlying cause is treated.</p>
<h2>Surgery</h2>
<p>Where the tissue is established and troubling, surgery removes it. Depending on the balance of gland and fat, Mr Ullah uses liposuction, removal of the gland through a small incision at the edge of the areola, or both. Where there is significant excess skin, further techniques may be needed, and he will explain them if they apply to you.</p>
<h2>Recovery and results</h2>
<p>The operation is usually a day case under general anaesthetic. A compression garment is worn for a few weeks. Most men return to desk work within a week and to full exercise at four to six weeks. The result is usually permanent, provided weight and any responsible medicine are managed.</p>
""",
        "faqs": [
            ("Is gynaecomastia dangerous?", "Almost never. It is a benign enlargement of breast gland tissue. A firm lump on one side, a lump that is growing, or discharge from the nipple should be assessed promptly to exclude male breast cancer, which is rare but does occur."),
            ("Will exercise get rid of gynaecomastia?", "Exercise and weight loss reduce the fatty part, but true gland tissue does not respond to exercise. This is why chest exercises often make no visible difference, and why removing the gland is part of the operation when gland predominates."),
            ("What scars are left after gynaecomastia surgery?", "Liposuction leaves a few marks a few millimetres long. Removing the gland usually adds a fine scar along the lower edge of the areola, where it tends to fade well."),
            ("Is gynaecomastia surgery covered by insurance?", "Usually not when it is cosmetic, although insurers may cover assessment of a new lump or a suspicious change. The hospital confirms self-pay prices in writing before you commit."),
        ],
        "related": ["benign-breast-conditions", "general-laparoscopic-surgery"],
    },
    {
        "slug": "general-laparoscopic-surgery",
        "nav": "Hernia and gallbladder",
        "short_desc": "Keyhole surgery",
        "summary": "Laparoscopic gallbladder removal, hernia repair and appendicectomy.",
        "title": "Keyhole Hernia & Gallbladder Surgery London | Mr Ullah FRCS",
        "desc": "Keyhole (laparoscopic) surgery in London and Essex: gallbladder removal, inguinal, umbilical and incisional hernia repair and appendicectomy with Mr Zaker Ullah.",
        "h1": "General and laparoscopic surgery",
        "lede": "Alongside his breast practice, Mr Ullah has a general surgical practice in laparoscopic, or keyhole, surgery: gallbladder removal, hernia repair and appendicectomy.",
        "glance": [("Approach", "Keyhole wherever suitable"), ("Hospital stay", "Usually a day case or one night"), ("Recovery", "Most people are back to normal within two weeks"), ("Research", "Published on laparoscopic hernia repair")],
        "sections": """
<h2>Gallstones and gallbladder removal</h2>
<p>Gallstones that cause pain, inflammation or pancreatitis are best treated by removing the gallbladder, an operation called <strong>laparoscopic cholecystectomy</strong>. It is performed through four small incisions and is one of the most common operations in the United Kingdom. Most patients go home the same day or after one night and return to normal activity within a fortnight. Life without a gallbladder is entirely normal.</p>
<h2>Hernia repair</h2>
<p>Mr Ullah repairs all types of hernia. A hernia in the groin (inguinal), at the navel (umbilical) or through a previous scar (incisional) will not repair itself. Mr Ullah repairs hernias by keyhole and by open surgery, usually reinforced with mesh, choosing the approach that suits the hernia and the patient. His keyhole hernia technique won the prize for best video presentation at the European Association for Endoscopic Surgery in 2003.</p>
<h2>Appendicectomy</h2>
<p>Suspected appendicitis needs urgent assessment. When surgery is required, a laparoscopic appendicectomy both confirms the diagnosis and treats it through small incisions, with a faster recovery than open surgery.</p>
""",
        "faqs": [
            ("What are the advantages of keyhole surgery?", "Smaller incisions mean less pain, a shorter stay in hospital, a faster return to work and smaller scars. Not every patient or condition is suitable, and a small proportion of keyhole operations are converted to open surgery for safety. That possibility is always discussed before consent."),
            ("How long does hernia repair recovery take?", "After keyhole repair most people return to desk work within one to two weeks and to heavy lifting at four to six weeks. Recovery after open repair takes a little longer. You may drive once you can make an emergency stop comfortably."),
            ("Do gallstones always need surgery?", "No. Gallstones found by chance that cause no symptoms can usually be left alone. Surgery is advised once they cause pain or complications, because further attacks are then likely."),
        ],
        "related": ["gynaecomastia", "benign-breast-conditions"],
    },
    {
        "slug": "lumps-cysts-skin-lesions",
        "nav": "Lumps, cysts and moles",
        "short_desc": "Minor skin surgery",
        "summary": "Removal of lipomas, sebaceous cysts, moles and other skin lesions, usually under local anaesthetic.",
        "title": "Lipoma, Cyst & Mole Removal Essex & London | Mr Zaker Ullah",
        "desc": "Private removal of lipomas, sebaceous cysts, moles and skin lesions at The Holly, Buckhurst Hill, and in London, by consultant surgeon Mr Zaker Ullah FRCS.",
        "h1": "Lumps, cysts, moles and skin lesions",
        "lede": "Lumps under the skin and changing moles are common reasons to see a surgeon. Mr Ullah assesses and removes them, usually as a short procedure under local anaesthetic, with every specimen sent for analysis.",
        "glance": [("Anaesthetic", "Usually local"), ("Procedure", "Often 20 to 45 minutes"), ("Hospital stay", "You go home the same day"), ("Results", "Laboratory report, usually within one to two weeks")],
        "sections": """
<h2>What Mr Ullah treats</h2>
<ul>
<li><strong>Lipomas</strong>: soft, slow growing lumps of fat under the skin</li>
<li><strong>Sebaceous (epidermoid) cysts</strong>, including those that keep becoming inflamed</li>
<li><strong>Moles and skin lesions</strong> that are changing, bleeding, catching on clothing or simply unwanted</li>
<li><strong>Abscesses</strong>, which need prompt drainage</li>
<li>Other <strong>soft tissue lumps</strong> that need a diagnosis</li>
</ul>
<h2>Assessment first</h2>
<p>Most lumps under the skin are harmless, but a few need a different plan. Mr Ullah examines the lump and, where it helps, arranges an ultrasound scan before deciding on treatment. A lump that is large, deep, growing quickly or painful is always imaged first. Any mole with features of concern is removed completely and examined in the laboratory, and if melanoma is confirmed, your care continues with the appropriate specialist team.</p>
<h2>The procedure</h2>
<p>Most lumps, cysts and moles are removed under local anaesthetic, through an incision planned to leave the neatest possible scar, closed with fine stitches. You go home the same day. Stitches usually come out after one to two weeks, and the laboratory report follows within a similar time.</p>
""",
        "faqs": [
            ("Is a lipoma dangerous?", "Lipomas are benign, and many can be left alone. They are usually removed when they are growing, uncomfortable or unwanted. A lump that is large, deep, painful or growing quickly should be scanned first to be sure of the diagnosis."),
            ("Will removing a sebaceous cyst leave a scar?", "There is always a small scar, usually a fine line a little longer than the cyst. Removing the whole cyst wall reduces the chance of it coming back."),
            ("Should a changing mole be checked?", "Yes. A mole that is changing in size, shape or colour, has an irregular edge, bleeds or itches should be seen promptly. Most are harmless, but a mole of concern is removed and examined in the laboratory."),
            ("Is minor skin surgery covered by insurance?", "Insurers usually cover the removal of lesions that are suspicious or causing symptoms, but not purely cosmetic removal. Self-funding patients receive a fixed price from the hospital in advance."),
        ],
        "related": ["general-laparoscopic-surgery", "benign-breast-conditions"],
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
    "duration": "PT34M04S", "duration_label": "34 minutes",
    "youtube": "rYpUCW_EbTY",
    "spotify": "https://open.spotify.com/episode/5bFR1v4vIfJxn29kMQ4yn1",
    "apple": "https://podcasts.apple.com/us/podcast/5-breast-cancer-questions-answered-by-a-surgeon/id1843133154?i=1000796268423",
    "summary": "Recorded before a live audience. Rosie Fawehimi, a breast cancer survivor, talks to the surgeon who diagnosed her and later performed her double mastectomy and reconstruction, and puts to him the five questions she is asked most often.",
    "chapters": [
        "Lumpectomy or mastectomy: how is the decision made?",
        "Symptoms, self examination and what to look for",
        "Is breast cancer rising in young women?",
        "Does everyone need radiotherapy?",
        "Triple negative breast cancer, explained",
    ],
}

# ------------------------------------------------------------- videos
# From the old Squarespace site (news) and Mr Ullah's YouTube channel. Titles via YouTube oEmbed.
YOUTUBE_CHANNEL = "https://www.youtube.com/channel/UC6iPKoum-L-S0sFh2Pe3Fbw"
VIDEOS = [
    {"slug": "breast-cancer-self-examination-in-bangla", "id": "wzwnucrNKV4", "date": "2022-10-26", "lang": "Bengali",
     "title": "Breast cancer self-examination, in Bangla",
     "desc": "For Breast Cancer Awareness Month 2022, Mr Ullah explains in Bangla the signs and symptoms of breast cancer and how to examine your own breasts.",
     "by": "His YouTube channel"},
    {"slug": "coronavirus-qampa-in-bangla", "id": "HT83gMhNxCo", "date": "2021-03-08", "lang": "Bengali",
     "title": "Coronavirus questions answered, in Bangla",
     "desc": "Mr Ullah answers common questions about coronavirus for Bengali-speaking families, recorded during the pandemic.",
     "by": "His YouTube channel"},
    {"slug": "covid-advice-with-dr-zaker-ullah", "id": "ZXobptg2HVQ", "date": "2021-03-08", "lang": "Bengali",
     "title": "COVID advice with Mr Zaker Ullah, on TV3 Bangla",
     "desc": "A health advice segment for TV3 Bangla, in which Mr Ullah answers viewers' questions about COVID-19.",
     "by": "TV3 Bangla"},
    {"slug": "health-advice", "id": "q8_1uiu2Vnk", "date": "2021-03-08", "lang": "Bengali",
     "title": "Health advice with Mr Zaker Ullah, on TV3 Bangla",
     "desc": "Mr Ullah's health advice programme for TV3 Bangla, answering viewers' questions on everyday health.",
     "by": "TV3 Bangla"},
]

# ------------------------------------------------------------- booking partners
# Verified profile pages. Patients book with the provider that suits their insurer and clinic.
HOLLY_APPTS_PHONE = "020 8505 3311"   # option 1, per Nuffield Health's own video
HOLLY_APPTS_TEL = "+442085053311"
HOLLY_APPTS_EMAIL = "hobkh.appointments@nuffieldhealth.com"
BOOKING_PARTNERS = [
    {"name": "Nuffield Health The Holly", "kind": "Hospital", "best": "Seeing Mr Ullah in Buckhurst Hill, insured or self-funding",
     "url": "https://www.nuffieldhealth.com/consultants/mr-md-zaker-ullah", "cta": "Book online with Nuffield",
     "extra": f"Or call {HOLLY_APPTS_PHONE}, option 1"},
    {"name": "Doctify", "kind": "Booking platform", "best": "Choosing a time online, at The Holly or in London",
     "url": "https://www.doctify.com/uk/specialist/mr-md-z-ullah", "cta": "Book on Doctify", "extra": ""},
    {"name": "Top Doctors", "kind": "Booking platform", "best": "Self-funding patients comparing appointments",
     "url": "https://www.topdoctors.co.uk/doctor/zaker-ullah/", "cta": "View on Top Doctors", "extra": ""},
    {"name": "Bupa Finder", "kind": "Insurer directory", "best": "Bupa members, including Open Referral",
     "url": "https://www.finder.bupa.co.uk/Consultant/view/192096/mr_md_z_ullah", "cta": "View on Bupa Finder", "extra": "Bupa Platinum consultant, fee-assured"},
]

# ------------------------------------------------------------- media mentions (text only, no logos)
AS_SEEN = [("Everything Changed podcast", "~/podcast/"), ("TV3 Bangla", "~/podcast/#bengali"), ("West Essex Life", "~/news/five-things-breast-cancer/"),
           ("PHA Global Summit 2024", "https://www.youtube.com/watch?v=gBP0rsPeJ9A"), ("Nuffield Health", "https://www.facebook.com/thehollyprivatehospital/videos/2402001463487795/")]
