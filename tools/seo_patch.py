# SEO + speed patch for the generated site components (site/ipa-*.js).
# 27/10/2026. The original design source used by build_site.py is no longer available,
# so this edits the generated files in place. It is idempotent: running it twice changes nothing.
import re, json, pathlib

SITE_DIR = pathlib.Path(__file__).resolve().parent.parent / 'site'
SITE = 'https://www.ipanemabeautyandspa.com'
APP = 'https://app.ipanemabeautyandspa.com'

LABEL_STYLE = 'display: block; margin: 0 0 16px; font-size: 15px; line-height: 1.4; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: %s'

# page -> (old uppercase label, new keyword line that goes inside the H1)
KW = {
 'ipa-home':   ('Brows · Waxing · Hair · Dr. Phillips, Orlando', 'Eyebrows · Brazilian Wax · Hair · Dr. Phillips, Orlando'),
 'ipa-brows':  ('Brows &amp; Lashes Bar', 'Eyebrow Threading, Waxing &amp; Lash Lift · Orlando'),
 'ipa-waxing': ('Waxing', 'Brazilian Wax in Orlando · Dr. Phillips'),
 'ipa-hair':   ('Hair', 'Hair Salon in Dr. Phillips, Orlando'),
 'ipa-visit':  ('Visit &amp; contact', 'Ipanema Beauty &amp; Spa · Dr. Phillips, Orlando'),
}

T = {  # en -> pt, es, he, ar
 'Eyebrows · Brazilian Wax · Hair · Dr. Phillips, Orlando': ('Sobrancelhas · Depilação brasileira · Cabelo · Dr. Phillips, Orlando', 'Cejas · Depilación brasileña · Cabello · Dr. Phillips, Orlando', 'גבות · שעווה ברזילאית · שיער · Dr. Phillips, אורלנדו', 'الحواجب · الشمع البرازيلي · الشعر · دكتور فيليبس، أورلاندو'),
 'Eyebrow Threading, Waxing & Lash Lift · Orlando': ('Sobrancelha na linha, na cera e lifting de cílios · Orlando', 'Cejas con hilo, con cera y lifting de pestañas · Orlando', 'עיצוב גבות בחוט ובשעווה והרמת ריסים · אורלנדו', 'تشكيل الحواجب بالخيط والشمع ورفع الرموش · أورلاندو'),
 'Brazilian Wax in Orlando · Dr. Phillips': ('Depilação brasileira em Orlando · Dr. Phillips', 'Depilación brasileña en Orlando · Dr. Phillips', 'שעווה ברזילאית באורלנדו · Dr. Phillips', 'الشمع البرازيلي في أورلاندو · دكتور فيليبس'),
 'Hair Salon in Dr. Phillips, Orlando': ('Salão de cabelo em Dr. Phillips, Orlando', 'Salón de cabello en Dr. Phillips, Orlando', 'מספרה ב-Dr. Phillips, אורלנדו', 'صالون شعر في دكتور فيليبس، أورلاندو'),
 'Ipanema Beauty & Spa · Dr. Phillips, Orlando': ('Ipanema Beauty & Spa · Dr. Phillips, Orlando', 'Ipanema Beauty & Spa · Dr. Phillips, Orlando', 'Ipanema Beauty & Spa · Dr. Phillips, אורלנדו', 'Ipanema Beauty & Spa · دكتور فيليبس، أورلاندو'),
 'Questions.': ('Perguntas.', 'Preguntas.', 'שאלות.', 'أسئلة.'),
}

