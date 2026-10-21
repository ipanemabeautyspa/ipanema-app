import re, html, json, pathlib

SRC = pathlib.Path('/tmp/claude-0/-home-claude/0c6e43e4-0f65-549f-9e17-91c789eeb5bd/scratchpad/site/project')
OUT = pathlib.Path('/home/claude/ipanema-app/site')
OUT.mkdir(exist_ok=True)
APP = 'https://app.ipanemabeautyandspa.com'
SITE = 'https://www.ipanemabeautyandspa.com'
BOOK = SITE + '/services-5'
BRAZ = SITE + '/booking-calendar/new-client-special-first-brazilian-39'
WA = 'https://wa.me/13219869171'

BLOBS = {
 '9a3a069277f2cf5b23a5c0b1ca4ef8ce': '/img/logo3d.png',
 '73cff51024726766a9f598d6aa573743': '/img/icon-512.png',
 '7c42f684a39b92a5ab8005dd85030c2e': '/img/phone-mockup.png',
 '32f42429c3cd43aa9d1214a405521376': '/img/w/hair-090.jpg',
 '7db3917391c3d46bff5965bcde954701': '/img/w/hair-065.jpg',
 '97c382d24d7aca9949a2eb7361cf1deb': '/img/w/hair-134.jpg',
 '3fe441e5d3da94ae7c25b8588145a918': '/img/w/hair-194.jpg',
 'ca412bc54d901de9bb3278386379137e': '/img/w/hair-218.jpg',
 'd04316f96a68eb9a82245e4153c52713': '/img/w/hair-072.jpg',
 'ef64dc3b24deefa1b74a401cde5c735e': '/img/w/hair-195.jpg',
 'fa090d2a96f2c0c05cf1177aaf75a901': '/img/w/brow-149.jpg',
 'feafe9106a0e667b1b291fe295f7abb2': '/img/w/brow-151.jpg',
 '3a8f815cb1136a0b2933c805db881d5b': '/img/w/brow-152.jpg',
 'ac63ea9d5d7512e9f0e11345d1fd99c1': '/img/w/brow-076.jpg',
 'e8c4d2c72dbbb9d92f7fa2756513d814': '/img/w/brow-150.jpg',
}
PAGE_BLOBS = {
 'Main': {'fa090d2a96f2c0c05cf1177aaf75a901': '/img/w/brow-170.jpg',   # hero
          'feafe9106a0e667b1b291fe295f7abb2': '/img/w/brow-076.jpg',   # brows tile
          '3a8f815cb1136a0b2933c805db881d5b': '/img/w/brow-155.jpg'},  # who we are
 'Brows': {'e8c4d2c72dbbb9d92f7fa2756513d814': '/img/w/brow-150.jpg',
           'feafe9106a0e667b1b291fe295f7abb2': '/img/w/brow-075.jpg',
           'fa090d2a96f2c0c05cf1177aaf75a901': '/img/w/brow-172.jpg',
           'ac63ea9d5d7512e9f0e11345d1fd99c1': '/img/w/brow-145.jpg',
           '3a8f815cb1136a0b2933c805db881d5b': '/img/w/brow-155.jpg'},
}
PAGES = {'Main': ('ipa-home', '/'), 'Brows': ('ipa-brows', '/browsandlashes'), 'Waxing': ('ipa-waxing', '/waxing'),
         'Hair': ('ipa-hair', '/hair'), 'Contact': ('ipa-visit', '/contact-8')}
NAV = {'brows': '/browsandlashes', 'waxing': '/waxing', 'hair': '/hair', 'visit': '/contact-8', 'contact': '/contact-8', 'home': '/', 'app': '/#app'}
SOCIAL = {'Instagram': 'https://www.instagram.com/ipanemabeauty_spa', 'Facebook': 'https://www.facebook.com/ipanemabeautyandspa',
          'TikTok': 'https://www.tiktok.com/@ipanemabeauty_spa', 'YouTube': 'https://www.youtube.com/@ipanemabeautyandspa',
          'Pinterest': 'https://www.pinterest.com/ipanemabeautyandspa/', 'Yelp': 'https://www.yelp.com/biz/ipanema-beauty-and-spa-orlando-2'}
MAP = '<iframe title="Map to Ipanema Beauty &amp; Spa" src="https://www.google.com/maps?q=Ipanema+Beauty+and+Spa,+6735+Conroy+Rd+Suite+114,+Orlando,+FL+32835&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="border:0;width:100%;height:100%;min-height:{h}px;border-radius:28px;display:block"></iframe>'

