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
        f'<a href="{h}" class="whitespace-nowrap hover:text-deepBlue transition-colors subtext-glow{" text-deepBlue" if h == active else ""}">{t(*l)}</a>'
        for h, l in NAV)
    mob = "\n".join(
        f'<a href="{h}" class="py-2 border-b border-navyBlue/10 hover:text-deepBlue">{t(*l)}</a>' for h, l in NAV)
    return f'''
<nav class="fixed w-full z-50 glass-panel bg-white/60 border-b-0">
  <div class="max-w-7xl mx-auto px-4 md:px-6 py-3 flex justify-between items-center relative gap-4">
    <a href="index.html" class="flex items-center gap-3 shrink-0">
      <img src="super-dentist-logo.jpg" alt="Super Dentist Clinic logo" width="48" height="48" class="w-10 h-10 md:w-12 md:h-12 rounded-xl object-cover shadow-glass bg-white">
      <span class="text-lg md:text-xl font-extrabold text-navyBlue tracking-tight leading-none text-glow">{t("عيادة سوبر دينتست", "Super Dentist", "کلینیکی سوپەر دێنتست")}</span>
    </a>
    <div class="hidden xl:flex items-center gap-5 font-bold text-navyBlue text-[15px]">{desk}</div>
    <div class="flex items-center gap-3 shrink-0">
      <div class="flex bg-white/60 rounded-full p-1 border border-white/60 shadow-sm" role="group" aria-label="Language">
        <button type="button" onclick="changeLang('ar')" id="btn-ar" class="px-2 md:px-3 py-1 text-xs font-bold rounded-full transition-colors">AR</button>
        <button type="button" onclick="changeLang('en')" id="btn-en" class="px-2 md:px-3 py-1 text-xs font-bold rounded-full transition-colors">EN</button>
        <button type="button" onclick="changeLang('ku')" id="btn-ku" class="px-2 md:px-3 py-1 text-xs font-bold rounded-full transition-colors">KU</button>
      </div>
      <button type="button" id="mobile-menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" class="xl:hidden p-2 text-navyBlue">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
      <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link hidden xl:inline-flex items-center gap-2 px-5 py-2.5 text-sm font-bold text-white bg-whatsapp rounded-full hover:bg-whatsappDark transition-all shadow-lg hover:shadow-glow">
        <i class="fa-brands fa-whatsapp text-lg" aria-hidden="true"></i>{t("احجز عبر واتساب", "Book via WhatsApp", "نۆرە بگرە لە واتسئاپ")}
      </a>
    </div>
  </div>
  <div id="mobile-menu" class="hidden xl:hidden absolute top-full left-0 w-full shadow-lg py-4 px-6 flex flex-col gap-2 text-center font-bold text-navyBlue rounded-b-2xl bg-white/95">
    {mob}
    <div class="flex justify-center gap-6 mt-2">
      <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link py-2 text-whatsapp flex items-center gap-2"><i class="fa-brands fa-whatsapp text-2xl" aria-hidden="true"></i>{t("واتساب", "WhatsApp", "واتسئاپ")}</a>
      <a href="tel:+{WA1}" dir="ltr" class="py-2 text-deepBlue flex items-center gap-2"><i class="fa-solid fa-phone text-xl" aria-hidden="true"></i>{t("اتصل", "Call", "پەیوەندی")}</a>
    </div>
  </div>
</nav>'''