FAQ = {
 'ipa-brows': [
  ('How long does eyebrow threading last?', 'Usually 3 to 5 weeks, depending on how fast your hair grows. Most clients come back every 3 to 4 weeks to keep the shape clean.',
   ('Quanto tempo dura a sobrancelha feita na linha?', 'Normalmente de 3 a 5 semanas, dependendo de quão rápido o seu pelo cresce. A maioria das clientes volta a cada 3 a 4 semanas para manter o desenho.'),
   ('¿Cuánto dura el depilado de cejas con hilo?', 'Normalmente de 3 a 5 semanas, según lo rápido que crezca tu vello. La mayoría de las clientas vuelve cada 3 a 4 semanas para mantener la forma.'),
   ('כמה זמן מחזיק עיצוב גבות בחוט?', 'בדרך כלל 3 עד 5 שבועות, תלוי בקצב צמיחת השיער. רוב הלקוחות חוזרות כל 3 עד 4 שבועות כדי לשמור על הצורה.'),
   ('كم يدوم تشكيل الحواجب بالخيط؟', 'عادةً من 3 إلى 5 أسابيع، حسب سرعة نمو الشعر. معظم العميلات يعدن كل 3 إلى 4 أسابيع للحفاظ على الشكل.')),
  ('Does eyebrow threading hurt?', 'Most clients feel a quick pinch that fades in seconds. Only the thread touches your skin, with no wax or heat, so it is a gentle choice for sensitive skin.',
   ('Sobrancelha na linha dói?', 'A maioria das clientes sente só uma beliscadinha rápida que passa em segundos. Só a linha toca a pele, sem cera e sem calor, por isso é uma opção delicada para pele sensível.'),
   ('¿Duele el depilado de cejas con hilo?', 'La mayoría de las clientas siente solo un pellizco rápido que pasa en segundos. Solo el hilo toca la piel, sin cera ni calor, por eso es una opción suave para piel sensible.'),
   ('האם עיצוב גבות בחוט כואב?', 'רוב הלקוחות מרגישות צביטה קלה שחולפת תוך שניות. רק החוט נוגע בעור, בלי שעווה ובלי חום, ולכן זו בחירה עדינה לעור רגיש.'),
   ('هل تشكيل الحواجب بالخيط مؤلم؟', 'معظم العميلات يشعرن بوخزة سريعة تختفي خلال ثوانٍ. الخيط وحده يلمس البشرة، بدون شمع أو حرارة، لذلك هو خيار لطيف للبشرة الحساسة.')),
  ('How long does brow lamination last?', 'About 6 to 8 weeks. Keep your brows away from water, steam and makeup for the first 24 hours to help it last.',
   ('Quanto tempo dura a laminação de sobrancelhas?', 'Cerca de 6 a 8 semanas. Nas primeiras 24 horas, evite água, vapor e maquiagem nas sobrancelhas para durar mais.'),
   ('¿Cuánto dura la laminación de cejas?', 'Unas 6 a 8 semanas. Durante las primeras 24 horas, evita agua, vapor y maquillaje en las cejas para que dure más.'),
   ('כמה זמן מחזיקה למינציה לגבות?', 'בערך 6 עד 8 שבועות. ב-24 השעות הראשונות כדאי להרחיק מהגבות מים, אדים ואיפור כדי שהתוצאה תחזיק.'),
   ('كم تدوم تقنية لامينيشن الحواجب؟', 'حوالي 6 إلى 8 أسابيع. أبعدي الماء والبخار والمكياج عن الحواجب خلال أول 24 ساعة لتدوم أطول.')),
 ],
 'ipa-waxing': [
  ('How long does a Brazilian wax last?', 'Usually 3 to 4 weeks. With regular visits every 4 weeks, hair tends to grow back finer and slower.',
   ('Quanto tempo dura a depilação brasileira?', 'Normalmente de 3 a 4 semanas. Com visitas regulares a cada 4 semanas, o pelo tende a voltar mais fino e mais devagar.'),
   ('¿Cuánto dura la depilación brasileña?', 'Normalmente de 3 a 4 semanas. Con visitas regulares cada 4 semanas, el vello suele volver más fino y más lento.'),
   ('כמה זמן מחזיקה שעווה ברזילאית?', 'בדרך כלל 3 עד 4 שבועות. עם ביקורים קבועים כל 4 שבועות, השיער נוטה לצמוח דק יותר ולאט יותר.'),
   ('كم يدوم الشمع البرازيلي؟', 'عادةً من 3 إلى 4 أسابيع. مع الزيارات المنتظمة كل 4 أسابيع، يميل الشعر إلى النمو بشكل أنعم وأبطأ.')),
  ('Should I shave before my Brazilian wax?', 'No. Stop shaving and let the hair grow to about ¼ inch, roughly 2 to 3 weeks, so the wax can grip it from the root.',
   ('Devo raspar antes da depilação brasileira?', 'Não. Pare de raspar e deixe o pelo crescer cerca de 0,5 cm, mais ou menos 2 a 3 semanas, para a cera conseguir puxar desde a raiz.'),
   ('¿Debo rasurarme antes de la depilación brasileña?', 'No. Deja de rasurarte y deja crecer el vello unos 0,5 cm, más o menos 2 a 3 semanas, para que la cera lo tome desde la raíz.'),
   ('האם לגלח לפני שעווה ברזילאית?', 'לא. הפסיקי לגלח ותני לשיער לצמוח לכחצי סנטימטר, בערך 2 עד 3 שבועות, כדי שהשעווה תתפוס אותו מהשורש.'),
   ('هل يجب الحلاقة قبل الشمع البرازيلي؟', 'لا. توقفي عن الحلاقة واتركي الشعر ينمو حوالي نصف سنتيمتر، أي من أسبوعين إلى 3 أسابيع تقريباً، ليتمكن الشمع من إزالته من الجذور.')),
  ('How soon can I shower or swim after a Brazilian wax?', 'You can shower the same day with lukewarm water. Wait 24 to 48 hours before pools, the beach, hot tubs, saunas or tanning.',
   ('Quando posso tomar banho ou nadar depois da depilação brasileira?', 'Você pode tomar banho no mesmo dia, com água morna. Espere de 24 a 48 horas para piscina, praia, banheira quente, sauna ou bronzeamento.'),
   ('¿Cuándo puedo ducharme o nadar después de la depilación brasileña?', 'Puedes ducharte el mismo día con agua tibia. Espera de 24 a 48 horas para piscina, playa, jacuzzi, sauna o bronceado.'),
   ('מתי אפשר להתקלח או לשחות אחרי שעווה ברזילאית?', 'אפשר להתקלח באותו יום במים פושרים. כדאי לחכות 24 עד 48 שעות לפני בריכה, ים, ג׳קוזי, סאונה או שיזוף.'),
   ('متى يمكنني الاستحمام أو السباحة بعد الشمع البرازيلي؟', 'يمكنك الاستحمام في اليوم نفسه بماء فاتر. انتظري من 24 إلى 48 ساعة قبل المسبح أو البحر أو الجاكوزي أو الساونا أو التسمير.')),
 ],
 'ipa-home': [
  ('Do you offer facials in Orlando?', 'Yes. Our deep-cleansing facial is done in a private room by our estheticians, in Dr. Phillips. You can book it online in under a minute.',
   ('Vocês fazem limpeza de pele em Orlando?', 'Sim. A nossa limpeza de pele profunda é feita em sala privativa pelas nossas esteticistas, em Dr. Phillips. Você agenda online em menos de um minuto.'),
   ('¿Hacen limpiezas faciales en Orlando?', 'Sí. Nuestra limpieza facial profunda se hace en una sala privada con nuestras esteticistas, en Dr. Phillips. Puedes reservarla en línea en menos de un minuto.'),
   ('האם אתם עושים טיפולי פנים באורלנדו?', 'כן. טיפול הניקוי העמוק לפנים נעשה בחדר פרטי על ידי הקוסמטיקאיות שלנו, ב-Dr. Phillips. אפשר לקבוע תור אונליין בפחות מדקה.'),
   ('هل تقدمون جلسات تنظيف البشرة في أورلاندو؟', 'نعم. جلسة التنظيف العميق للبشرة تتم في غرفة خاصة على يد خبيرات التجميل لدينا في دكتور فيليبس. يمكنك الحجز عبر الإنترنت في أقل من دقيقة.')),
  ('How often should I get a facial?', 'About every 4 weeks, which follows your skin’s natural renewal cycle. Your esthetician will suggest the best rhythm for your skin.',
   ('Com que frequência devo fazer limpeza de pele?', 'Mais ou menos a cada 4 semanas, que acompanha o ciclo natural de renovação da pele. A sua esteticista indica o melhor ritmo para a sua pele.'),
   ('¿Cada cuánto debo hacerme una limpieza facial?', 'Más o menos cada 4 semanas, que sigue el ciclo natural de renovación de la piel. Tu esteticista te dirá el mejor ritmo para tu piel.'),
   ('כל כמה זמן כדאי לעשות טיפול פנים?', 'בערך כל 4 שבועות, בהתאם למחזור ההתחדשות הטבעי של העור. הקוסמטיקאית תמליץ על הקצב המתאים לעור שלך.'),
   ('كم مرة يجب أن أنظف بشرتي؟', 'تقريباً كل 4 أسابيع، بما يتوافق مع دورة تجدد البشرة الطبيعية. ستقترح عليك خبيرة التجميل الإيقاع الأنسب لبشرتك.')),
  ('Do you do eyebrow threading?', 'Yes. Our artists shape brows with thread, wax or tweezers, whichever suits your skin and hair best.',
   ('Vocês fazem sobrancelha na linha?', 'Sim. As nossas profissionais desenham a sobrancelha com linha, cera ou pinça, o que for melhor para a sua pele e o seu pelo.'),
   ('¿Hacen cejas con hilo?', 'Sí. Nuestras artistas diseñan las cejas con hilo, cera o pinza, lo que mejor se adapte a tu piel y tu vello.'),
   ('האם אתם עושים עיצוב גבות בחוט?', 'כן. האמניות שלנו מעצבות גבות בחוט, בשעווה או בפינצטה, לפי מה שמתאים לעור ולשיער שלך.'),
   ('هل تقدمون تشكيل الحواجب بالخيط؟', 'نعم. فناناتنا يشكّلن الحواجب بالخيط أو الشمع أو الملقط، حسب ما يناسب بشرتك وشعرك.')),
  ('Where are you located?', '6735 Conroy Rd, Suite 114, Orlando, FL 32835, in Dr. Phillips, a few minutes from Windermere, Bay Hill and MetroWest.',
   ('Onde vocês ficam?', '6735 Conroy Rd, Suite 114, Orlando, FL 32835, em Dr. Phillips, a poucos minutos de Windermere, Bay Hill e MetroWest.'),
   ('¿Dónde están ubicados?', '6735 Conroy Rd, Suite 114, Orlando, FL 32835, en Dr. Phillips, a pocos minutos de Windermere, Bay Hill y MetroWest.'),
   ('איפה אתם נמצאים?', '6735 Conroy Rd, Suite 114, Orlando, FL 32835, ב-Dr. Phillips, כמה דקות מ-Windermere, Bay Hill ו-MetroWest.'),
   ('أين يقع الصالون؟', '6735 Conroy Rd, Suite 114, Orlando, FL 32835، في دكتور فيليبس، على بُعد دقائق من Windermere وBay Hill وMetroWest.')),
 ],
}