SOC = {k.lower(): v for k, v in SOCIAL.items()}
import os as _os
_SI = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'si/package/icons')
def svg(n):
    t = open(_os.path.join(_SI, n + '.svg')).read()
    return t.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1).replace(re.search(r'<title>.*?</title>', t).group(0), '')
GMAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Ipanema+Beauty+and+Spa+6735+Conroy+Rd+Orlando'
GICON = '<span class="ipa-gi">' + svg('google') + '</span>'

def fix_link(m):
    attrs, text = m.group(1), m.group(2)
    t = re.sub('<[^>]+>', '', text).strip().lower()
    t = html.unescape(t)
    hm = re.search(r'href="([^"]*)"', attrs)
    href = hm.group(1) if hm else ''
    first = t.split()[0] if t.split() else ''
    extra = ''
    if t in SOC:
        new = SOC[t]
    elif 'whatsapp' in t:
        new = WA
    elif t.startswith('call') or re.search(r'\d{3}-\d{3}-\d{4}', t) and 'whatsapp' not in t:
        num = re.search(r'(\d{3})-(\d{3})-(\d{4})', t)
        new = 'tel:+1' + ''.join(num.groups()) if num else 'tel:+14072709102'
    elif 'directions' in t or 'open in maps' in t:
        new = 'https://maps.google.com/?q=Ipanema+Beauty+and+Spa+6735+Conroy+Rd+Orlando'
    elif 'refund' in t:
        new = SITE + '/copy-of-terms-and-conditions'
    elif 'book saturday' in t:
        new = BRAZ
    elif t.startswith('the ipanema app') or t.startswith('get the app'):
        new = '#app'; extra = ' data-install'
    elif first in ('brows', 'brows &') or t.startswith('brows'):
        new = SITE + '/browsandlashes'
    elif first == 'waxing':
        new = SITE + '/waxing'
    elif first == 'hair':
        new = SITE + '/hair'
    elif 'see prices' in t:
        new = SITE + '/browsandlashes'
    elif href.startswith('#') and href != '#book':
        new = href
    else:
        new = BOOK
    new_attrs = re.sub(r'href="[^"]*"', 'href="%s"' % new, attrs) if hm else attrs + ' href="%s"' % new
    if new.startswith('http') and 'ipanemabeautyandspa.com' not in new:
        new_attrs += ' target="_blank" rel="noopener"'
    elif new.startswith(SITE):
        new_attrs += ' target="_top"'
    return '<a%s%s>%s</a>' % (new_attrs, extra, text)