FOOTER = f'''
<footer id="contact" class="relative z-10 mt-8 md:mt-12 border-t border-white/60 bg-white/85 backdrop-blur-md">
  <div class="max-w-7xl mx-auto px-4 md:px-6 py-10 md:py-12 text-center space-y-8">
    <h2 class="text-2xl md:text-3xl font-extrabold text-navyBlue">{t("عيادة سوبر دينتست", "Super Dentist Clinic", "کلینیکی سوپەر دێنتست")}</h2>
    <div class="flex flex-col md:flex-row justify-center items-center md:items-start gap-8 md:gap-16 text-base md:text-lg font-bold text-navyBlue/90">
      <div class="flex flex-col items-center gap-2">
        <i class="fa-solid fa-location-dot text-deepBlue text-3xl mb-2" aria-hidden="true"></i>
        <span>{t("أربيل - شارع 120م - لالاف سيتي فيو", "Erbil - 120m Street - Lalav City View", "هەولێر - شەقامی 120م - لالاف ستی ڤیو")}</span>
        <a href="https://www.google.com/maps/dir/?api=1&destination=Super+Dentist+Clinic+Erbil" target="_blank" rel="noopener" class="text-sm text-deepBlue underline">{t("الاتجاهات", "Get directions", "ڕێنمایی ڕێگا")}</a>
      </div>
      <!-- TODO opening hours: fill in, then remove the comment markers
      <div class="flex flex-col items-center gap-2">
        <i class="fa-regular fa-clock text-deepBlue text-3xl mb-2" aria-hidden="true"></i>
        <span>{t("السبت - الخميس: ...", "Sat - Thu: ...", "شەممە - پێنجشەممە: ...")}</span>
      </div>
      -->
      <div class="flex flex-col items-center gap-3">
        <i class="fa-solid fa-phone text-deepBlue text-3xl mb-2" aria-hidden="true"></i>
        <div class="flex items-center gap-3" dir="ltr">
          <a href="tel:+{WA1}" class="tracking-wide text-xl hover:text-deepBlue">+964 750 722 7500</a>
          <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" aria-label="WhatsApp" class="wa-link"><i class="fa-brands fa-whatsapp text-whatsapp text-2xl" aria-hidden="true"></i></a>
        </div>
        <div class="flex items-center gap-3" dir="ltr">
          <a href="tel:+{WA2}" class="tracking-wide text-xl hover:text-deepBlue">+964 776 121 2111</a>
          <a href="https://wa.me/{WA2}" target="_blank" rel="noopener" aria-label="WhatsApp" class="wa-link"><i class="fa-brands fa-whatsapp text-whatsapp text-2xl" aria-hidden="true"></i></a>
        </div>
      </div>
    </div>
    <p class="pt-6 text-xs md:text-sm text-navyBlue/70 font-semibold border-t border-navyBlue/10 max-w-2xl mx-auto leading-relaxed">
      &copy; <span id="year" dir="ltr">2026</span>
      {t('جميع الحقوق محفوظة لشركة وي سكيور We Secure للتصميم والاعلان وتكنولوجيا المعلومات | <span dir="ltr">07703060331</span>',
         'All rights reserved to We Secure for Design, Advertising &amp; IT | <span dir="ltr">07703060331</span>',
         'هەموو مافێک پارێزراوە بۆ کۆمپانیای We Secure بۆ دیزاین و ڕیکلام و تەکنەلۆجیای زانیاری | <span dir="ltr">07703060331</span>')}
    </p>
  </div>
</footer>'''


def page(filename, titles, desc, body, active="", video=False, head_extra="", scripts=""):
    if video:
        bg = '''
<div class="fixed inset-0 w-full h-full z-[0] pointer-events-none bg-slate-100">
  <!-- poster = still image shown while the video loads. Export one frame of the video as clinic-bg-poster.jpg -->
  <video id="bg-video" autoplay loop muted playsinline preload="metadata" poster="clinic-bg-poster.jpg" class="bg-video w-full h-full object-cover">
    <source src="clinic-doctors-bg.mp4" type="video/mp4">
  </video>
  <div class="absolute inset-0 bg-white/30"></div>
</div>'''
        body_cls = "bg-transparent"
    else:
        bg = ""
        body_cls = "bg-gradient-to-b from-sky-50 via-white to-sky-50"
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl" data-title-ar="{titles['ar']}" data-title-en="{titles['en']}" data-title-ku="{titles['ku']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titles['ar']}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1a365d">
<link rel="icon" href="super-dentist-logo.jpg">
<meta property="og:type" content="website">
<meta property="og:title" content="{titles['ar']}">
<meta property="og:description" content="{desc}">
<!-- TODO: og:image needs a full URL once you have a domain, e.g. https://YOUR-DOMAIN/super-dentist-logo.jpg -->
<meta property="og:image" content="super-dentist-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+Arabic:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<!-- Pre-built Tailwind CSS. If you add new Tailwind classes, styles.css must be rebuilt. -->
<link rel="stylesheet" href="styles.css">
{head_extra}
</head>
<body class="antialiased relative selection:bg-navyBlue selection:text-white font-sans {body_cls}">
{bg}
{nav(active)}
<main>
{body}
</main>
{FOOTER}
{scripts}
<script src="site.js"></script>
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
            f'class="wa-link inline-flex items-center justify-center gap-2 {cls} font-bold text-white bg-whatsapp rounded-full hover:bg-whatsappDark transition-all shadow-lg hover:shadow-glow">'
            f'<i class="fa-brands fa-whatsapp text-xl" aria-hidden="true"></i>{label}</a>')


