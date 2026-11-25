"""Generates every page of the Super Dentist Clinic site into ./site/
Run:  python3 build.py   then rebuild CSS with the Tailwind CLI."""
import json, os
from content import SERVICES, DOCTORS

OUT = os.path.join(os.path.dirname(__file__), "site")
WA1, WA2 = "9647507227500", "9647761212111"
MAPS = "https://www.google.com/maps/search/?api=1&query=Super+Dentist+Clinic+Erbil"


def t(ar, en, ku, block=False):
    s = "-block" if block else ""
    return (f'<span class="lang-text lang-ar{s}">{ar}</span>'
            f'<span class="lang-text lang-en{s}">{en}</span>'
            f'<span class="lang-text lang-ku{s}">{ku}</span>')


def tt(d, block=False):
    return t(d["ar"], d["en"], d["ku"], block)


NAV = [
    ("index.html", ("الرئيسية", "Home", "سەرەکی")),
    ("index.html#services", ("الخدمات", "Services", "خزمەتگوزارییەکان")),
    ("doctors.html", ("أطباؤنا", "Doctors", "پزیشکەکانمان")),
    ("gallery.html", ("قبل وبعد", "Before & After", "پێش و دوای")),
    ("tour.html", ("جولة في العيادة", "Clinic Tour", "گەشتی کلینیک")),
    ("index.html#reviews", ("آراء المرضى", "Reviews", "بۆچوونەکان")),
    ("#contact", ("تواصل معنا", "Contact", "پەیوەندی")),
]


def nav(active):
    desk = "\n".join(
        f'<a href="{h}" class="whitespace-nowrap hover:text-deepBlue transition-colors sub{" text-deepBlue" if h == active else ""}">{t(*l)}</a>'
        for h, l in NAV)
    mob = "\n".join(
        f'<a href="{h}" class="py-2 border-b border-navyBlue/10 hover:text-deepBlue">{t(*l)}</a>' for h, l in NAV)
    return f'''
<nav class="fixed w-full z-50 site-header">
  <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 flex justify-between items-center relative gap-2 md:gap-4">
    <a href="index.html" class="flex items-center gap-2 md:gap-3 min-w-0">
      <span class="logo-metal" style="width:54px;height:44px"><img src="super-dentist-logo.png" alt="Super Dentist Clinic logo" width="54" height="44" style="width:54px;height:44px;object-fit:contain"></span>
      <span class="text-[15px] sm:text-lg md:text-xl font-bold text-navyBlue tracking-tight leading-tight ">{t("عيادة سوبر دينتست", "Super Dentist Clinic", "کلینیکی سوپەر دێنتست")}</span>
    </a>
    <div class="hidden lg:flex items-center gap-3 xl:gap-5 font-bold text-navyBlue text-[13.5px] xl:text-[15px]">{desk}</div>
    <div class="flex items-center gap-2 md:gap-3 shrink-0">
      <div class="flex bg-white/60 rounded-full p-1 border border-white/60 shadow-sm" role="group" aria-label="Language">
        <button type="button" onclick="changeLang('ar')" id="btn-ar" class="px-2.5 md:px-3 py-1.5 text-[13px] font-bold rounded-full transition-colors">AR</button>
        <button type="button" onclick="changeLang('en')" id="btn-en" class="px-2.5 md:px-3 py-1.5 text-[13px] font-bold rounded-full transition-colors">EN</button>
        <button type="button" onclick="changeLang('ku')" id="btn-ku" class="px-2.5 md:px-3 py-1.5 text-[13px] font-bold rounded-full transition-colors">KU</button>
      </div>
      <button type="button" id="mobile-menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" class="lg:hidden p-1.5 text-navyBlue">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
      <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" aria-label="WhatsApp" class="wa-link hidden lg:inline-flex items-center gap-2 p-2.5 xl:px-5 xl:py-2.5 text-sm font-bold text-white bg-whatsapp rounded-[14px] hover:bg-whatsappDark hover:-translate-y-px transition-all shadow-cta">
        <i class="fa-brands fa-whatsapp text-lg" aria-hidden="true"></i><span class="hidden xl:inline">{t("احجز عبر واتساب", "Book via WhatsApp", "نۆرە بگرە لە واتسئاپ")}</span>
      </a>
    </div>
  </div>
  <div id="mobile-menu" class="hidden lg:hidden absolute top-full left-0 w-full shadow-lg py-4 px-6 flex flex-col gap-2 text-center font-bold text-navyBlue rounded-b-2xl bg-white/95">
    {mob}
    <div class="flex justify-center gap-6 mt-2">
      <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link py-2 text-whatsapp flex items-center gap-2"><i class="fa-brands fa-whatsapp text-2xl" aria-hidden="true"></i>{t("واتساب", "WhatsApp", "واتسئاپ")}</a>
      <a href="tel:+{WA1}" dir="ltr" class="py-2 text-deepBlue flex items-center gap-2"><i class="fa-solid fa-phone text-xl" aria-hidden="true"></i>{t("اتصل", "Call", "پەیوەندی")}</a>
    </div>
  </div>
</nav>'''


MOBILE_CTA = f'''
<!-- Sticky booking bar: phones only -->
<div id="mobile-cta" class="md:hidden fixed inset-x-0 bottom-0 z-40 bg-white/95 border-t border-slate-200 shadow-[0_-4px_16px_rgba(15,23,42,.08)] px-3 pt-2 transition-transform duration-200" style="padding-bottom:calc(8px + env(safe-area-inset-bottom))">
  <div class="flex gap-2">
    <a href="tel:+{WA1}" class="flex-1 h-12 inline-flex items-center justify-center gap-2 rounded-[14px] border-[1.5px] border-slate-300 bg-white font-bold text-slate-900"><i class="fa-solid fa-phone" aria-hidden="true"></i>{t("اتصل", "Call", "پەیوەندی")}</a>
    <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link flex-[1.6] h-12 inline-flex items-center justify-center gap-2 rounded-[14px] bg-whatsapp hover:bg-whatsappDark font-bold text-white shadow-cta"><i class="fa-brands fa-whatsapp text-xl" aria-hidden="true"></i>{t("احجز عبر واتساب", "Book on WhatsApp", "نۆرە بگرە لە واتسئاپ")}</a>
  </div>
</div>'''