# Microblading = $425 in 2 sessions of $212.50 (Ozeias 27/10/2026)
MB = {
 'ipa-brows': [('>Natural-looking hair strokes for fuller brows.</p>', '>Natural-looking hair strokes for fuller brows. Done in 2 sessions, $425 in total.</p>')],
 'ipa-home': [('>Natural hair strokes. $63.75 deposit to book.</p>', '>Natural hair strokes in 2 sessions ($425 total). $63.75 deposit to book.</p>'),
              ('color: #1f1f1f">$212.50</p>', 'color: #1f1f1f">$212.50 <span style="font-size: 16px; font-weight: 500; color: #4f4a3a">per session</span></p>')],
}
T['Natural-looking hair strokes for fuller brows. Done in 2 sessions, $425 in total.'] = ('Fios naturais desenhados para sobrancelhas mais cheias. Feito em 2 sessões, $425 no total.', 'Trazos naturales para cejas más pobladas. Se hace en 2 sesiones, $425 en total.', 'משיכות שיער טבעיות לגבות מלאות יותר. מתבצע ב-2 מפגשים, $425 בסך הכול.', 'شعيرات طبيعية لحواجب أكثر كثافة. يتم على جلستين، بإجمالي $425.')
T['Natural hair strokes in 2 sessions ($425 total). $63.75 deposit to book.'] = ('Fios naturais em 2 sessões ($425 no total). Sinal de $63.75 para agendar.', 'Trazos naturales en 2 sesiones ($425 en total). Depósito de $63.75 para reservar.', 'משיכות שיער טבעיות ב-2 מפגשים ($425 בסך הכול). מקדמה של $63.75 להזמנת תור.', 'شعيرات طبيعية على جلستين (إجمالي $425). عربون $63.75 للحجز.')