def page_header(title_html, sub_html=""):
    return f'''
<section class="pt-32 pb-8 md:pt-36 md:pb-10">
  <div class="max-w-5xl mx-auto px-4 md:px-6 text-center space-y-4">
    <h1 class="text-3xl md:text-5xl font-extrabold text-navyBlue">{title_html}</h1>
    {f'<p class="text-lg md:text-xl text-navyBlue/80 font-semibold max-w-3xl mx-auto leading-relaxed">{sub_html}</p>' if sub_html else ''}
  </div>
</section>'''


SVC = {s["slug"]: s for s in SERVICES}

# ====================================================================== HOME
def build_home():
    doctors = ""
    for d in DOCTORS:
        doctors += f'''
<a href="doctors.html#{d["id"]}" class="specialist-card relative rounded-[1.5rem] md:rounded-[2rem] overflow-hidden glass-panel group/item flex flex-col justify-end p-6 md:p-8">
  <div class="absolute inset-0 bg-gradient-to-t from-white/95 via-white/40 to-transparent z-0"></div>
  <img src="{d["photo"]}" loading="lazy" class="absolute top-0 left-0 w-full h-full object-cover object-top z-[-1]" alt="{d["name"]["en"]}">
  <div class="relative z-10 transform md:translate-y-10 md:group-hover/item:translate-y-0 transition-transform duration-500 bg-white/85 p-3 md:p-4 rounded-xl md:rounded-2xl">
    <h3 class="text-xl md:text-2xl font-black text-navyBlue mb-1">{tt(d["name"])}</h3>
    <p class="text-deepBlue font-bold text-sm md:text-lg">{tt(d["role"])}</p>
    <span class="text-sm font-bold text-navyBlue/70">{t("الملف الشخصي ←", "View profile →", "پرۆفایل ←")}</span>
  </div>
</a>'''

    services = ""
    for i, s in enumerate(SERVICES):
        span = " lg:col-span-2" if i == len(SERVICES) - 1 else ""
        services += f'''
<a href="{s["slug"]}.html" class="glass-panel p-5 md:p-6 rounded-2xl md:rounded-3xl hover:-translate-y-2 transition-transform duration-300 flex flex-col justify-center items-center text-center gap-2 bg-white/70 hover:bg-white/90{span}">
  <h3 class="text-lg md:text-xl font-black text-navyBlue">{tt(s["title"])}</h3>
  <span class="text-sm font-bold text-deepBlue">{t("اعرف المزيد", "Learn more", "زیاتر بزانە")}</span>
</a>'''

    jsonld = {
        "@context": "https://schema.org", "@type": "Dentist",
        "name": "Super Dentist Clinic", "alternateName": "عيادة سوبر دينتست",
        "image": "super-dentist-logo.jpg",
        "telephone": ["+" + WA1, "+" + WA2],
        "address": {"@type": "PostalAddress", "streetAddress": "120m Street, Lalav City View",
                    "addressLocality": "Erbil", "addressCountry": "IQ"},
        "medicalSpecialty": ["Orthodontic", "CosmeticDentistry"],
        "availableLanguage": ["ar", "en", "ku"],
    }
    head = ('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n'
            '<!-- TODO: add "openingHours": ["Sa-Th 10:00-21:00"] (real hours) to the JSON above -->')

    reviews_script = '''
<script>
/* =====================  REAL GOOGLE REVIEWS  =====================
   Copy reviews WORD FOR WORD from the clinic's Google page and add them here.
   Use the reviewer's first name + initial, the star count, and the month.
   lang = the language the review was written in ('ar', 'en' or 'ku').
   Example:
     { name: 'Ahmed K.', stars: 5, lang: 'ar', date: '2026-10', text: 'نص المراجعة كما هو في جوجل' },
   While this list is empty, the section just shows the Google rating + buttons. */
window.REVIEWS = [

];
</script>'''

    body = f'''
<section id="home" class="relative min-h-screen flex items-center overflow-hidden">
  <div class="max-w-7xl mx-auto px-4 md:px-6 w-full relative z-10 pt-24">
    <div class="space-y-4 md:space-y-6 max-w-2xl bg-white/30 p-6 md:p-8 rounded-3xl backdrop-blur-md border border-white/40 shadow-glass">
      <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-navyBlue leading-[1.2] text-glow">
        {t("ابتسامتك،", "Your Smile,", "خەندەکەت،", block=True)}
        <span class="text-deepBlue">{t("شغفنا.", "Our Passion.", "خولیای ئێمەیە.")}</span>
      </h1>
      <p class="text-lg md:text-xl text-navyBlue font-bold subtext-glow leading-relaxed">{t("نجمع بين أمهر الأطباء وأحدث التقنيات لنمنحك الرعاية التي تستحقها.", "Combining top specialists and the latest technology to give you the care you deserve.", "باشترین پزیشکەکان و نوێترین تەکنەلۆژیا کۆدەکەینەوە بۆ پێدانی ئەو چاودێرییەی شایستەیت.")}</p>
      <div class="pt-4 flex flex-wrap gap-3">
        <a href="https://wa.me/{WA1}" target="_blank" rel="noopener" dir="ltr" class="wa-link inline-flex items-center gap-2 px-8 py-3 font-bold text-white bg-whatsapp rounded-full hover:bg-whatsappDark shadow-lg hover:shadow-glow"><i class="fa-brands fa-whatsapp text-xl" aria-hidden="true"></i>{t("احجز موعدك", "Book an Appointment", "نۆرە بگرە")}</a>
        <a href="tel:+{WA1}" dir="ltr" class="inline-flex items-center gap-2 px-8 py-3 font-bold text-navyBlue bg-white/80 rounded-full hover:bg-white shadow-lg"><i class="fa-solid fa-phone" aria-hidden="true"></i>{t("اتصل بنا", "Call Us", "پەیوەندیمان پێوە بکە")}</a>
      </div>
    </div>
  </div>
</section>

<!-- Stats. TODO: confirm these numbers with the clinic -->
<section id="stats" class="py-8 md:py-12 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 text-center">
    <div class="glass-panel p-4 md:p-6 rounded-[1.5rem] md:rounded-[2rem] flex flex-col items-center bg-white/60"><span class="text-3xl md:text-5xl font-black text-deepBlue" dir="ltr">5000<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("علاج ناجح", "Successful Treatments", "چارەسەری سەرکەوتوو")}</span></div>
    <div class="glass-panel p-4 md:p-6 rounded-[1.5rem] md:rounded-[2rem] flex flex-col items-center bg-white/60"><span class="text-3xl md:text-5xl font-black text-deepBlue" dir="ltr">4782<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("مريض سعيد", "Happy Patients", "نەخۆشی دڵخۆش")}</span></div>
    <div class="glass-panel p-4 md:p-6 rounded-[1.5rem] md:rounded-[2rem] flex flex-col items-center bg-white/60"><span class="text-3xl md:text-5xl font-black text-deepBlue" dir="ltr">5.0 <span class="text-yellow-500 text-2xl md:text-3xl">★</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("تقييم جوجل", "Google Rating", "هەڵسەنگاندنی گوگڵ")}</span></div>
    <div class="glass-panel p-4 md:p-6 rounded-[1.5rem] md:rounded-[2rem] flex flex-col items-center bg-white/60"><span class="text-3xl md:text-5xl font-black text-deepBlue" dir="ltr">35<span class="text-xl md:text-2xl">+</span></span><span class="text-navyBlue font-bold text-sm md:text-lg mt-2">{t("سنوات الخبرة", "Years of Experience", "ساڵانی ئەزموون")}</span></div>
  </div>
</section>

<section id="specialists" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <h2 class="text-center mb-8 md:mb-12 text-3xl md:text-5xl font-extrabold text-navyBlue text-glow">{t('فريقنا <span class="text-deepBlue">الطبي</span>', 'Our Medical <span class="text-deepBlue">Team</span>', 'تیمی <span class="text-deepBlue">پزیشکیمان</span>')}</h2>
    <div class="flex flex-col md:flex-row h-auto md:h-[65vh] gap-4 specialists-container">{doctors}</div>
  </div>
</section>

<section id="services" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6">
    <h2 class="text-center mb-8 md:mb-12 text-3xl md:text-5xl font-extrabold text-navyBlue text-glow">{t('خدمات <span class="text-deepBlue">العيادة</span>', 'Clinic <span class="text-deepBlue">Services</span>', 'خزمەتگوزارییەکانی <span class="text-deepBlue">کلینیک</span>')}</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">{services}</div>
  </div>
</section>

<!-- Gallery + tour teasers -->
<section class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 grid md:grid-cols-2 gap-6">
    <a href="gallery.html" class="glass-panel bg-white/75 hover:bg-white/90 rounded-[2rem] p-8 md:p-10 flex flex-col gap-3">
      <i class="fa-solid fa-wand-magic-sparkles text-3xl text-deepBlue" aria-hidden="true"></i>
      <h2 class="text-2xl md:text-3xl font-extrabold text-navyBlue">{t("نتائج قبل وبعد", "Before &amp; After", "ئەنجامی پێش و دوای")}</h2>
      <p class="text-navyBlue/80 font-semibold">{t("شاهد نتائج حقيقية لمرضانا في ابتسامة هوليود والتقويم والتبييض.", "See real results from our patients: Hollywood Smile, orthodontics, whitening and more.", "ئەنجامی ڕاستەقینەی نەخۆشەکانمان ببینە لە خەندەی هۆلیوود، ڕاستکردنەوە و سپیکردنەوەدا.")}</p>
      <span class="font-bold text-deepBlue">{t("عرض المعرض ←", "View gallery →", "بینینی گەلەری ←")}</span>
    </a>
    <a href="tour.html" class="glass-panel bg-white/75 hover:bg-white/90 rounded-[2rem] p-8 md:p-10 flex flex-col gap-3">
      <i class="fa-solid fa-house-medical text-3xl text-deepBlue" aria-hidden="true"></i>
      <h2 class="text-2xl md:text-3xl font-extrabold text-navyBlue">{t("جولة في العيادة", "Clinic Tour", "گەشتێک بە کلینیکدا")}</h2>
      <p class="text-navyBlue/80 font-semibold">{t("تعرّف على عيادتنا وتجهيزاتها قبل زيارتك.", "Take a look inside our clinic and equipment before your visit.", "پێش سەردانەکەت کلینیک و ئامێرەکانمان ببینە.")}</p>
      <span class="font-bold text-deepBlue">{t("ابدأ الجولة ←", "Start the tour →", "دەستپێکردنی گەشت ←")}</span>
    </a>
  </div>
</section>

<section id="reviews" class="py-12 md:py-16 relative z-10">
  <div class="max-w-7xl mx-auto px-4 md:px-6 grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-12 items-start">
    <div class="space-y-6">
      <h2 class="text-3xl md:text-5xl font-extrabold text-navyBlue text-glow">{t('ماذا يقول <span class="text-deepBlue">مرضانا</span>', 'What Our <span class="text-deepBlue">Patients Say</span>', 'نەخۆشەکانمان <span class="text-deepBlue">چی دەڵێن</span>')}</h2>
      <a href="{MAPS}" target="_blank" rel="noopener" class="inline-flex items-center gap-4 glass-panel px-5 md:px-6 py-3 md:py-4 rounded-full bg-white/80 hover:bg-white">
        <i class="fa-brands fa-google text-2xl text-[#4285F4]" aria-hidden="true"></i>
        <div>
          <div class="text-yellow-500 text-lg" aria-hidden="true">★★★★★</div>
          <span class="text-navyBlue font-extrabold text-xs md:text-sm block">{t("تقييم 5.0 من أصل 131 مراجعة على جوجل", "5.0 rating from 131 Google reviews", "هەڵسەنگاندنی 5.0 لە 131 پێداچوونەوەی گوگڵ")}</span>
        </div>
      </a>
      <div id="reviews-list" class="hidden space-y-4 max-h-[450px] overflow-y-auto pe-1"></div>
      <div class="flex flex-wrap gap-3">
        <a href="{MAPS}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-6 py-3 font-bold text-white bg-navyBlue rounded-full hover:bg-deepBlue">{t("عرض جميع المراجعات", "See all reviews", "هەموو پێداچوونەوەکان ببینە")}</a>
        <!-- TODO: replace href with your "write a review" link:
             https://search.google.com/local/writereview?placeid=YOUR_PLACE_ID
             (find the Place ID at developers.google.com/maps/documentation/places/web-service/place-id) -->
        <a href="{MAPS}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-6 py-3 font-bold text-navyBlue bg-white/85 rounded-full hover:bg-white shadow"><i class="fa-solid fa-pen" aria-hidden="true"></i>{t("اكتب تقييمك", "Write a review", "هەڵسەنگاندن بنووسە")}</a>
      </div>
    </div>
    <div class="flex flex-col gap-3">
      <!-- TODO: replace src with the official embed (Google Maps → Share → Embed a map) -->
      <div class="h-[320px] md:h-[450px] glass-panel rounded-[2rem] overflow-hidden p-2 bg-white/40">
        <iframe src="https://maps.google.com/maps?q=Super+dentists+clinic+Erbil&t=&z=16&ie=UTF8&iwloc=&output=embed" title="Super Dentist Clinic location" width="100%" height="100%" style="border:0;border-radius:1.5rem" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
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
                mark = (f'<span class="shrink-0 w-8 h-8 rounded-full bg-deepBlue text-white flex items-center justify-center font-black text-sm">{i+1}</span>'
                        if numbered else '<i class="fa-solid fa-check text-deepBlue mt-1.5" aria-hidden="true"></i>')
                out += f'<li class="flex gap-3 items-start">{mark}<span class="font-semibold text-navyBlue/90 leading-relaxed">{t(items["ar"][i], items["en"][i], items["ku"][i])}</span></li>'
            return out

        gallery_link = ""
        if s["gallery"]:
            gallery_link = f'<a href="gallery.html#{s["gallery"]}" class="inline-flex items-center gap-2 px-8 py-3 font-bold text-navyBlue bg-white rounded-full hover:bg-sky-50 shadow"><i class="fa-solid fa-images" aria-hidden="true"></i>{t("شاهد نتائج قبل وبعد", "See before &amp; after results", "ئەنجامی پێش و دوای ببینە")}</a>'

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
        <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-4">{t("لمن هذا العلاج؟", "Who is it for?", "ئەم چارەسەرە بۆ کێیە؟")}</h2>
        <ul class="space-y-3">{li(s["who"])}</ul>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-4">{t("خطوات العلاج", "How it works", "هەنگاوەکانی چارەسەر")}</h2>
        <ol class="space-y-3">{li(s["steps"], numbered=True)}</ol>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-4">{t("كم يستغرق؟", "How long does it take?", "چەند دەخایەنێت؟")}</h2>
        <p class="flex gap-3 items-start font-semibold text-navyBlue/90"><i class="fa-regular fa-clock text-deepBlue mt-1" aria-hidden="true"></i>{tt(s["duration"])}</p>
      </div>
      <div class="card rounded-3xl p-6 md:p-8">
        <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-4">{t("بعد العلاج", "Aftercare", "دوای چارەسەر")}</h2>
        <ul class="space-y-3">{li(s["after"])}</ul>
      </div>
    </div>
    <!-- TODO (optional): add a price range, e.g. "Starting from ..." -->
    <p class="text-center text-sm text-navyBlue/70 font-semibold">{t("كل حالة مختلفة؛ يحدد الطبيب خطة العلاج المناسبة لك بعد الفحص.", "Every case is different. Your dentist will confirm the right plan for you after an examination.", "هەر حاڵەتێک جیاوازە؛ پزیشک دوای پشکنین پلانی گونجاوت بۆ دیاری دەکات.")}</p>
  </div>
</section>
<section class="py-10">
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-4 text-center">{t("خدمات أخرى", "Other services", "خزمەتگوزاری تر")}</h2>
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
        gal = (f'<a href="gallery.html#{d["gallery"]}" class="inline-flex items-center gap-2 px-6 py-3 font-bold text-navyBlue bg-white rounded-full border border-navyBlue/15 hover:bg-sky-50"><i class="fa-solid fa-images" aria-hidden="true"></i>{t("شاهد الحالات", "See cases", "حاڵەتەکان ببینە")}</a>'
               if d["gallery"] else "")
        n = d["name"]
        cards += f'''