FOOTER = f'''
<footer id="contact" class="footer-glass crystal-panel relative z-10 mt-8 mb-24 md:mb-4 mx-3 md:mx-auto max-w-[1320px] text-slate-700">
  <div class="max-w-7xl mx-auto px-4 md:px-6 pt-14 pb-8">
    <div class="grid gap-10 md:grid-cols-[1.3fr_1fr_1.3fr]">
      <div class="space-y-4">
        <a href="index.html" class="inline-flex items-center gap-3">
          <span class="logo-metal" style="width:56px;height:44px"><img src="super-dentist-logo.png" alt="" width="56" height="44" style="width:56px;height:44px;object-fit:contain" loading="lazy"></span>
          <span class="text-xl font-bold text-navyBlue">{t("عيادة سوبر دينتست", "Super Dentist Clinic", "کلینیکی سوپەر دێنتست")}</span>
        </a>
        <p class="text-slate-600 max-w-[36ch]">{t("رعاية أسنان متكاملة في أربيل، من التقويم والزراعة إلى تجميل الابتسامة.", "Complete dental care in Erbil, from orthodontics and implants to smile design.", "چاودێری تەواوی ددان لە هەولێر، لە ڕاستکردنەوە و چاندنەوە تا جوانکاری خەندە.")}</p>
      </div>
      <nav aria-label="Footer">
        <h3 class="text-sm font-semibold text-navyBlue mb-4">{t("الصفحات", "Pages", "پەڕەکان")}</h3>
        <ul class="grid grid-cols-2 gap-x-6 gap-y-2.5 text-slate-700">
          <li><a class="hover:text-[#0062D6]" href="index.html#services">{t("الخدمات", "Services", "خزمەتگوزارییەکان")}</a></li>
          <li><a class="hover:text-[#0062D6]" href="doctors.html">{t("أطباؤنا", "Doctors", "پزیشکەکانمان")}</a></li>
          <li><a class="hover:text-[#0062D6]" href="gallery.html">{t("قبل وبعد", "Before &amp; After", "پێش و دوای")}</a></li>
          <li><a class="hover:text-[#0062D6]" href="tour.html">{t("جولة في العيادة", "Clinic Tour", "گەشتی کلینیک")}</a></li>
          <li><a class="hover:text-[#0062D6]" href="index.html#reviews">{t("آراء المرضى", "Reviews", "بۆچوونەکان")}</a></li>
          <li><a class="hover:text-[#0062D6]" href="hollywood-smile.html">{t("ابتسامة هوليود", "Hollywood Smile", "خەندەی هۆلیوود")}</a></li>
        </ul>
      </nav>
      <div class="space-y-4">
        <h3 class="text-sm font-semibold text-navyBlue">{t("تواصل معنا", "Contact", "پەیوەندی")}</h3>
        <p class="flex items-start gap-3"><i class="fa-solid fa-location-dot text-[#0062D6] mt-1" aria-hidden="true"></i><span>{t("أربيل - شارع 120م - لالاف سيتي فيو", "Erbil - 120m Street - Lalav City View", "هەولێر - شەقامی 120م - لالاف ستی ڤیو")}<br><a href="https://www.google.com/maps/dir/?api=1&destination=Super+Dentist+Clinic+Erbil" target="_blank" rel="noopener" class="text-[#0062D6] hover:underline text-sm">{t("الاتجاهات", "Get directions", "ڕێنمایی ڕێگا")}</a></span></p>
        <p class="flex items-start gap-3"><i class="fa-regular fa-clock text-[#0062D6] mt-1" aria-hidden="true"></i><span>{t("مفتوح 24 ساعة، طوال أيام الأسبوع", "Open 24 hours, 7 days a week", "24 کاتژمێر کراوەیە، هەموو ڕۆژانی هەفتە")}<br><span class="text-sm text-slate-600">{t("بما في ذلك حالات الطوارئ", "Including emergencies", "لەگەڵ حاڵەتە فریاکەوتنەکان")}</span></span></p>
        <div class="flex items-center gap-3" dir="ltr">
          <i class="fa-solid fa-phone text-[#0062D6]" aria-hidden="true"></i>
          <a href="tel:+{WA1}" dir="ltr" class="tracking-wide text-navyBlue hover:underline">+964 750 722 7500</a>
          <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" aria-label="WhatsApp" class="wa-link text-[#15803D] text-xl"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>
        </div>
        <div class="flex items-center gap-3" dir="ltr">
          <i class="fa-solid fa-phone text-[#0062D6]" aria-hidden="true"></i>
          <a href="tel:+{WA2}" dir="ltr" class="tracking-wide text-navyBlue hover:underline">+964 776 121 2111</a>
          <a href="https://wa.me/{WA2}" target="_blank" rel="noopener" aria-label="WhatsApp" class="wa-link text-[#15803D] text-xl"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>
        </div>
      </div>
    </div>
    <p class="mt-12 pt-6 border-t border-slate-900/10 text-sm text-slate-600 text-center leading-relaxed">
      &copy; <span id="year" dir="ltr">2026</span>
      {t('جميع الحقوق محفوظة لشركة وي سكيور We Secure للتصميم والاعلان وتكنولوجيا المعلومات | <span dir="ltr">07703060331</span>',
         'All rights reserved to We Secure for Design, Advertising &amp; IT | <span dir="ltr">07703060331</span>',
         'هەموو مافێک پارێزراوە بۆ کۆمپانیای We Secure بۆ دیزاین و ڕیکلام و تەکنەلۆجیای زانیاری | <span dir="ltr">07703060331</span>')}
    </p>
  </div>
</footer>'''


def page(filename, titles, desc, body, active="", video=False, head_extra="", scripts=""):
    if video:
        bg = ""
        body_cls = ""
    else:
        bg = ""
        body_cls = ""
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl" data-title-ar="{titles['ar']}" data-title-en="{titles['en']}" data-title-ku="{titles['ku']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titles['ar']}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1a365d">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{titles['ar']}">
<meta property="og:description" content="{desc}">
<!-- TODO: og:image needs a full URL once you have a domain, e.g. https://YOUR-DOMAIN/super-dentist-logo.png -->
<meta property="og:image" content="super-dentist-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<!-- Pre-built Tailwind CSS. If you add new Tailwind classes, styles.css must be rebuilt. -->
<link rel="stylesheet" href="styles.css?v=33">
{head_extra}
</head>
<body class="pb-[76px] md:pb-0 antialiased relative selection:bg-navyBlue selection:text-white font-sans {body_cls}">
{bg}
{nav(active)}
<main>
{body}
</main>
{FOOTER}
{MOBILE_CTA}
{scripts}
<script src="site.js?v=33"></script>
<!-- AI Assistant Chat Widget -->
<script src="https://app.aiassist.chat/widget.js" data-site-id="82ca7860-756f-42e5-a851-264dc3e4ab57" data-api-url="https://engine.aiassist.chat" async></script>
</body>
</html>
'''
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)


def wa_btn(text_ar, text_en, text_ku, label, cls="px-8 py-3 text-base"):
    return (f'<a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" '
            f'data-wa-ar="{text_ar}" data-wa-en="{text_en}" data-wa-ku="{text_ku}" '
            f'class="wa-link inline-flex items-center justify-center gap-2 {cls} font-bold text-white bg-whatsapp rounded-[14px] hover:bg-whatsappDark hover:-translate-y-px transition-all shadow-cta">'
            f'<i class="fa-brands fa-whatsapp text-xl" aria-hidden="true"></i>{label}</a>')


def page_header(title_html, sub_html=""):
    return f'''