# Pre-wax exfoliation rule aligned with professional guidance (27/10/2026)
MB.setdefault('ipa-waxing', []).append(('>Skip exfoliating and retinol creams the day before.<', '>Exfoliate gently 1–2 days before, not on the day of your wax. Pause retinol creams about 1 week before.<'))
T['Exfoliate gently 1–2 days before, not on the day of your wax. Pause retinol creams about 1 week before.'] = ('Esfolie de leve 1 a 2 dias antes, nunca no dia da depilação. Pare os cremes com retinol cerca de 1 semana antes.', 'Exfolia suavemente 1 a 2 días antes, nunca el mismo día de la depilación. Suspende las cremas con retinol una semana antes.', 'עשי פילינג עדין יום-יומיים לפני, לא ביום השעווה. הפסיקי קרמים עם רטינול כשבוע לפני.', 'قشّري بلطف قبل يوم أو يومين، وليس يوم الشمع. أوقفي كريمات الريتينول قبل أسبوع تقريباً.')

DET = ('<details style="background: #ffffff; border-radius: 18px; padding: 22px 26px"><summary style="font-size: 18px; font-weight: 600; color: #1f1f1f; cursor: pointer">%s</summary>'
       '<p style="margin: 12px 0 0; font-size: 16px; line-height: 1.6; color: #5c5c5c">%s</p></details>\n')
