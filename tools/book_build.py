"""Generates site/ipa-book.js — Apple-style "Book now" page (replaces the old services-5 gallery).
Data = visible Wix Bookings services (queried 2026-10-21). Each row links to /booking-calendar/<slug>."""
import json, pathlib, re

OUT = pathlib.Path('/home/claude/ipanema-app/site')

S = [  # name, category, slug, price, minutes
 ("New Client Special: First Brazilian $39", "BRAZILIAN WAXING", "new-client-special-first-brazilian-39", "$39 (reg. $53)", 30),
 ("Brazilian First Time (Women)", "BRAZILIAN WAXING", "brazilian-first-time-women", "Starting at $53", 30),
 ("Brazilian Up to 4 Weeks (Women)", "BRAZILIAN WAXING", "brazilian-up-to-4-weeks-women", "49", 30),
 ("Brazilian Wax after 4 Weeks (Women)", "BRAZILIAN WAXING", "brazilian-wax-after-4-weeks-women", "53", 30),
 ("Brazilian Wax and Vajacial", "BRAZILIAN WAXING", "brazilian-wax-and-vajacial", "88", 60),
 ("Women Bikini (Full)", "BRAZILIAN WAXING", "women-bikini-full", "45", 30),
 ("Women Bikini (Deep)", "BRAZILIAN WAXING", "women-bikini-deep", "40", 30),
 ("Women Bikini (Line)", "BRAZILIAN WAXING", "women-bikini-line", "35", 30),
 ("Buttocks (Women)", "BRAZILIAN WAXING", "buttocks-women", "33", 30),
 ("Buttocks Strip (Women)", "BRAZILIAN WAXING", "buttocks-strip-women", "23", 30),
 ("Buttocks (Men)", "BRAZILIAN WAXING", "buttocks-men", "50", 30),

 ("Brows Shaping (First Time)", "BROWS AND LASHES BAR", "brows-shaping-first-time", "25", 30),
 ("Brows Maintenance (up to 2 weeks)", "BROWS AND LASHES BAR", "brows-maintenance-up-to-2-weeks", "18", 30),
 ("Brows Maintenance (up to 4 weeks)", "BROWS AND LASHES BAR", "brows-maintenance-up-to-4-weeks", "21", 30),
 ("Brows Maintenance (after 4 weeks)", "BROWS AND LASHES BAR", "brows-maintenance-after-4-weeks", "25", 30),
 ("Combo: Brows Shaping + Tinting or Henna", "BROWS AND LASHES BAR", "combo-brows-shaping-tinting-or-henna", "44", 60),
 ("Brows Tinting / Henna Filling", "BROWS AND LASHES BAR", "brows-tinting-henna-filling", "30", 30),
 ("Brows Lamination", "BROWS AND LASHES BAR", "brows-lamination", "73", 90),
 ("Grow Brow", "BROWS AND LASHES BAR", "grow-brow", "88", 60),
 ("Microblading or Micropigmentation", "BROWS AND LASHES BAR", "microblading-or-micropigmentation", "212.50", 120),
 ("Lashes Lifting", "BROWS AND LASHES BAR", "lashes-lifting", "73", 60),
 ("Lashes Tinting", "BROWS AND LASHES BAR", "lashes-tinting", "30", 30),
 ("Combo: Lashes Lifting + Tinting", "BROWS AND LASHES BAR", "combo-lashes-lifting-tinting", "88", 120),
 ("Consultation", "BROWS AND LASHES BAR", "consultation", "NO_FEE", 15),

 ("Legs (Women) (Full)", "Waxing", "legs-women-full", "Starting at $68", 45),
 ("Legs (Women) (Half) Lower", "Waxing", "legs-women-half-lower", "Starting at $43", 30),
 ("Women Upper Leg", "Waxing", "women-upper-leg", "45", 30),
 ("Women Inner Thigh", "Waxing", "women-inner-thigh", "25", 30),
 ("Knees (Women)", "Waxing", "knees-women", "20", 15),
 ("Toes (Women)", "Waxing", "toes-women", "18", 15),
 ("Underarm (Women)", "Waxing", "underarm-women", "27", 15),
 ("Women Arms (Full)", "Waxing", "women-arms-full", "48", 30),
 ("Women Arms (Half)", "Waxing", "women-arms-half", "33", 30),
 ("Hands (Women)", "Waxing", "hands-women-1", "13", 15),
 ("Women Back (Full)", "Waxing", "women-back-full", "53", 60),
 ("Women Back (Half)", "Waxing", "women-back-half", "33", 30),
 ("Shoulders (Women)", "Waxing", "shoulders-women", "25", 15),
 ("Chest (Full) Women", "Waxing", "chest-full-women", "33", 30),
 ("Chest (Strip) Women", "Waxing", "chest-strip-women", "23", 30),
 ("Breast (Around Nipple) Women", "Waxing", "breast-around-nipple-women", "15", 30),
 ("Stomach (Women)", "Waxing", "stomach-women", "Starting at $25", 15),
 ("Stomach Strip (Women)", "Waxing", "stomach-strip-women", "20", 15),
 ("Women Full Face", "Waxing", "women-full-face", "Starting at $53", 45),
 ("Women Lip (Threading or Waxing)", "Waxing", "women-lip-threading-or-waxing", "17", 15),
 ("Women Chin (Threading or Waxing)", "Waxing", "women-chin-threading-or-waxing", "17", 15),
 ("Women Sideburns", "Waxing", "women-sideburns", "17", 15),
 ("Forehead (Women)", "Waxing", "forehead-women", "17", 15),
 ("Nose (Women)", "Waxing", "nose-women", "17", 15),
 ("Women Neck", "Waxing", "women-neck", "23", 15),
 ("Combo Women (two areas)", "Waxing", "combo-women-two-areas", "Starting at $26", 15),
 ("Full Body (Women)", "Waxing", "full-body-women", "265", 165),
 ("Legs (Men) (Full)", "Waxing", "legs-men-full", "Starting at $78", 60),
 ("Legs (Men) (Half)", "Waxing", "legs-men-half", "45", 45),
 ("Men Upper Leg", "Waxing", "men-upper-leg", "50", 60),
 ("Chest (Full) Men", "Waxing", "chest-full-men", "43", 45),
 ("Chest (Strip) Men", "Waxing", "chest-strip-men", "30", 30),
 ("Breast (Around Nipple) Men", "Waxing", "breast-around-nipple-men", "20", 30),
 ("Stomach (Men)", "Waxing", "stomach-men", "35", 15),
 ("Stomach Strip (Men)", "Waxing", "stomach-strip-men", "28", 15),
 ("Men Back (Full)", "Waxing", "men-back-full", "68", 45),
 ("Men Back (Half)", "Waxing", "men-back-half", "43", 30),
 ("Shoulders (Men)", "Waxing", "shoulders-men", "30", 30),
 ("Men Arms (Full)", "Waxing", "men-arms-full", "53", 45),
 ("Men Arms (Half)", "Waxing", "men-arms-half", "45", 60),
 ("Underarm (Men)", "Waxing", "underarm-men", "30", 15),
 ("Hands (Men)", "Waxing", "hands-men-1", "18", 15),
 ("Men Full Face", "Waxing", "men-full-face", "65", 45),
 ("Men Neck", "Waxing", "men-neck", "28", 30),
 ("Men Nose", "Waxing", "men-nose", "18", 15),
 ("Ear (Men)", "Waxing", "ear-men", "18", 15),
 ("Combo Men (two areas)", "Waxing", "combo-men-two-areas", "30", 15),
 ("Full Body (Men)", "Waxing", "full-body-men", "315", 150),

 ("Women Hair Cut (wet or dry, cut only)", "HAIR", "women-hair-cut-wet-or-dry-only-cut", "60", 60),
 ("Hair Cut and Blow Dry", "HAIR", "hair-cut-and-blow-dry", "Starting at $80", 75),
 ("Men Hair Cut", "HAIR", "men-hair-cut", "35", 60),
 ("Kids Hair Cut (wet or dry, up to 12 yrs)", "HAIR", "kids-hair-cut-wet-or-dry-up-to-12-yrs", "Starting at $35", 45),
 ("Kids Hair Cut and Blow Dry (up to 12 yrs)", "HAIR", "kids-hair-cut-and-blow-dry-up-to-12-yr", "starting at $45", 60),
 ("Bang Trim", "HAIR", "bang-trim", "15", 30),
 ("Blow Dry Short", "HAIR", "blow-dry-short", "Starting at $60", 75),
 ("Blow Dry Medium", "HAIR", "blow-dry-medium", "Starting at $75", 80),
 ("Blow Dry Long", "HAIR", "blow-dry-long", "Starting at $85", 90),
 ("Curls", "HAIR", "curls", "Starting at $45", 60),
 ("Hair Wash", "HAIR", "hair-wash", "17", 15),
 ("All Over Color", "HAIR", "all-over-color", "Starting at $135", 120),
 ("Root Touch Up", "HAIR", "root-touch-up", "Starting at $75", 90),
 ("Toner", "HAIR", "toner", "Starting at $50", 45),
 ("Highlights Short", "HAIR", "highlights-short", "Starting at $190", 120),
 ("Highlights Medium", "HAIR", "highlights-medium", "Starting at $205", 180),
 ("Highlights Long", "HAIR", "highlights-long", "Starting at $300", 210),
 ("Balayage", "HAIR", "balayage", "Starting at $260.00", 180),
 ("Keratin", "HAIR", "keratin", "190", 180),
 ("Hydration (without machine)", "HAIR", "hydration-without-machine", "Starting at $65", 45),
 ("Hydration and Blow Dry (with machine)", "HAIR", "hydration-and-blow-dry-with-machine", "Starting at $100", 90),

 ("Facial", "FACIALS & SKIN", "facial", "Starting at $110", 90),
 ("Dermaplane", "FACIALS & SKIN", "dermaplane", "85", 60),
]