<section class="page-head">
  <div class="max-w-5xl mx-auto px-4 md:px-6 text-center space-y-4">
    <h1 class="t-h1 font-bold text-navyBlue">{title_html}</h1>
    {f'<p class="t-lead text-slate-600 max-w-[60ch] mx-auto">{sub_html}</p>' if sub_html else ''}
  </div>
</section>'''


SVC = {s["slug"]: s for s in SERVICES}

# ====================================================================== HOME
def build_home():
    doctors = ""
    for d in DOCTORS:
        doctors += f'''
<a href="doctors.html#{d["id"]}" class="doctor-card relative isolate w-full max-w-[420px] sm:max-w-none sm:w-[calc(50%-12px)] lg:w-[calc(33.333%-16px)] aspect-[3/4] rounded-[20px] overflow-hidden bg-slate-200 hover:-translate-y-0.5 transition-transform border border-slate-200 shadow-[0_1px_2px_rgba(15,23,42,.04),0_8px_24px_rgba(15,23,42,.08)] group/item flex flex-col justify-end p-6 md:p-8">
  <div class="absolute inset-0 bg-gradient-to-t from-[#0A192F]/90 via-[#0A192F]/25 via-40% to-transparent z-0"></div>
  <img src="{d["photo"]}" loading="lazy" class="absolute top-0 left-0 w-full h-full object-cover object-top z-[-1]" alt="{d["name"]["en"]}">
  <div class="relative z-10 p-1">
    <h3 class="t-h3 font-semibold text-white mb-1">{tt(d["name"])}</h3>
    <p class="text-[#7DD3FC] font-semibold text-sm md:text-base">{tt(d["role"])}</p>
    <span class="inline-block mt-2 text-sm font-semibold text-white/85 underline underline-offset-4 decoration-white/40">{t("الملف الشخصي ←", "View profile →", "پرۆفایل ←")}</span>
  </div>
</a>'''

    COVERS = {
        "hollywood-smile": ("fa-face-smile-beam", "#2563EB", "#7DD3FC"),
        "dental-implants": ("fa-tooth", "#0E7490", "#5EEAD4"),
        "cosmetic-dentistry": ("fa-wand-magic-sparkles", "#7C3AED", "#F0ABFC"),
        "orthodontics": ("fa-teeth", "#1D4ED8", "#A5B4FC"),
        "root-canal": ("fa-teeth-open", "#0F766E", "#99F6E4"),
        "pediatric-dentistry": ("fa-child-reaching", "#EA580C", "#FDE68A"),
        "laser-whitening": ("fa-sun", "#0284C7", "#E0F2FE"),
    }
    services = ""
    for s in SERVICES:
        icon, c1, c2 = COVERS[s["slug"]]
        services += f'''
<a href="{s["slug"]}.html" class="svc-card glass-panel group flex flex-col !p-0 w-full max-w-[420px] sm:max-w-none sm:w-[calc(50%-8px)] md:w-[calc(33.333%-11px)] lg:w-[calc(25%-12px)]">
  <div class="svc-cover has-photo relative aspect-[16/10] overflow-hidden rounded-t-[23px]" style="--c1:{c1};--c2:{c2}" >
    <img src="services/{s["slug"]}.jpg" alt="{s["title"]["en"]}" width="1200" height="750" loading="lazy" onerror="this.onerror=null;this.src='services/{s["slug"]}.svg'">
  </div>
  <div class="p-4 flex flex-col gap-1.5 flex-1">
    <h3 class="text-base md:text-[17px] font-semibold text-navyBlue">{tt(s["title"])}</h3>
    <p class="text-slate-600 text-sm leading-relaxed line-clamp-2">{tt(s["intro"])}</p>
    <span class="mt-auto pt-1.5 text-[13px] font-semibold text-deepBlue">{t("اعرف المزيد ←", "Learn more →", "زیاتر بزانە ←")}</span>
  </div>
</a>'''

    jsonld = {
        "@context": "https://schema.org", "@type": "Dentist",
        "name": "Super Dentist Clinic", "alternateName": "عيادة سوبر دينتست",
        "image": "super-dentist-logo.png",
        "telephone": ["+" + WA1, "+" + WA2],
        "address": {"@type": "PostalAddress", "streetAddress": "120m Street, Lalav City View",
                    "addressLocality": "Erbil", "addressCountry": "IQ"},
        "medicalSpecialty": ["Orthodontic", "CosmeticDentistry"],
        "availableLanguage": ["ar", "en", "ku"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "00:00", "closes": "23:59"}],
    }
    head = ('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'
            '')

    reviews_script = '''
<script>
/* =====================  GOOGLE REVIEWS  =====================
   OPTION A - automatic & live (recommended):
     1. In Google Cloud Console create an API key and enable "Maps JavaScript API" and "Places API (New)".
        Restrict the key to your website (HTTP referrers: lewaaalobaidi-byte.github.io/*).
     2. Find the clinic's Place ID:
        https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder
     3. Paste both below. The site then shows the live rating, review count and up to 5 latest reviews.
   OPTION B - by hand: leave apiKey empty and paste real reviews WORD FOR WORD into REVIEWS:
     { name: 'Ahmed K.', stars: 5, month: '2026-11', text: 'review text exactly as on Google' },   (month = year-month it was posted)
*/
window.GOOGLE_REVIEWS = { apiKey: '', placeId: '' };
window.REVIEWS = [
  { name: 'Mohamad Ali S.', stars: 5, month: '2026-09', text: 'We called them after midnight, and they were incredibly responsive, accommodating, and professional. By the time we arrived, they were already waiting for us.\\n\\nDr. Mohammed and Dr. Sawin were both extremely friendly, welcoming, and reassuring. They performed the necessary procedure immediately, smoothly, and with great professionalism.\\n\\nWhat really stood out to us was the way they treated us. They made us feel more like family than regular patients, even though they stayed at the clinic until the early hours of the morning to make sure everything was taken care of.\\n\\nI highly recommend Dr. Mohammed and Dr. Sawin to anyone looking for caring, professional, and trustworthy doctors. Truly excellent service and exceptional human beings.' },
  { name: 'Miran H.', stars: 5, month: '2026-02', text: 'Best service ever! I called for an emergency on Friday, and they responded very quickly and took care of everything the same day. Excellent service and very professional staff. Highly recommended!' },
  { name: 'رؤى ر.', stars: 5, month: '2026-02', text: 'Excellent experience for my little daughter she didn’t feel any pain thanks for the 2 amazing dentists who were very professional in dealing with her fear!!! Definitely I’d  recommend ppl to do their teeth here!!!' },
  { name: 'Mayss L.', stars: 5, month: '2026-01', text: 'عيادة تجنن مريحة ولطيفة والدكتور جداً متعاون ومتفهم ويسمع للمريض ويحاول بكل الطرق يخلي مرتاح وراضي يفهم بادق التفاصيل وينطي اجابات مقنعة ودقيقة كل التوفيق 💗' },
  { name: 'RANDOMIII S.', stars: 5, month: '2026-07', text: 'Such a great dentist with great work , didn’t feel any pain it was quick , smooth and with great results. Definitely the best dentist in erbil 💗' },
  { name: 'Taranom A.', stars: 5, month: '2026-01', text: 'أتقدم بخالص الشكر والتقدير إلى طبيب الأسنان العزيز وكادره الطبي المتفاني واللطيف. إن حسن التعامل، والصبر، والدقة في العمل جعلت تجربتي مريحة وممتعة. أتمنى لكم دوام الصحة والتوفيق والنجاح المستمر' },
  { name: 'Aiesha A.', stars: 5, month: '2026-02', text: 'I had an excellent experience. The dentist did an amazing job and was very professional and gentle. The entire team was incredibly friendly and welcoming, which made me feel comfortable from the moment I arrived. I’m very happy with the results and highly recommend this clinic.' },
  { name: 'alaa 2001', stars: 5, month: '2026-10', text: 'موجودين لحالات الطوارئ 24 ساعة شغلهم كلش زين واسعارهم مناسبه شكرا' },
  { name: 'zayn A.', stars: 5, month: '2026-01', text: 'احسن عيادة أسنان خابرت الدكتور ساعة ٤ الفجر واجة ومقصر وشكرا جزيلاً' },
  { name: 'Rawand B.', stars: 5, month: '2026-09', text: 'I had cleaning, and filling done. Was happy with the speed of the procedure and the capabilties of the whole staff.' }
];
</script>'''

    body = f'''