<article id="{d["id"]}" class="card rounded-[2rem] overflow-hidden grid md:grid-cols-[320px_1fr]">
  <img src="{d["photo"]}" alt="{n["en"]}" loading="lazy" class="w-full h-80 md:h-full object-cover object-top">
  <div class="p-6 md:p-10 space-y-5">
    <div>
      <h2 class="text-2xl md:text-3xl font-black text-navyBlue">{tt(n)}</h2>
      <p class="text-deepBlue font-bold text-lg mt-1">{tt(d["role"])}</p>
    </div>
    <!-- TODO: fill in the doctor's real details, then remove the comment markers.
    <p class="text-navyBlue/85 font-semibold leading-relaxed">
      <span class="lang-text lang-ar">نبذة قصيرة عن الطبيب ...</span>
      <span class="lang-text lang-en">Short bio ...</span>
      <span class="lang-text lang-ku">کورتەیەک دەربارەی پزیشک ...</span>
    </p>
    <ul class="space-y-2 font-semibold text-navyBlue/90">
      <li><i class="fa-solid fa-graduation-cap text-deepBlue w-6" aria-hidden="true"></i> University / degree ...</li>
      <li><i class="fa-solid fa-briefcase-medical text-deepBlue w-6" aria-hidden="true"></i> Years of experience ...</li>
      <li><i class="fa-solid fa-language text-deepBlue w-6" aria-hidden="true"></i> Arabic, Kurdish, English ...</li>
    </ul>
    -->
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
    <div class="flex flex-wrap justify-center gap-2 mb-8">{btns}</div>
    <div id="gallery-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    <p id="gallery-empty" class="hidden text-center font-bold text-navyBlue/70 py-12">{t("سنضيف حالات قريباً.", "Cases coming soon.", "بەم زووانە حاڵەت زیاد دەکەین.")}</p>
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
    <div class="card rounded-[2rem] p-6 md:p-10 grid md:grid-cols-[auto_1fr] gap-6 items-center">
      <i class="fa-solid fa-shield-virus text-5xl text-deepBlue" aria-hidden="true"></i>
      <div>
        <h2 class="text-xl md:text-2xl font-extrabold text-navyBlue mb-2">{t("سلامتك أولاً", "Your safety comes first", "سەلامەتی تۆ لە پێشەوەیە")}</h2>
        <!-- TODO: ask the clinic to confirm this text matches their sterilization routine -->
        <p class="font-semibold text-navyBlue/85 leading-relaxed">{t("نعقّم جميع الأدوات بعد كل مريض ونستخدم المواد ذات الاستخدام الواحد حيثما أمكن.", "All instruments are sterilized after every patient, and we use single-use materials wherever possible.", "هەموو ئامرازەکان دوای هەر نەخۆشێک بێگەرد دەکرێن و لە هەر شوێنێک بکرێت کەرەستەی یەکجار بەکارهاتوو بەکاردەهێنین.")}</p>
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