CATS = [("brows", "BROWS AND LASHES BAR"), ("brazilian", "BRAZILIAN WAXING"), ("waxing", "Waxing"), ("hair", "HAIR"), ("skin", "FACIALS & SKIN")]

def fmt_price(p):
    p = p.strip()
    if p == 'NO_FEE': return {'free': 1}
    m = re.match(r'(?i)starting at \$?([\d.]+)', p)
    if m: return {'from': m.group(1).rstrip('0').rstrip('.') if '.' in m.group(1) else m.group(1)}
    if re.fullmatch(r'[\d.]+', p):
        v = p
        if v.endswith('.00'): v = v[:-3]
        return {'v': v}
    return {'raw': p}

DATA = [{'n': n, 'c': dict((v, k) for k, v in CATS)[c], 's': s, 'p': fmt_price(p), 'm': m} for n, c, s, p, m in S]

T = {
 'en': {'eyebrow': 'Book online', 'title': 'Book your visit.', 'sub': 'Choose a service and pick a time. It takes less than a minute.',
        'brows': 'Brows & Lashes', 'brazilian': 'Brazilian', 'waxing': 'Waxing', 'hair': 'Hair', 'skin': 'Facials & Skin',
        'search': 'Search services', 'book': 'Book', 'from': 'from', 'free': 'Free', 'min': 'min', 'h': 'h',
        'none': 'No services found.', 'help': 'Not sure what to book? Message us on WhatsApp at 321-986-9171 or call 407-270-9102.',
        'sat': 'Saturdays only', 'policy': 'Cancellation & refund policy'},
 'pt': {'eyebrow': 'Agende online', 'title': 'Agende sua visita.', 'sub': 'Escolha o serviço e o horário. Leva menos de um minuto.',
        'brows': 'Sobrancelhas & Cílios', 'brazilian': 'Brasileira', 'waxing': 'Depilação', 'hair': 'Cabelo', 'skin': 'Faciais & Pele',
        'search': 'Buscar serviço', 'book': 'Agendar', 'from': 'a partir de', 'free': 'Grátis', 'min': 'min', 'h': 'h',
        'none': 'Nenhum serviço encontrado.', 'help': 'Na dúvida? Fale com a gente no WhatsApp 321-986-9171 ou ligue 407-270-9102.',
        'sat': 'Só aos sábados', 'policy': 'Política de cancelamento e reembolso'},
 'es': {'eyebrow': 'Reserva en línea', 'title': 'Reserva tu visita.', 'sub': 'Elige un servicio y un horario. Toma menos de un minuto.',
        'brows': 'Cejas y pestañas', 'brazilian': 'Brasileña', 'waxing': 'Depilación', 'hair': 'Cabello', 'skin': 'Faciales y piel',
        'search': 'Buscar servicios', 'book': 'Reservar', 'from': 'desde', 'free': 'Gratis', 'min': 'min', 'h': 'h',
        'none': 'No se encontraron servicios.', 'help': '¿Dudas? Escríbenos por WhatsApp al 321-986-9171 o llama al 407-270-9102.',
        'sat': 'Solo los sábados', 'policy': 'Política de cancelación y reembolso'},
 'he': {'eyebrow': 'הזמנה אונליין', 'title': 'הזמינו את הביקור שלכם.', 'sub': 'בחרו שירות ושעה. זה לוקח פחות מדקה.',
        'brows': 'גבות וריסים', 'brazilian': 'ברזילאי', 'waxing': 'שעווה', 'hair': 'שיער', 'skin': 'טיפולי פנים ועור',
        'search': 'חיפוש שירות', 'book': 'הזמנה', 'from': 'החל מ-', 'free': 'חינם', 'min': 'דק׳', 'h': 'ש׳',
        'none': 'לא נמצאו שירותים.', 'help': 'לא בטוחים מה להזמין? כתבו לנו בוואטסאפ 321-986-9171 או התקשרו 407-270-9102.',
        'sat': 'רק בשבתות', 'policy': 'מדיניות ביטולים והחזרים'},
 'ar': {'eyebrow': 'احجز عبر الإنترنت', 'title': 'احجز زيارتك.', 'sub': 'اختر الخدمة والموعد. يستغرق الأمر أقل من دقيقة.',
        'brows': 'الحواجب والرموش', 'brazilian': 'البرازيلي', 'waxing': 'إزالة الشعر بالشمع', 'hair': 'الشعر', 'skin': 'العناية بالبشرة',
        'search': 'ابحث عن خدمة', 'book': 'احجز', 'from': 'ابتداءً من', 'free': 'مجاني', 'min': 'د', 'h': 'س',
        'none': 'لم يتم العثور على خدمات.', 'help': 'لست متأكدًا؟ راسلنا على واتساب 321-986-9171 أو اتصل على 407-270-9102.',
        'sat': 'أيام السبت فقط', 'policy': 'سياسة الإلغاء والاسترداد'},
}