<!-- Video background: only behind the hero + stats -->
<div class="relative overflow-hidden">
  <div class="absolute inset-0 z-0 pointer-events-none bg-slate-200 video-fade" aria-hidden="true">
    <video id="bg-video" autoplay loop muted playsinline preload="metadata" poster="clinic-bg-poster.jpg" class="bg-video w-full h-full object-cover">
      <source src="clinic-doctors-bg-hq.mp4" type="video/mp4" media="(min-width: 768px)">
      <source src="clinic-doctors-bg.mp4" type="video/mp4">
    </video>
    <div class="absolute inset-0 hero-overlay"></div>
    
  </div>
<section id="home" class="relative min-h-[600px] md:min-h-[min(78svh,720px)] flex items-center overflow-hidden">
  <div class="max-w-7xl mx-auto px-4 md:px-6 w-full relative z-10 pt-24">
    <div class="crystal-panel crystal-dark space-y-5 md:space-y-6 max-w-2xl p-7 md:p-11">
      <span class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/12 border border-white/30 text-white text-sm font-semibold"><span class="relative flex w-2.5 h-2.5"><span class="absolute inset-0 rounded-full bg-[#4ADE80] animate-ping opacity-60"></span><span class="relative w-2.5 h-2.5 rounded-full bg-[#4ADE80]"></span></span>{t("مفتوح 24/7، حتى للطوارئ", "Open 24/7, including emergencies", "24/7 کراوەیە، بۆ فریاکەوتنیش")}</span>
      <h1 class="t-display font-bold text-white">
        {t("ابتسامتك،", "Your Smile,", "خەندەکەت،", block=True)}
        <span class="text-[#7DD3FC]">{t("شغفنا.", "Our Passion.", "خولیای ئێمەیە.")}</span>
      </h1>
      <p class="t-lead text-white/90 max-w-[60ch]">{t("نجمع بين أمهر الأطباء وأحدث التقنيات لنمنحك الرعاية التي تستحقها.", "Combining top specialists and the latest technology to give you the care you deserve.", "باشترین پزیشکەکان و نوێترین تەکنەلۆژیا کۆدەکەینەوە بۆ پێدانی ئەو چاودێرییەی شایستەیت.")}</p>
      <div class="pt-4 flex flex-wrap gap-3">
        <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link inline-flex items-center gap-2 px-8 py-3 font-bold text-white bg-whatsapp rounded-[14px] hover:bg-whatsappDark hover:-translate-y-px transition-all shadow-cta"><i class="fa-brands fa-whatsapp text-xl" aria-hidden="true"></i>{t("احجز موعدك", "Book an Appointment", "نۆرە بگرە")}</a>
        <a href="tel:+{WA1}" dir="ltr" class="inline-flex items-center gap-2 px-8 py-3 font-bold text-white bg-white/10 rounded-[14px] border-[1.5px] border-white/60 hover:bg-white/20 transition-colors"><i class="fa-solid fa-phone" aria-hidden="true"></i>{t("اتصل بنا", "Call Us", "پەیوەندیمان پێوە بکە")}</a>
      </div>
    </div>
  </div>
</section>

<!-- Stats. TODO: confirm these numbers with the clinic -->
<section id="stats" class="pt-0 pb-14 md:pb-20 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 text-center">
    <div class="stat-tile p-4 md:p-6 rounded-[20px] flex flex-col items-center"><span class="text-3xl md:text-5xl font-bold text-deepBlue" dir="ltr">5000<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("علاج ناجح", "Successful Treatments", "چارەسەری سەرکەوتوو")}</span></div>
    <div class="stat-tile p-4 md:p-6 rounded-[20px] flex flex-col items-center"><span class="text-3xl md:text-5xl font-bold text-deepBlue" dir="ltr">4782<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("مريض سعيد", "Happy Patients", "نەخۆشی دڵخۆش")}</span></div>
    <div class="stat-tile p-4 md:p-6 rounded-[20px] flex flex-col items-center"><span class="text-3xl md:text-5xl font-bold text-deepBlue" dir="ltr">5.0 <span class="text-yellow-500 text-2xl md:text-3xl">★</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("تقييم جوجل", "Google Rating", "هەڵسەنگاندنی گوگڵ")}</span></div>
    <div class="stat-tile p-4 md:p-6 rounded-[20px] flex flex-col items-center"><span class="text-3xl md:text-5xl font-bold text-deepBlue" dir="ltr">35<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("سنوات الخبرة", "Years of Experience", "ساڵانی ئەزموون")}</span></div>
  </div>
</section>

</div>

<section id="specialists" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <h2 class="text-center mb-8 md:mb-12 t-h2 font-bold text-navyBlue">{t('فريقنا <span class="text-deepBlue">الطبي</span>', 'Our Medical <span class="text-deepBlue">Team</span>', 'تیمی <span class="text-deepBlue">پزیشکیمان</span>')}</h2>
    <div class="flex flex-wrap justify-center gap-4 md:gap-6">{doctors}</div>
  </div>