QSEC = ('<section style="background: #f5f5f7; padding: 100px 0">\n<div class="wrap" style="max-width: 860px">\n'
        '<h2 class="h-sec" style="margin: 0; text-align: center; font-size: 52px; line-height: 1.05; font-weight: 700; letter-spacing: -0.04em; color: #1f1f1f">Questions.</h2>\n'
        '<div style="margin-top: 44px; display: flex; flex-direction: column; gap: 12px">\n%s</div>\n</div>\n</section>\n')

LANGS = ['pt', 'es', 'he', 'ar']
esc = lambda t: t.replace('&', '&amp;')

def get(src, name):
    m = re.search(r'const %s = (.*?);\n' % name, src, re.S)
    return m, json.loads(m.group(1))

def put(src, m, name, val):
    return src[:m.start()] + 'const %s = %s;\n' % (name, json.dumps(val, ensure_ascii=False) if name == 'I18N' else json.dumps(val)) + src[m.end():]

def patch(path):
    tag = path.stem
    src = path.read_text(encoding='utf-8')
    orig = src
    mh, h = get(src, 'HTML')
    mi, I = get(src, 'I18N')

    # 1. Keyword line inside the H1 (replaces the small uppercase label above it)
    if tag in KW and 'class="ipa-kw"' not in h:
        old, new = KW[tag]
        pat = re.compile(r'<p style="margin: 0; font-size: 15px; font-weight: 600; letter-spacing: 0\.14em; text-transform: uppercase; color: (#[0-9a-f]{3,6})">'
                         + re.escape(old) + r'</p>\s*<h1 class="h-hero" style="margin: 1[68]px ([^;]*?) 0;')
        m = pat.search(h)
        assert m, (tag, 'label/h1 not found')
        col, side = m.group(1), m.group(2)
        h1_end = h.find('>', m.end()) + 1
        rest = h[m.end():h1_end]
        h = h[:m.start()] + '<h1 class="h-hero" style="margin: 0 %s 0;%s' % (side, rest) + '<span class="ipa-kw" style="%s">%s</span>' % (LABEL_STYLE % col, new) + h[h1_end:]

    h = re.sub(r'(<span class="ipa-kw"[^>]*>[^<]*</span>)(?=[^\s<])', r'\1 ', h)
    for a, b in MB.get(tag, []):
        if b not in h: h = h.replace(a, b)
    # 2. Breadcrumb "Home" goes to the home page, not the booking page
    h = h.replace('href="%s/services-5" target="_top" target="_top">Home</a>' % SITE, 'href="%s/" target="_top">Home</a>' % SITE)

    # 3. New questions
    items = FAQ.get(tag, [])
    new_items = [it for it in items if '>%s</summary>' % esc(it[0]) not in h]
    if new_items:
        det = ''.join(DET % (esc(q), esc(a)) for q, a, *_ in new_items)
        qi = h.find('>Questions.</h2>')
        if qi > 0:
            last = h.rfind('</details>', 0, h.find('</section>', qi)) + len('</details>')
            nl = 1 if h[last:last + 1] == '\n' else 0
            h = h[:last + nl] + det + h[last + nl:]
        else:
            bi = h.find('<section id="visit"')
            assert bi > 0, (tag, 'no place for questions')
            h = h[:bi] + QSEC % det + h[bi:]
    for q, a, *tr in items:
        for l, (tq, ta) in zip(LANGS, tr):
            I.setdefault(l, {})[q] = tq; I[l][a] = ta
    for en, tr in T.items():
        for l, t in zip(LANGS, tr):
            I.setdefault(l, {})[en] = t

    # 4. Lighter images (WebP) + lazy loading below the hero + reserved size for the hero logo
    h = re.sub(r'(%s/img/w/[\w.-]+)\.jpg' % re.escape(APP), r'\1.webp', h)
    h = h.replace(APP + '/img/logo3d.png', APP + '/img/logo3d.webp').replace(APP + '/img/phone-mockup.png', APP + '/img/phone-mockup.webp').replace(APP + '/img/icon-512.png', APP + '/img/icon-512.webp')
    top_end = h.find('</section>', h.find('<section id="top"')) if '<section id="top"' in h else 0
    def img_fix(m):
        tag_ = m.group(0)
        if 'logo3d' in tag_ and m.start() < top_end:
            if 'width="' not in tag_:
                tag_ = tag_.replace('<img ', '<img width="720" height="347" fetchpriority="high" decoding="async" ', 1)
            return tag_
        if 'loading=' not in tag_:
            tag_ = tag_.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
        return tag_
    h = re.sub(r'<img [^>]*>', img_fix, h)

    src = put(src, mh, 'HTML', h)
    _, mi = None, re.search(r'const I18N = (.*?);\n', src, re.S)
    src = put(src, mi, 'I18N', I)
    # modal (install popup) icon
    mm = re.search(r'const MODAL = (".*?");\n', src, re.S)
    if mm:
        mo = json.loads(mm.group(1)).replace(APP + '/img/icon-512.png', APP + '/img/icon-512.webp')
        src = src[:mm.start()] + 'const MODAL = %s;\n' % json.dumps(mo) + src[mm.end():]

    # 5. CSS for the keyword line (mobile-safe) + hero shows at once (no reveal animation above the fold)
    mc = re.search(r'const CSS = (".*?");\n', src, re.S)
    css = json.loads(mc.group(1))
    if '.ipa-kw' not in css:
        css += '.h-hero .ipa-kw{text-wrap:balance}@media(max-width:600px){.h-hero .ipa-kw{font-size:13px!important;letter-spacing:.1em!important;margin-bottom:12px!important}}:host([data-narrow]) .h-hero .ipa-kw{font-size:13px!important;letter-spacing:.1em!important;margin-bottom:12px!important}'
        src = src[:mc.start()] + 'const CSS = %s;\n' % json.dumps(css) + src[mc.end():]
    if 'details{align-self:stretch' not in css:
        css += ':host([data-narrow]) section details{align-self:stretch;width:100%}@media(max-width:600px){section details{align-self:stretch;width:100%}}'
        mc = re.search(r'const CSS = (".*?");\n', src, re.S)
        src = src[:mc.start()] + 'const CSS = %s;\n' % json.dumps(css) + src[mc.end():]
    hook = "const logo = root.querySelector('section img[src*=\"logo3d\"]');"
    if hook in src and 'closest(\'#top\')' not in src:
        src = src.replace(hook, "Array.from(set).forEach(el => { if (el.closest('#top')) set.delete(el); });\n      " + hook)
    # start downloading the hero logo as soon as the script runs
    if tag == 'ipa-home' and 'ipa-preload' not in src:
        src = src.replace("if (customElements.get('ipa-home')) return;",
                          "if (customElements.get('ipa-home')) return;\ntry { if (!document.getElementById('ipa-preload')) { const p = document.createElement('link'); p.id = 'ipa-preload'; p.rel = 'preload'; p.as = 'image'; p.href = '%s/img/logo3d.webp'; p.setAttribute('fetchpriority', 'high'); document.head.appendChild(p); } } catch (e) {}" % APP, 1)

    if src != orig:
        path.write_text(src, encoding='utf-8')
        print('patched', tag)

for p in sorted(SITE_DIR.glob('ipa-*.js')):
    if p.stem == 'ipa-book' or p.stem == 'ipa-welcome':
        # different templates; only swap image formats
        s = p.read_text(encoding='utf-8'); o = s
        s = re.sub(r'(%s/img/w/[\w.-]+)\.jpg' % re.escape(APP), r'\1.webp', s)
        s = s.replace(APP + '/img/logo3d.png', APP + '/img/logo3d.webp').replace(APP + '/img/icon-512.png', APP + '/img/icon-512.webp')
        if s != o: p.write_text(s, encoding='utf-8'); print('images', p.stem)
        continue
    patch(p)