def convert(name):
    s = (SRC / f'{name}.dc.html').read_text()
    style = '\n'.join(re.findall(r'<style>(.*?)</style>', s, re.S))
    body = re.search(r'</helmet>\s*(.*)</x-dc>', s, re.S).group(1)
    body = re.sub(r'<header.*?</header>', '', body, flags=re.S)
    body = re.sub(r'<sc-if value="\{\{install\}\}".*?</div>\s*</div>\s*</sc-if>', '', body, flags=re.S)
    body = re.sub(r'<sc-if.*?</sc-if>', '', body, flags=re.S)
    for k, v in PAGE_BLOBS.get(name, {}).items():
        body = body.replace('/_blob/' + k, APP + v)
    for k, v in BLOBS.items():
        body = body.replace('/_blob/' + k, APP + v)
    body = re.sub(r'7 languages</strong>[^<]*', 'We speak</strong> · English · Português · Español', body)
    if name == 'Main':
        body = body.replace('<section id="top" style="background: #f5f5f7; padding: 88px 0 0;', '<section id="top" style="background: #f5f5f7; padding: 64px 0 0;', 1)
        body = body.replace('<div class="wrap">', '<div class="wrap"><img src="%s/img/logo3d.png" alt="Ipanema Beauty &amp; Spa" style="display:block;margin:0 auto 34px;width:min(440px,82vw);height:auto;filter:drop-shadow(0 22px 34px rgba(0,0,0,.16))">' % APP, 1)
    body = re.sub(r'<a([^>]*)>(.*?)</a>', fix_link, body, flags=re.S)
    body = body.replace('onClick="{{openInstall}}"', 'data-install')
    # social names -> clickable icons
    def _ico(m):
        a, n = m.group(1), m.group(2)
        return a[:-1] + ' class="ipa-soc" aria-label="%s" title="%s">' % (n, n) + svg(n.lower()) + '</a>'
    body = body.replace('>Instagram · Facebook · TikTok · YouTube · Pinterest · Yelp</p>', '>' + ''.join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (SOCIAL[n], n) for n in ['Instagram','Facebook','TikTok','YouTube','Pinterest','Yelp']) + '</p>')
    body = re.sub(r'(<a [^>]*>)(Instagram|Facebook|TikTok|YouTube|Pinterest|Yelp)</a>', _ico, body)
    body = re.sub(r'</a>\s*·\s*(?=<a [^>]*class="ipa-soc")', '</a>', body)
    # Google icon + link
    body = body.replace('<span><strong style="color: #1f1f1f">★ 4.9</strong> on Google · 100+ reviews</span>',
        '<a class="ipa-glink" href="%s" target="_blank" rel="noopener"><strong style="color: #1f1f1f">★ 4.9</strong> %s on Google · 100+ reviews</a>' % (GMAPS, GICON))
    body = re.sub(r'(<p[^>]*>)(★★★★★ 4.9 on Google from 115 reviews)</p>', lambda m: m.group(1) + '<a class="ipa-glink" href="%s" target="_blank" rel="noopener">%s %s</a></p>' % (GMAPS, GICON, m.group(2)), body)
    body = re.sub(r' · Google</p>', ' <a class="ipa-glink" href="%s" target="_blank" rel="noopener" aria-label="Google review">%s</a></p>' % (GMAPS, GICON), body)
    # the app is presented once (dedicated section), not also as a tile
    body = re.sub(r'<a href="#app" style="background: linear-gradient.*?</a>\n(?=</div>\n</section>)', '', body, flags=re.S)
    body = body.replace('<a id="hair" href="#book" style="background: #f5f5f7;', '<a id="hair" href="#book" style="grid-column: 1 / -1; background: #f5f5f7;', 1)
    body = body.replace('Privacy · Terms · Refund &amp; Cancellation', '<a href="%s/privacy-policy" target="_top">Privacy</a> · <a href="%s/copy-of-privacy-policy" target="_top">Terms</a> · <a href="%s/copy-of-terms-and-conditions" target="_top">Refund &amp; Cancellation</a>' % (SITE, SITE, SITE))
    body = re.sub(r'<div style="[^"]*">\[Google Map[^\]]*\]</div>', lambda m: MAP.format(h=440), body)
    # contact form -> contact buttons
    body = re.sub(r'<form .*?</form>', '''<div style="background:#ffffff;border-radius:26px;padding:34px;display:flex;flex-direction:column;gap:12px;box-shadow:0 20px 50px rgba(60,50,20,0.10)">
<a href="%s" target="_blank" rel="noopener" style="height:56px;border-radius:999px;background:#333333;color:#ffffff;font-size:17px;font-weight:600;display:flex;align-items:center;justify-content:center">WhatsApp 321-986-9171</a>
<a href="tel:+14072709102" style="height:56px;border-radius:999px;border:1px solid #c9c9c9;color:#333333;font-size:17px;font-weight:600;display:flex;align-items:center;justify-content:center">Call 407-270-9102</a>
<a href="mailto:ipanemabeautyandspa@gmail.com" style="height:56px;border-radius:999px;border:1px solid #c9c9c9;color:#333333;font-size:17px;font-weight:600;display:flex;align-items:center;justify-content:center">Email us</a>
</div>''' % WA, body, flags=re.S)
    assert '{{' not in body, re.findall(r'\{\{[^}]*\}\}', body)[:5]
    return style, body

INSTALL = '''<div class="ipa-modal" hidden><div class="ipa-card" role="dialog" aria-modal="true" aria-label="Get the Ipanema app">
<button type="button" class="ipa-x" aria-label="Close">×</button>
<div style="display:flex;align-items:center;gap:16px"><img src="%s/img/icon-512.png" alt="" style="width:64px;height:64px;border-radius:15px;box-shadow:0 6px 16px rgba(0,0,0,.12)">
<div><h2 style="margin:0;font-size:28px;font-weight:700;letter-spacing:-.03em;color:#1f1f1f">Get the Ipanema app</h2><p style="margin:4px 0 0;font-size:15px;color:#6b6b6b">Free · 30 seconds · no App Store needed</p></div></div>
<div class="ipa-tabs"><button type="button" data-t="ios" class="on">iPhone</button><button type="button" data-t="and">Android</button></div>
<ol data-p="ios"><li>Open <b>app.ipanemabeautyandspa.com</b> in <b>Safari</b>.</li><li>Tap the <b>Share</b> button.</li><li>Tap <b>Add to Home Screen</b>, then <b>Add</b>.</li></ol>
<ol data-p="and" hidden><li>Open <b>app.ipanemabeautyandspa.com</b> in <b>Chrome</b>.</li><li>Tap the <b>⋮</b> menu.</li><li>Tap <b>Install app</b> or <b>Add to Home screen</b>.</li></ol>
<a href="%s" target="_blank" rel="noopener" class="ipa-go">Open the app</a></div></div>''' % (APP, APP)
MODAL_CSS = '''.ipa-modal{position:fixed;inset:0;z-index:99999;background:rgba(40,40,40,.45);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:24px}
.ipa-modal[hidden]{display:none}.ipa-card{position:relative;width:100%;max-width:520px;background:#fff;border-radius:28px;padding:40px 36px 30px;box-shadow:0 40px 100px rgba(0,0,0,.3);box-sizing:border-box}
.ipa-x{position:absolute;top:16px;right:16px;width:44px;height:44px;border-radius:50%;border:0;background:#f2f2f2;color:#4d4d4d;font-size:20px;cursor:pointer}
.ipa-tabs{margin-top:24px;display:grid;grid-template-columns:1fr 1fr;gap:6px;background:#f2f2f2;border-radius:999px;padding:4px}
.ipa-tabs button{height:40px;border:0;border-radius:999px;background:transparent;font:600 15px/1 inherit;font-family:inherit;color:#333;cursor:pointer}.ipa-tabs button.on{background:#fff}
.ipa-card ol{margin:20px 0 0;padding-left:22px;font-size:17px;line-height:1.7;color:#333}.ipa-card ol[hidden]{display:none}
.ipa-go{margin-top:22px;height:52px;border-radius:999px;background:#333;color:#fff !important;font-size:17px;font-weight:600;display:flex;align-items:center;justify-content:center}'''