</section>

<section id="services" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <h2 class="text-center mb-8 md:mb-12 t-h2 font-bold text-navyBlue">{t('خدمات <span class="text-deepBlue">العيادة</span>', 'Clinic <span class="text-deepBlue">Services</span>', 'خزمەتگوزارییەکانی <span class="text-deepBlue">کلینیک</span>')}</h2>
    <div class="flex flex-wrap justify-center gap-4">{services}</div>
  </div>
</section>

<!-- Gallery + tour teasers -->
<section id="teasers" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 grid md:grid-cols-2 gap-6">
    <a href="gallery.html" class="glass-panel bg-white/75 hover:bg-white/90 rounded-[2rem] p-8 md:p-10 flex flex-col gap-3">
      <i class="fa-solid fa-wand-magic-sparkles text-3xl text-deepBlue" aria-hidden="true"></i>
      <h2 class="t-h3 font-bold text-navyBlue">{t("نتائج قبل وبعد", "Before &amp; After", "ئەنجامی پێش و دوای")}</h2>
      <p class="text-slate-600 font-normal">{t("شاهد نتائج حقيقية لمرضانا في ابتسامة هوليود والتقويم والتبييض.", "See real results from our patients: Hollywood Smile, orthodontics, whitening and more.", "ئەنجامی ڕاستەقینەی نەخۆشەکانمان ببینە لە خەندەی هۆلیوود، ڕاستکردنەوە و سپیکردنەوەدا.")}</p>
      <span class="font-bold text-deepBlue">{t("عرض المعرض ←", "View gallery →", "بینینی گەلەری ←")}</span>
    </a>
    <a href="tour.html" class="glass-panel bg-white/75 hover:bg-white/90 rounded-[2rem] p-8 md:p-10 flex flex-col gap-3">
      <i class="fa-solid fa-house-medical text-3xl text-deepBlue" aria-hidden="true"></i>
      <h2 class="t-h3 font-bold text-navyBlue">{t("جولة في العيادة", "Clinic Tour", "گەشتێک بە کلینیکدا")}</h2>
      <p class="text-slate-600 font-normal">{t("تعرّف على عيادتنا وتجهيزاتها قبل زيارتك.", "Take a look inside our clinic and equipment before your visit.", "پێش سەردانەکەت کلینیک و ئامێرەکانمان ببینە.")}</p>
      <span class="font-bold text-deepBlue">{t("ابدأ الجولة ←", "Start the tour →", "دەستپێکردنی گەشت ←")}</span>
    </a>
  </div>
</section>

<section id="reviews" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 space-y-8">
    <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
      <h2 class="t-h2 font-bold text-navyBlue">{t('ماذا يقول <span class="text-deepBlue">مرضانا</span>', 'What Our <span class="text-deepBlue">Patients Say</span>', 'نەخۆشەکانمان <span class="text-deepBlue">چی دەڵێن</span>')}</h2>
      <div id="g-summary" class="card rounded-3xl px-5 py-4 flex flex-wrap items-center gap-x-5 gap-y-3">
        <div class="flex items-center gap-3">
          <svg class="w-7 h-7 shrink-0" viewBox="0 0 24 24" aria-hidden="true"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
          <div>
            <div class="flex items-center gap-2"><span id="g-rating" class="text-3xl font-bold text-navyBlue" dir="ltr">5.0</span><span class="text-yellow-400 text-xl tracking-wider" aria-hidden="true">★★★★★</span></div>
            <a id="g-count-link" href="{MAPS}" target="_blank" rel="noopener" class="text-sm font-bold text-slate-600 hover:text-deepBlue"><span id="g-count" dir="ltr">131</span> {t("مراجعة على جوجل", "Google reviews", "پێداچوونەوە لە گوگڵ")}</a>
          </div>
        </div>
        <!-- TODO: your write-a-review link: https://search.google.com/local/writereview?placeid=YOUR_PLACE_ID -->
        <a id="g-write" href="{MAPS}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-5 py-2.5 font-bold text-white bg-[#1a73e8] rounded-[14px] hover:bg-[#1558b0] text-sm"><i class="fa-solid fa-pen" aria-hidden="true"></i>{t("اكتب تقييمك", "Write a review", "هەڵسەنگاندن بنووسە")}</a>
      </div>
    </div>

    <!-- Live Google reviews from Trustindex (replaces the manual list below while it loads correctly) -->
    <div id="ti-widget" class="min-h-[1px]">
      <script defer async src="https://cdn.trustindex.io/loader.js?2119ee586e95519c9796397d2c3"></script>
    </div>

    <!-- Backup: the manual reviews below show only if the Trustindex widget does not load -->
    <div id="reviews-wrap" class="hidden relative">
      <div id="reviews-track" class="flex gap-4 md:gap-6 overflow-x-auto snap-x snap-mandatory scroll-smooth pb-4 no-scrollbar"></div>
      <button type="button" id="rv-prev" aria-label="Previous" class="hidden md:flex absolute top-[45%] -translate-y-1/2 -start-5 w-11 h-11 rounded-full bg-white shadow-lg text-navyBlue items-center justify-center hover:bg-sky-50 text-xl font-bold"><i class="fa-solid fa-chevron-left rtl:rotate-180" aria-hidden="true"></i></button>
      <button type="button" id="rv-next" aria-label="Next" class="hidden md:flex absolute top-[45%] -translate-y-1/2 -end-5 w-11 h-11 rounded-full bg-white shadow-lg text-navyBlue items-center justify-center hover:bg-sky-50 text-xl font-bold"><i class="fa-solid fa-chevron-right rtl:rotate-180" aria-hidden="true"></i></button>
      <div id="rv-dots" class="flex justify-center gap-2 mt-2"></div>
      <p id="rv-attrib" class="hidden text-center text-xs text-slate-500 font-semibold mt-2">{t("المراجعات من خرائط جوجل", "Reviews from Google Maps", "پێداچوونەوەکان لە نەخشەی گوگڵەوە")}</p>
    </div>

    <div id="reviews-empty" class="card rounded-3xl p-8 text-center space-y-4">
      <p class="text-navyBlue font-bold text-lg">{t("اقرأ تجارب مرضانا الحقيقية على جوجل.", "Read real experiences from our patients on Google.", "ئەزموونی ڕاستەقینەی نەخۆشەکانمان لە گوگڵ بخوێنەوە.")}</p>
      <a href="{MAPS}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-6 py-3 font-bold text-white bg-navyBlue rounded-[14px] hover:bg-[#0A192F] transition-colors">{t("عرض جميع المراجعات", "See all reviews", "هەموو پێداچوونەوەکان ببینە")}</a>
    </div>
  </div>
</section>