CSS = r'''
:host{display:block;width:100%;max-width:100vw;overflow-x:clip}*{box-sizing:border-box}
.r{font-family:Inter,-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,"Noto Sans Hebrew","Noto Sans Arabic",sans-serif;-webkit-font-smoothing:antialiased;color:#1f1f1f;background:#fff;position:relative;padding:72px 0 96px}
.w{max-width:900px;margin:0 auto;padding:0 24px}
.lang{position:absolute;top:14px;inset-inline-end:16px;z-index:5;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.92);border:1px solid #dcdcdc;border-radius:999px;padding:0 10px 0 12px;height:38px;box-shadow:0 4px 14px rgba(0,0,0,.08);font:600 13px Inter,system-ui,sans-serif;color:#333}
.lang select{appearance:none;-webkit-appearance:none;border:0;background:transparent;font:inherit;color:inherit;cursor:pointer;outline:none}
.ey{margin:0;text-align:center;font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#6b6b6b}
h1{margin:14px 0 0;text-align:center;font-size:72px;line-height:1.02;font-weight:700;letter-spacing:-.045em}
.sub{margin:18px auto 0;max-width:560px;text-align:center;font-size:20px;line-height:1.5;color:#4d4d4d}
.tabs{margin:40px auto 0;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.tabs button{height:40px;padding:0 18px;border-radius:999px;border:1px solid #dcdcdc;background:#fff;color:#333;font:600 15px Inter,system-ui,sans-serif;cursor:pointer}
.tabs button.on{background:#1f1f1f;border-color:#1f1f1f;color:#fff}
.q{display:block;width:100%;max-width:420px;margin:20px auto 0;height:46px;border-radius:14px;border:1px solid #dcdcdc;background:#f5f5f7;padding:0 16px;font:16px Inter,system-ui,sans-serif;color:#1f1f1f;outline:none}
.q:focus{background:#fff;border-color:#999}
.list{margin-top:28px;background:#f5f5f7;border-radius:24px;padding:6px 22px}
.row{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid #e3e3e6}
.row:last-child{border-bottom:0}
.nm{flex:1;min-width:0}
.nm b{display:block;font-size:17px;font-weight:600;line-height:1.3}
.nm span{display:block;margin-top:3px;font-size:14px;color:#6b6b6b}
.nm i{font-style:normal;display:inline-block;margin-inline-start:8px;padding:2px 8px;border-radius:999px;background:#e9e3cf;color:#3f463b;font-size:12px;font-weight:600}
.pr{font-size:17px;font-weight:600;white-space:nowrap;text-align:end}
.pr small{display:block;font-size:12px;font-weight:500;color:#6b6b6b}
.bk{flex:none;display:inline-flex;align-items:center;justify-content:center;height:40px;padding:0 18px;border-radius:999px;background:#333;color:#fff;text-decoration:none;font-size:15px;font-weight:600}
.none{padding:28px 0;text-align:center;color:#6b6b6b}
.help{margin:28px auto 0;max-width:620px;text-align:center;font-size:15px;line-height:1.6;color:#6b6b6b}
.help a{color:#333;font-weight:600}
:host([data-narrow]) .r{padding:56px 0 72px}
:host([data-narrow]) h1{font-size:clamp(30px,calc(var(--ipa-w,390px)*.12),52px)}
:host([data-narrow]) .sub{font-size:17px}
:host([data-narrow]) .w{padding:0 16px}
:host([data-narrow]) .list{padding:4px 14px;border-radius:20px}
:host([data-narrow]) .row{flex-wrap:wrap;gap:8px 12px}
:host([data-narrow]) .nm{flex-basis:100%}
:host([data-narrow]) .pr{text-align:start;flex:1}
:host([data-narrow]) .tabs{justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:4px;margin-inline:-16px;padding-inline:16px}
:host([data-narrow]) .tabs button{flex:none}
:host{--ease-out:cubic-bezier(0.23,1,0.32,1)}
h1,.sub,.help{text-wrap:balance}
.tabs button{transition:background-color 200ms ease,color 200ms ease,border-color 200ms ease,transform 160ms var(--ease-out)}
.tabs button:active,.bk:active{transform:scale(0.97)}
.bk{transition:background-color 200ms ease,transform 160ms var(--ease-out)}
.q{transition:background-color 200ms ease,border-color 200ms ease,box-shadow 200ms ease}
.q:focus{box-shadow:0 0 0 4px rgba(51,51,51,.08)}
.tabs button:focus-visible,.bk:focus-visible,.help a:focus-visible,.lang select:focus-visible{outline:2px solid #333;outline-offset:2px}
.row{transition:background-color 200ms ease}
@media (hover:hover) and (pointer:fine){
 .tabs button:not(.on):hover{border-color:#333;background:#fafafa}
 .bk:hover{background:#1f1f1f}
}
@keyframes ri{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.list.anim .row,.list.anim .none{animation:ri 320ms var(--ease-out) both;animation-delay:calc(min(var(--i,0),8) * 30ms)}
.intro .ey,.intro h1,.intro .sub,.intro .tabs,.intro .q,.intro .list{animation:ri 700ms var(--ease-out) both}
.intro h1{animation-delay:70ms}.intro .sub{animation-delay:140ms}.intro .tabs{animation-delay:210ms}.intro .q{animation-delay:260ms}.intro .list{animation-delay:310ms}
.intro .tabs button{animation:ri 500ms var(--ease-out) both;animation-delay:calc(240ms + var(--i,0) * 50ms)}
:host([data-narrow]) .tabs{-webkit-mask-image:linear-gradient(90deg,transparent,#000 16px,#000 calc(100% - 28px),transparent);mask-image:linear-gradient(90deg,transparent,#000 16px,#000 calc(100% - 28px),transparent);scrollbar-width:none}
:host([data-narrow]) .tabs::-webkit-scrollbar{display:none}
@media (prefers-reduced-motion:reduce){
 .list.anim .row,.list.anim .none,.intro .ey,.intro h1,.intro .sub,.intro .tabs,.intro .q,.intro .list,.intro .tabs button{animation-name:rf;animation-duration:200ms;animation-delay:0ms}
 .tabs button:active,.bk:active{transform:none}
}
@keyframes rf{from{opacity:0}to{opacity:1}}
'''