LANGBAR = ('<label class="ipa-lang"><span aria-hidden="true">🌐</span><select aria-label="Language">'
           '<option value="en">English</option><option value="pt">Português</option><option value="es">Español</option>'
           '<option value="he">עברית</option><option value="ar">العربية</option></select></label>')
LANG_CSS = ('.ipa-root{position:relative}.ipa-lang{position:absolute;top:14px;inset-inline-end:16px;z-index:20;display:flex;align-items:center;gap:6px;'
            'background:rgba(255,255,255,.92);border:1px solid #dcdcdc;border-radius:999px;padding:0 10px 0 12px;height:38px;'
            'box-shadow:0 4px 14px rgba(0,0,0,.08);font:600 13px Inter,system-ui,sans-serif;color:#333}'
            '.ipa-lang select{appearance:none;-webkit-appearance:none;border:0;background:transparent;font:inherit;color:inherit;padding:0 2px;cursor:pointer;outline:none}'
            '.ipa-soc{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;border:1px solid rgba(128,128,128,.35);margin:2px;color:inherit}div:has(>.ipa-soc){gap:6px!important;justify-content:center}'
            '.ipa-soc svg{width:19px;height:19px;fill:currentColor}.ipa-soc:hover{background:rgba(128,128,128,.12)}'
            '.ipa-gi{display:inline-flex;vertical-align:-3px}.ipa-gi svg{width:18px;height:18px;fill:#4285F4}.ipa-glink{color:inherit}'
            'div[style*="justify-content: space-between"]>strong:last-child{white-space:nowrap;text-align:end;flex-shrink:0}'
            '.ipa-root[dir=rtl],.ipa-card[dir=rtl]{font-family:Inter,"Noto Sans Hebrew","Noto Sans Arabic",system-ui,sans-serif}')
import os
_src = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n_src.json')))
_I = {}
for _l in ['pt', 'es', 'he', 'ar']:
    _f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'i18n_%s.json' % _l)
    if os.path.exists(_f):
        _t = json.load(open(_f))
        assert len(_t) == len(_src), _l
        _I[_l] = {a: b for a, b in zip(_src, _t) if b and b != a}
        for a, b in zip(_src, _t):
            if a.endswith(' · Google'):
                _I[_l][a[:-9]] = re.sub(r'\s*·\s*Google\s*$', '', b)
I18N_JSON = json.dumps(_I, ensure_ascii=False)