<section id="location" class="pb-12 md:pb-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <!-- TODO: replace src with the official embed (Google Maps -> Share -> Embed a map) -->
    <div class="h-[320px] md:h-[420px] card rounded-[2rem] overflow-hidden p-2">
      <iframe src="https://maps.google.com/maps?q=Super+dentists+clinic+Erbil&t=&z=16&ie=UTF8&iwloc=&output=embed" title="Super Dentist Clinic location" width="100%" height="100%" style="border:0;border-radius:1.5rem" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>'''
    page("index.html",
         {"ar": "عيادة سوبر دينتست | أربيل", "en": "Super Dentist Clinic | Erbil", "ku": "کلینیکی سوپەر دێنتست | هەولێر"},
         "عيادة سوبر دينتست في أربيل - تقويم وزراعة وتجميل الأسنان، ابتسامة هوليود وتبييض بالليزر. Super Dentist Clinic, Erbil.",
         body, active="index.html", video=True, head_extra=head, scripts=reviews_script)


# ====================================================================== SERVICES
def build_services():
    for s in SERVICES:
        def li(items, numbered=False):
            out = ""
            for i in range(len(items["en"])):
                mark = (f'<span class="shrink-0 w-8 h-8 rounded-full bg-deepBlue text-white flex items-center justify-center font-bold text-sm">{i+1}</span>'
                        if numbered else '<i class="fa-solid fa-check text-deepBlue mt-1.5" aria-hidden="true"></i>')
                out += f'<li class="flex gap-3 items-start">{mark}<span class="font-normal text-slate-700 leading-relaxed">{t(items["ar"][i], items["en"][i], items["ku"][i])}</span></li>'
            return out

        gallery_link = ""
        if s["gallery"]:
            gallery_link = f'<a href="gallery.html#{s["gallery"]}" class="inline-flex items-center gap-2 px-8 py-3 font-bold text-slate-900 bg-white rounded-[14px] border-[1.5px] border-slate-300 hover:border-navyBlue transition-colors"><i class="fa-solid fa-images" aria-hidden="true"></i>{t("شاهد نتائج قبل وبعد", "See before &amp; after results", "ئەنجامی پێش و دوای ببینە")}</a>'

        others = "".join(
            f'<a href="{o["slug"]}.html" class="card rounded-2xl px-4 py-3 font-bold text-navyBlue hover:text-deepBlue text-center">{tt(o["title"])}</a>'
            for o in SERVICES if o["slug"] != s["slug"])

        ti = s["title"]
        body = page_header(tt(ti), tt(s["intro"])) + f'''
<section class="pb-10">
  <div class="max-w-5xl mx-auto px-4 md:px-6 space-y-6">
    <div class="flex flex-wrap justify-center gap-3">
      {wa_btn("مرحباً، أود الاستفسار عن " + ti["ar"] + " في عيادة سوبر دينتست",
              "Hello, I'd like to ask about " + ti["en"] + " at Super Dentist Clinic",
              "سڵاو، دەمەوێت پرسیار بکەم دەربارەی " + ti["ku"] + " لە کلینیکی سوپەر دێنتست",
              t("احجز استشارة", "Book a consultation", "نۆرەی ڕاوێژ بگرە"))}
      {gallery_link}
    </div>
    <div class="grid md:grid-cols-2 gap-6">
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="t-h3 font-semibold text-navyBlue mb-4">{t("لمن هذا العلاج؟", "Who is it for?", "ئەم چارەسەرە بۆ کێیە؟")}</h2>
        <ul class="space-y-3">{li(s["who"])}</ul>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="t-h3 font-semibold text-navyBlue mb-4">{t("خطوات العلاج", "How it works", "هەنگاوەکانی چارەسەر")}</h2>
        <ol class="space-y-3">{li(s["steps"], numbered=True)}</ol>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="t-h3 font-semibold text-navyBlue mb-4">{t("كم يستغرق؟", "How long does it take?", "چەند دەخایەنێت؟")}</h2>
        <p class="flex gap-3 items-start font-semibold text-slate-700"><i class="fa-regular fa-clock text-deepBlue mt-1" aria-hidden="true"></i>{tt(s["duration"])}</p>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="t-h3 font-semibold text-navyBlue mb-4">{t("بعد العلاج", "Aftercare", "دوای چارەسەر")}</h2>
        <ul class="space-y-3">{li(s["after"])}</ul>
      </div>
    </div>
    <!-- TODO (optional): add a price range, e.g. "Starting from ..." -->
    <p class="text-center text-sm text-slate-600 font-semibold">{t("كل حالة مختلفة؛ يحدد الطبيب خطة العلاج المناسبة لك بعد الفحص.", "Every case is different. Your dentist will confirm the right plan for you after an examination.", "هەر حاڵەتێک جیاوازە؛ پزیشک دوای پشکنین پلانی گونجاوت بۆ دیاری دەکات.")}</p>
  </div>
</section>
<section class="py-10">
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <h2 class="t-h3 font-semibold text-navyBlue mb-4 text-center">{t("خدمات أخرى", "Other services", "خزمەتگوزاری تر")}</h2>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-3">{others}</div>
  </div>
</section>'''
        page(s["slug"] + ".html",
             {l: f'{ti[l]} | {"عيادة سوبر دينتست أربيل" if l=="ar" else "Super Dentist Clinic Erbil" if l=="en" else "کلینیکی سوپەر دێنتست هەولێر"}' for l in ("ar", "en", "ku")},
             f'{ti["ar"]} في أربيل - عيادة سوبر دينتست. {s["intro"]["ar"]}',
             body, active="index.html#services")


# ====================================================================== DOCTORS
def build_doctors():
    cards = ""
    for d in DOCTORS:
        links = "".join(
            f'<a href="{sl}.html" class="px-4 py-2 rounded-full bg-sky-50 text-navyBlue font-bold text-sm hover:bg-sky-100">{tt(SVC[sl]["title"])}</a>'
            for sl in d["services"])
        gal = ""
        n = d["name"]
        bio_html = ""
        if d.get("bio"):
            facts = "".join(f'<li class="flex items-start gap-3"><i class="fa-solid {ic} text-deepBlue mt-1 w-5 text-center" aria-hidden="true"></i><span>{tt(tx)}</span></li>' for ic, tx in d.get("facts", []))
            bio_html = f'<p class="text-slate-700 leading-relaxed max-w-[62ch]">{tt(d["bio"])}</p>' + (f'<ul class="space-y-2 text-slate-700 font-medium">{facts}</ul>' if facts else "")
        cards += f'''