JS = r'''/* Ipanema Beauty & Spa — ipa-book (generated) */
(function(){
if (customElements.get('ipa-book')) return;
const T = __T__; const D = __D__; const CSS = __CSS__; const CATS = __CATS__;
const LS = ['en','pt','es','he','ar'];
const SITE = 'https://www.ipanemabeautyandspa.com';
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
class E extends HTMLElement {
  connectedCallback(){
    if (this._r) return; this._r = 1;
    if (!document.getElementById('ipa-inter')) { const l=document.createElement('link'); l.id='ipa-inter'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'; document.head.appendChild(l); }
    this.style.display = 'block'; this.style.width = '100%';
    const setW = () => { let m = Infinity, p = this.parentElement; while (p && p !== document.documentElement) { const cw = p.clientWidth; if (cw > 0 && cw < m) m = cw; p = p.parentElement; }
      if (m < Infinity && Math.abs(this.offsetWidth - m) > 1) { this.style.maxWidth = m + 'px'; this.style.width = m + 'px'; }
      const w = Math.min(this.clientWidth || m, m); if (w && w < Infinity) { this.style.setProperty('--ipa-w', w + 'px'); this.toggleAttribute('data-narrow', w < 700); } };
    setW(); try { new ResizeObserver(setW).observe(this); } catch (e) { window.addEventListener('resize', setW); }
    let lang = '', cat = '';
    try { const u = new URLSearchParams(location.search); lang = u.get('lang') || localStorage.getItem('ipa-site-lang') || ''; cat = u.get('cat') || ''; } catch (e) {}
    if (LS.indexOf(lang) < 0) { const b = (navigator.language || 'en').slice(0, 2).toLowerCase(); lang = LS.indexOf(b) >= 0 ? b : 'en'; }
    this.lang = lang; this.cat = CATS.indexOf(cat) >= 0 ? cat : 'brows'; this.q = '';
    this.root = this.attachShadow({mode:'open'});
    this.render();
    window.addEventListener('ipa-lang', e => { if (LS.indexOf(e.detail) >= 0) { this.lang = e.detail; this.render(); } });
  }
  price(p){ const t = T[this.lang];
    if (p.free) return t.free;
    if (p.from) return '<small>' + t.from + '</small>$' + p.from;
    if (p.v) return '$' + p.v;
    return esc(p.raw); }
  dur(m){ const t = T[this.lang]; if (m < 60) return m + ' ' + t.min; const h = Math.floor(m / 60), r = m % 60; return h + ' ' + t.h + (r ? ' ' + r + ' ' + t.min : ''); }
  rows(){ const t = T[this.lang], q = this.q.trim().toLowerCase();
    const list = D.filter(s => q ? s.n.toLowerCase().indexOf(q) >= 0 : s.c === this.cat);
    if (!list.length) return '<div class="none">' + t.none + '</div>';
    return list.map((s, i) => '<div class="row" style="--i:' + i + '"><div class="nm"><b>' + esc(s.n) + (s.s.indexOf('new-client-special') === 0 ? '<i>' + t.sat + '</i>' : '') + '</b><span>' + this.dur(s.m) + '</span></div>' +
      '<div class="pr">' + this.price(s.p) + '</div><a class="bk" target="_top" href="' + SITE + '/booking-calendar/' + s.s + '">' + t.book + '</a></div>').join(''); }
  render(){ const t = T[this.lang], rtl = this.lang === 'he' || this.lang === 'ar';
    const opts = [['en','English'],['pt','Português'],['es','Español'],['he','עברית'],['ar','العربية']].map(o => '<option value="' + o[0] + '"' + (o[0] === this.lang ? ' selected' : '') + '>' + o[1] + '</option>').join('');
    const intro = !this._shown; this._shown = 1;
    this.root.innerHTML = '<style>' + CSS + '</style><div class="r' + (intro ? ' intro' : '') + '" dir="' + (rtl ? 'rtl' : 'ltr') + '" lang="' + this.lang + '">' +
      '<label class="lang"><span aria-hidden="true">🌐</span><select aria-label="Language">' + opts + '</select></label><div class="w">' +
      '<p class="ey">' + t.eyebrow + '</p><h1>' + t.title + '</h1><p class="sub">' + t.sub + '</p>' +
      '<div class="tabs" role="tablist">' + CATS.map((c, i) => '<button type="button" role="tab" style="--i:' + i + '" data-c="' + c + '" class="' + (c === this.cat && !this.q ? 'on' : '') + '">' + t[c] + '</button>').join('') + '</div>' +
      '<input class="q" type="search" placeholder="' + t.search + '" value="' + esc(this.q) + '">' +
      '<div class="list">' + this.rows() + '</div>' +
      '<p class="help">' + t.help + '<br><a href="' + SITE + '/copy-of-terms-and-conditions" target="_top">' + t.policy + '</a></p></div></div>';
    const r = this.root;
    r.querySelector('.lang select').onchange = e => { const v = e.target.value; try { localStorage.setItem('ipa-site-lang', v); } catch (x) {} window.dispatchEvent(new CustomEvent('ipa-lang', { detail: v })); };
    const inp = r.querySelector('.q'), lst = r.querySelector('.list'), tabs = r.querySelectorAll('.tabs button');
    if (intro) setTimeout(() => { const x = r.querySelector('.intro'); if (x) x.classList.remove('intro'); }, 1400);
    tabs.forEach(b => b.onclick = () => {
      if (b.dataset.c === this.cat && !this.q) return;
      this.cat = b.dataset.c; this.q = ''; inp.value = '';
      tabs.forEach(x => x.classList.toggle('on', x === b));
      lst.classList.remove('anim'); lst.innerHTML = this.rows(); void lst.offsetWidth; lst.classList.add('anim');
      if (this.hasAttribute('data-narrow')) try { b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); } catch (e) {}
    });
    inp.oninput = () => { this.q = inp.value; lst.classList.remove('anim'); lst.innerHTML = this.rows(); r.querySelectorAll('.tabs button').forEach(b => b.classList.toggle('on', !this.q && b.dataset.c === this.cat)); };
  }
}
customElements.define('ipa-book', E);
})();
'''

js = (JS.replace('__T__', json.dumps(T, ensure_ascii=False)).replace('__D__', json.dumps(DATA, ensure_ascii=False))
        .replace('__CSS__', json.dumps(CSS)).replace('__CATS__', json.dumps([k for k, _ in CATS])))
(OUT / 'ipa-book.js').write_text(js, encoding='utf-8')
(OUT / 'ipa-book.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>ipa-book</title><body style="margin:0"><script src="ipa-book.js"></script><ipa-book></ipa-book></body>', encoding='utf-8')
print('ok', len(DATA))