TPL = '''/* Ipanema Beauty & Spa — %(tag)s (generated) */
(function(){
if (customElements.get('%(tag)s')) return;
const CSS = %(css)s;
const HTML = %(html)s;
const MODAL = %(modal)s;
const I18N = %(i18n)s;
class E extends HTMLElement {
  connectedCallback(){
    if (this._r) return; this._r = 1;
    if (!document.getElementById('ipa-inter')) { const l = document.createElement('link'); l.id='ipa-inter'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'; document.head.appendChild(l); }
    const r = this.attachShadow({mode:'open'});
    r.innerHTML = '<style>'+CSS+'</style>' + HTML + MODAL;
    this.style.display = 'block'; this.style.width = '100%%';
    const LS = ['en','pt','es','he','ar'];
    const walk = () => { const out = []; const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentNode && n.parentNode.nodeName === 'STYLE' ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT }); let n; while ((n = w.nextNode())) out.push(n); return out; };
    const nodes = walk().filter(n => /[A-Za-z]/.test(n.nodeValue));
    nodes.forEach(n => n.__en = n.nodeValue);
    const sel = r.querySelector('.ipa-lang select');
    const apply = l => {
      const d = I18N[l] || {};
      nodes.forEach(n => { const o = n.__en, k = o.replace(/\\s+/g, ' ').trim(); const t = d[k]; n.nodeValue = t ? o.match(/^\\s*/)[0] + t + o.match(/\\s*$/)[0] : o; });
      const rtl = l === 'he' || l === 'ar';
      r.querySelectorAll('.ipa-root, .ipa-card').forEach(x => { x.dir = rtl ? 'rtl' : 'ltr'; x.lang = l; });
      if (sel) sel.value = l;
    };
    let lang = '';
    try { lang = new URLSearchParams(location.search).get('lang') || localStorage.getItem('ipa-site-lang') || ''; } catch (e) {}
    if (LS.indexOf(lang) < 0) { const b = (navigator.language || 'en').slice(0, 2).toLowerCase(); lang = LS.indexOf(b) >= 0 ? b : 'en'; }
    apply(lang);
    if (sel) sel.addEventListener('change', () => { try { localStorage.setItem('ipa-site-lang', sel.value); } catch (e) {} window.dispatchEvent(new CustomEvent('ipa-lang', { detail: sel.value })); });
    window.addEventListener('ipa-lang', e => apply(e.detail));
    const m = r.querySelector('.ipa-modal');
    r.querySelectorAll('a[href^="#"]').forEach(a => { if (a.hasAttribute('data-install')) return; a.addEventListener('click', e => { const id = a.getAttribute('href').slice(1); const el = id && r.getElementById(id); if (el) { e.preventDefault(); el.scrollIntoView({behavior:'smooth'}); } else if (id==='top') { e.preventDefault(); this.scrollIntoView({behavior:'smooth'}); } }); });
    if (m) {
      r.querySelectorAll('[data-install]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); m.hidden = false; }));
      m.querySelector('.ipa-x').addEventListener('click', () => m.hidden = true);
      m.addEventListener('click', e => { if (e.target === m) m.hidden = true; });
      m.querySelectorAll('.ipa-tabs button').forEach(b => b.addEventListener('click', () => {
        m.querySelectorAll('.ipa-tabs button').forEach(x => x.classList.toggle('on', x === b));
        m.querySelectorAll('ol').forEach(o => o.hidden = o.dataset.p !== b.dataset.t); }));
    }
  }
}
customElements.define('%(tag)s', E);
})();
'''

for name, (tag, _) in PAGES.items():
    style, body = convert(name)
    css = (':host{display:block;width:100%}*{box-sizing:border-box}' + style.replace('body{', '.ipa-root{') +
           '\nimg{max-width:100%}a{color:#4d4d4d;text-decoration:none}\n' + MODAL_CSS + LANG_CSS)
    html_ = '<div class="ipa-root">' + LANGBAR + body + '</div>'
    modal = INSTALL
    (OUT / f'{tag}.js').write_text(encoding='utf-8', data=TPL % {'tag': tag, 'css': json.dumps(css), 'html': json.dumps(html_), 'modal': json.dumps(modal), 'i18n': I18N_JSON})
    # preview page
    (OUT / f'{tag}.html').write_text(f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{tag}</title><body style="margin:0"><script src="{tag}.js"></script><{tag}></{tag}></body>')
    print(tag, len(html_))

src = (OUT / 'ipa-visit.js').read_text()
m = re.search(r'const HTML = (".*?");\n', src, re.S)
hv = json.loads(m.group(1))
fv = re.search(r'<footer.*?</footer>', hv, re.S).group(0)
(OUT / 'ipa-visit-nf.js').write_text(src.replace(m.group(0), 'const HTML = ' + json.dumps(hv.replace(fv, '')) + ';\n').replace("'ipa-visit'", "'ipa-visit-nf'"))
hh = json.loads(re.search(r'const HTML = (".*?");\n', (OUT / 'ipa-home.js').read_text(), re.S).group(1))
fh = re.search(r'<footer.*?</footer>', hh, re.S).group(0)
(OUT / 'ipa-footer.js').write_text(src.replace(m.group(0), 'const HTML = ' + json.dumps('<div class="ipa-root">' + fh + '</div>') + ';\n').replace("'ipa-visit'", "'ipa-footer'"))
print('visit-nf/footer ok')