<article id="{d["id"]}" class="card rounded-[2rem] overflow-hidden grid md:grid-cols-[320px_1fr]">
  <img src="{d["photo"]}" alt="{n["en"]}" loading="lazy" class="w-full h-80 md:h-full object-cover object-top">
  <div class="p-6 md:p-10 space-y-5">
    <div>
      <h2 class="t-h2 font-bold text-navyBlue">{tt(n)}</h2>
      <p class="text-deepBlue font-bold text-lg mt-1">{tt(d["role"])}</p>
    </div>
    <!-- TODO: fill in the doctor's real details, then remove the comment markers.
    <p class="text-slate-700 font-semibold leading-relaxed">
      <span class="lang-text lang-ar">نبذة قصيرة عن الطبيب ...</span>
      <span class="lang-text lang-en">Short bio ...</span>
      <span class="lang-text lang-ku">کورتەیەک دەربارەی پزیشک ...</span>
    </p>
    <ul class="space-y-2 font-semibold text-slate-700">
      <li><i class="fa-solid fa-graduation-cap text-deepBlue w-6" aria-hidden="true"></i> University / degree ...</li>
      <li><i class="fa-solid fa-briefcase-medical text-deepBlue w-6" aria-hidden="true"></i> Years of experience ...</li>
      <li><i class="fa-solid fa-language text-deepBlue w-6" aria-hidden="true"></i> Arabic, Kurdish, English ...</li>
    </ul>
    -->
    {bio_html}
    {f'<div class="flex flex-wrap gap-2">{links}</div>' if links else ''}
    <div class="flex flex-wrap gap-3 pt-2">
      {wa_btn("مرحباً، أود حجز موعد مع " + n["ar"], "Hello, I'd like to book an appointment with " + n["en"], "سڵاو، دەمەوێت نۆرەیەک بگرم لای " + n["ku"],
              t("احجز مع الطبيب", "Book with this doctor", "نۆرە بگرە لای ئەم پزیشکە"), cls="px-6 py-3")}
      {gal}
    </div>
  </div>
</article>'''
    body = page_header(t('فريقنا <span class="text-deepBlue">الطبي</span>', 'Our Medical <span class="text-deepBlue">Team</span>', 'تیمی <span class="text-deepBlue">پزیشکیمان</span>'),
                       t("تعرّف على أطبائنا واختر الطبيب المناسب لعلاجك.", "Meet our doctors and choose the right one for your treatment.", "پزیشکەکانمان بناسە و پزیشکی گونجاو بۆ چارەسەرەکەت هەڵبژێرە.")) + f'''
<section class="pb-12"><div class="max-w-6xl mx-auto px-4 md:px-6 space-y-8">{cards}</div></section>'''
    page("doctors.html",
         {"ar": "أطباؤنا | عيادة سوبر دينتست", "en": "Our Doctors | Super Dentist Clinic", "ku": "پزیشکەکانمان | کلینیکی سوپەر دێنتست"},
         "تعرّف على أطباء عيادة سوبر دينتست في أربيل: تقويم الأسنان، تجميل الأسنان وطب الأسنان العام.",
         body, active="doctors.html")


# ====================================================================== GALLERY
def build_gallery():
    cats = [("all", ("الكل", "All", "هەموو")),
            ("hollywood", ("ابتسامة هوليود", "Hollywood Smile", "خەندەی هۆلیوود")),
            ("implants", ("زراعة الأسنان", "Implants", "چاندنی ددان")),
            ("cosmetic", ("تجميل الأسنان", "Cosmetic", "جوانکاری")),
            ("orthodontics", ("التقويم", "Orthodontics", "ڕاستکردنەوە")),
            ("whitening", ("التبييض", "Whitening", "سپیکردنەوە"))]
    btns = "".join(f'<button type="button" data-cat="{c}" class="filter-btn px-5 py-2 rounded-full font-bold text-navyBlue bg-white border border-navyBlue/15 hover:bg-sky-50 transition-colors">{t(*l)}</button>' for c, l in cats)
    script = '''
<script>
/* =====================  BEFORE / AFTER CASES  =====================
   1. Put the photos in a folder called "gallery" next to this page.
   2. Add one line per case below.  cat = hollywood | implants | cosmetic | orthodontics | whitening
   3. Before and after photos should be taken from the same angle and cropped to the same size (4:3 works best).
   IMPORTANT: only use photos the patient has agreed in writing to publish.
   The 5 lines below are examples: they show grey boxes until the real photos exist.
   Replace them with real cases (or delete them). */
window.CASES = [
  { cat: 'hollywood',    before: 'gallery/hollywood-1-before.jpg',    after: 'gallery/hollywood-1-after.jpg',
    caption: { ar: 'ابتسامة هوليود - فينير', en: 'Hollywood Smile - veneers', ku: 'خەندەی هۆلیوود - ڤینیر' } },
  { cat: 'orthodontics', before: 'gallery/ortho-1-before.jpg',        after: 'gallery/ortho-1-after.jpg',
    caption: { ar: 'تقويم الأسنان', en: 'Orthodontic treatment', ku: 'ڕاستکردنەوەی ددان' } },
  { cat: 'whitening',    before: 'gallery/whitening-1-before.jpg',    after: 'gallery/whitening-1-after.jpg',
    caption: { ar: 'تبييض بالليزر', en: 'Laser whitening', ku: 'سپیکردنەوە بە لێزەر' } },
  { cat: 'implants',     before: 'gallery/implants-1-before.jpg',     after: 'gallery/implants-1-after.jpg',
    caption: { ar: 'زراعة الأسنان', en: 'Dental implants', ku: 'چاندنی ددان' } },
  { cat: 'cosmetic',     before: 'gallery/cosmetic-1-before.jpg',     after: 'gallery/cosmetic-1-after.jpg',
    caption: { ar: 'تجميل الأسنان', en: 'Cosmetic bonding', ku: 'جوانکاری ددان' } }
];
</script>'''
    body = page_header(t('نتائج <span class="text-deepBlue">قبل وبعد</span>', 'Before <span class="text-deepBlue">&amp; After</span>', 'ئەنجامی <span class="text-deepBlue">پێش و دوای</span>'),
                       t("اسحب الخط لترى الفرق. جميع الصور لمرضى حقيقيين وبموافقتهم.", "Drag the line to see the difference. All photos are of real patients, shared with their permission.", "هێڵەکە ڕابکێشە بۆ بینینی جیاوازی. هەموو وێنەکان هی نەخۆشی ڕاستەقینەن و بە ڕەزامەندی خۆیان.")) + f'''
<section class="pb-12">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <div id="gallery-filters" class="flex flex-wrap justify-center gap-2 mb-8">{btns}</div>
    <div id="gallery-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    <div id="gallery-empty" class="hidden card rounded-[20px] max-w-xl mx-auto text-center p-8 space-y-2"><i class="fa-regular fa-images text-3xl text-cyan-600" aria-hidden="true"></i><p class="font-semibold text-navyBlue text-lg">{t("نضيف صور الحالات قريباً.", "Patient results are being added soon.", "بەم زووانە وێنەی حاڵەتەکان زیاد دەکەین.")}</p><p class="text-slate-500">{t("اطلب رؤية نتائج حالات مشابهة لحالتك عبر واتساب.", "Ask us on WhatsApp to see results for cases like yours.", "لە واتسئاپ داوای بینینی ئەنجامی حاڵەتی هاوشێوە بکە.")}</p></div>
    <div class="text-center mt-10">
      {wa_btn("مرحباً، رأيت نتائج قبل وبعد وأود حجز استشارة", "Hello, I saw your before & after results and I'd like to book a consultation", "سڵاو، ئەنجامی پێش و دوایم بینی و دەمەوێت نۆرەی ڕاوێژ بگرم", t("احجز استشارتك", "Book your consultation", "نۆرەی ڕاوێژ بگرە"))}
    </div>
  </div>
</section>'''
    page("gallery.html",
         {"ar": "قبل وبعد | عيادة سوبر دينتست", "en": "Before & After | Super Dentist Clinic", "ku": "پێش و دوای | کلینیکی سوپەر دێنتست"},
         "صور قبل وبعد لمرضى عيادة سوبر دينتست في أربيل: ابتسامة هوليود، تقويم، زراعة وتبييض الأسنان.",
         body, active="gallery.html", scripts=script)


# ====================================================================== TOUR
def build_tour():
    script = '''
<script>
/* =====================  CLINIC TOUR PHOTOS  =====================
   Put the photos in a folder called "tour" next to this page and edit the list.
   Add, remove or rename rooms freely (e.g. a kids' corner, if the clinic has one). */
window.TOUR = [
  { src: 'tour/reception.jpg',     caption: { ar: 'الاستقبال',        en: 'Reception',          ku: 'پێشوازی' } },
  { src: 'tour/waiting-area.jpg',  caption: { ar: 'صالة الانتظار',    en: 'Waiting area',       ku: 'هۆڵی چاوەڕوانی' } },
  { src: 'tour/treatment-room.jpg',caption: { ar: 'غرفة العلاج',      en: 'Treatment room',     ku: 'ژووری چارەسەر' } },
  { src: 'tour/sterilization.jpg', caption: { ar: 'غرفة التعقيم',     en: 'Sterilization room', ku: 'ژووری پاککردنەوە و بێگەردکردن' } },
  { src: 'tour/xray.jpg',          caption: { ar: 'الأشعة الرقمية',   en: 'Digital X-ray',      ku: 'تیشکی دیجیتاڵ' } },
  { src: 'tour/equipment.jpg',     caption: { ar: 'أحدث التجهيزات',   en: 'Modern equipment',   ku: 'نوێترین ئامێرەکان' } }
];
</script>'''
    body = page_header(t('جولة في <span class="text-deepBlue">العيادة</span>', 'Clinic <span class="text-deepBlue">Tour</span>', 'گەشتێک بە <span class="text-deepBlue">کلینیکدا</span>'),
                       t("بيئة نظيفة ومريحة وتجهيزات حديثة. تعرّف على عيادتنا قبل زيارتك.", "A clean, comfortable space with modern equipment. Take a look before your visit.", "شوێنێکی پاک و ئاسوودە و ئامێری مۆدێرن. پێش سەردانەکەت سەیرێکی بکە.")) + f'''
<section class="pb-12">
  <div class="max-w-7xl mx-auto px-4 md:px-6 space-y-10">
    <!-- OPTIONAL tour video: put clinic-tour.mp4 next to this page and remove the comment markers.
    <div class="card rounded-[2rem] overflow-hidden">
      <video controls playsinline preload="metadata" poster="tour/reception.jpg" class="w-full">
        <source src="clinic-tour.mp4" type="video/mp4">
      </video>
    </div>
    -->
    <div id="tour-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    <div id="tour-empty" class="hidden card rounded-[20px] max-w-xl mx-auto text-center p-8 space-y-2"><i class="fa-regular fa-images text-3xl text-cyan-600" aria-hidden="true"></i><p class="font-semibold text-navyBlue text-lg">{t("صور العيادة قريباً.", "Clinic photos coming soon.", "بەم زووانە وێنەی کلینیک.")}</p><p class="text-slate-500">{t("شاهد الفيديو في الصفحة الرئيسية أو زرنا مباشرة.", "Watch the video on our homepage, or come and visit.", "ڤیدیۆکە لە پەڕەی سەرەکی ببینە یان سەردانمان بکە.")}</p></div>
    <div class="card rounded-[2rem] p-6 md:p-10 grid md:grid-cols-[auto_1fr] gap-6 items-center">
      <i class="fa-solid fa-shield-virus text-5xl text-deepBlue" aria-hidden="true"></i>
      <div>
        <h2 class="t-h3 font-semibold text-navyBlue mb-2">{t("سلامتك أولاً", "Your safety comes first", "سەلامەتی تۆ لە پێشەوەیە")}</h2>
        <!-- TODO: ask the clinic to confirm this text matches their sterilization routine -->
        <p class="font-normal text-slate-700 leading-relaxed">{t("نعقّم جميع الأدوات بعد كل مريض ونستخدم المواد ذات الاستخدام الواحد حيثما أمكن.", "All instruments are sterilized after every patient, and we use single-use materials wherever possible.", "هەموو ئامرازەکان دوای هەر نەخۆشێک بێگەرد دەکرێن و لە هەر شوێنێک بکرێت کەرەستەی یەکجار بەکارهاتوو بەکاردەهێنین.")}</p>
      </div>
    </div>
    <div class="text-center">
      {wa_btn("مرحباً، أود زيارة العيادة وحجز موعد", "Hello, I'd like to visit the clinic and book an appointment", "سڵاو، دەمەوێت سەردانی کلینیک بکەم و نۆرە بگرم", t("احجز زيارتك", "Book your visit", "سەردانەکەت تۆمار بکە"))}
    </div>
  </div>
</section>
<div id="lightbox" class="hidden fixed inset-0 z-[60] bg-black/85 items-center justify-center p-4 cursor-zoom-out">
  <img id="lightbox-img" src="" alt="" class="max-w-full max-h-full rounded-2xl">
</div>'''
    page("tour.html",
         {"ar": "جولة في العيادة | عيادة سوبر دينتست", "en": "Clinic Tour | Super Dentist Clinic", "ku": "گەشتی کلینیک | کلینیکی سوپەر دێنتست"},
         "جولة مصورة داخل عيادة سوبر دينتست في أربيل: الاستقبال، غرف العلاج، التعقيم والتجهيزات الحديثة.",
         body, active="tour.html", scripts=script)


if __name__ == "__main__":
    build_home(); build_services(); build_doctors(); build_gallery(); build_tour()
    print("\n".join(sorted(f for f in os.listdir(OUT) if f.endswith(".html"))))
