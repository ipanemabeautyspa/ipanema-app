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

FAQ_NEW = json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'faq_new.json'), encoding='utf-8'))

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
    body = body.replace('A spa day with a Brazilian touch.', 'Brazilian beauty, done with care.')
    body = body.replace('Come see us.', 'Come see us!')
    body = body.replace('We started in Brazil in 2011 with brow shaping and waxing. Today our team in Dr. Phillips brings the same care to brows, lashes, waxing and hair.',
                        'We are a Brazilian beauty spa in Dr. Phillips, focused on what we do best: brows, waxing and hair. Our purpose is to make every client walk out feeling confident and cared for, with the technique, the warmth and the attention to detail of Brazilian beauty.')

    if name == 'Waxing':
        _items = [('women-legs','Legs'),('women-underarm','Underarms'),('women-arms','Arms'),('women-back','Back'),('women-full-face','Full face'),('women-lip','Lip'),('men-chest','Men · chest'),('men-legs','Men · legs')]
        _g = ('<section style="padding: 96px 0 40px"><div class="wrap"><h2 class="h-sec" style="margin: 0; text-align: center; font-size: 52px; line-height: 1.05; font-weight: 700; letter-spacing: -0.04em; color: #1f1f1f">Every area, done with care.</h2>'
              '<p style="margin: 14px 0 0; text-align: center; font-size: 19px; color: #5c5c5c">Face and body, for women and men.</p><div class="ipa-wgal">'
              + ''.join('<figure><img src="%s/img/w/wax-%s.jpg" alt="%s waxing at Ipanema Beauty &amp; Spa" loading="lazy"><figcaption>%s</figcaption></figure>' % (APP, k, t, t) for k, t in _items)
              + '</div></div></section>\n')
        _i = body.find('How often should I wax'); _j = body.rfind('<section', 0, _i)
        if _j > 0: body = body[:_j] + _g + body[_j:]
    if name == 'Main':
        body = body.replace('<section id="top" style="background: #f5f5f7; padding: 88px 0 0;', '<section id="top" style="background: #f5f5f7; padding: 64px 0 0;', 1)
        body = body.replace('<div class="wrap">', '<div class="wrap"><img src="%s/img/logo3d.png" alt="Ipanema Beauty &amp; Spa" style="display:block;margin:0 auto 26px;width:320px;max-width:68%%;height:auto;filter:drop-shadow(0 22px 34px rgba(0,0,0,.16))">' % APP, 1)
    _faq = FAQ_NEW.get(name, [])
    if _faq:
        _det = ''.join('<details style="background: #ffffff; border-radius: 18px; padding: 22px 26px"><summary style="font-size: 18px; font-weight: 600; color: #1f1f1f; cursor: pointer">%s</summary><p style="margin: 12px 0 0; font-size: 16px; line-height: 1.6; color: #5c5c5c">%s</p></details>\n' % (q, a) for q, a, _t in _faq)
        _qi = body.find('>Questions.</h2>')
        if _qi > 0:
            _last = body.rfind('</details>', 0, body.find('</section>', _qi)) + len('</details>\n')
            body = body[:_last] + _det + body[_last:]
        else:
            _sec = ('<section style="background: #f5f5f7; padding: 100px 0">\n<div class="wrap" style="max-width: 860px">\n<h2 class="h-sec" style="margin: 0; text-align: center; font-size: 52px; line-height: 1.05; font-weight: 700; letter-spacing: -0.04em; color: #1f1f1f">Questions.</h2>\n<div style="margin-top: 44px; display: flex; flex-direction: column; gap: 12px">\n' + _det + '</div>\n</div>\n</section>\n')
            _bi = body.find('<section id="book"')
            if _bi > 0: body = body[:_bi] + _sec + body[_bi:]
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


MOTION_CSS = (
 ':host{--ease-out:cubic-bezier(0.23,1,0.32,1);--ease-in-out:cubic-bezier(0.77,0,0.175,1)}'
 'h1,h2,h3{text-wrap:balance}p{text-wrap:pretty}'
 # press feedback on everything pressable
 'a[style*="border-radius: 999px"],button,.ipa-soc,.ipa-lang,.ipa-go{transition:transform 160ms var(--ease-out),background-color 150ms ease,color 150ms ease,border-color 150ms ease}'
 'a[style*="border-radius: 999px"]:active,button:active,.ipa-soc:active,.ipa-go:active{transform:scale(0.97)}'
 # tiles / cards: press + hover lift (desktop only)
 'a[style*="border-radius: 28px"],div[style*="border-radius: 24px"]{transition:transform 250ms var(--ease-out),box-shadow 250ms var(--ease-out)}'
 'a[style*="border-radius: 28px"]:active{transform:scale(0.985)}'
 'a[style*="border-radius: 28px"] img{transition:transform 600ms var(--ease-out)}'
 '@media (hover:hover) and (pointer:fine){'
 'a[style*="border-radius: 28px"]:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(0,0,0,.10)}'
 'a[style*="border-radius: 28px"]:hover img{transform:scale(1.04)}'
 'div[style*="border-radius: 24px"]:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(0,0,0,.07)}'
 'a[style*="background: #333333"]:hover{background:#1f1f1f!important}'
 'a[style*="border: 1px solid"]:hover{border-color:#333!important}'
 'a{transition:color 150ms ease}}'
 # focus ring
 'a:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid #333;outline-offset:3px;border-radius:12px}'
 # scroll reveal (only armed when JS adds .ipa-m to root)
 '.ipa-m .rv{opacity:0;transform:translateY(18px);transition:opacity 700ms var(--ease-out),transform 700ms var(--ease-out);transition-delay:var(--d,0ms)}'
 '.ipa-m .rv.in{opacity:1;transform:none}'
 '.ipa-m img.rv{transform:translateY(18px) scale(1.03)}.ipa-m img.rv.in{transform:none}'
 '.ipa-m .rv-logo{opacity:0;transform:scale(0.96);filter:blur(6px);transition:opacity 800ms var(--ease-out),transform 800ms var(--ease-out),filter 800ms var(--ease-out)}'
 '.ipa-m .rv-logo.in{opacity:1;transform:none;filter:none}'
 # install modal enter/exit
 '.ipa-modal{transition:opacity 220ms var(--ease-out)}.ipa-modal .ipa-card{transition:transform 260ms var(--ease-out),opacity 260ms var(--ease-out)}'
 '.ipa-modal:not(.open){opacity:0}.ipa-modal:not(.open) .ipa-card{opacity:0;transform:scale(0.96)}'
 '.ipa-modal.closing{transition-duration:150ms}.ipa-modal.closing .ipa-card{transition-duration:150ms}'
 '@media (prefers-reduced-motion:reduce){'
 '.ipa-m .rv,.ipa-m img.rv,.ipa-m .rv-logo{transform:none!important;filter:none!important;transition:opacity 300ms ease!important}'
 'a,button,.ipa-soc,a[style*="border-radius: 28px"],a[style*="border-radius: 28px"] img,div[style*="border-radius: 24px"],.ipa-modal .ipa-card{transform:none!important}}'
)

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
            '.ipa-wgal{margin-top:44px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.ipa-wgal figure{margin:0;position:relative;border-radius:22px;overflow:hidden;aspect-ratio:1/1;background:#f5f5f7}'
            '.ipa-wgal img{width:100%;height:100%;object-fit:cover;display:block}.ipa-wgal figcaption{position:absolute;inset-inline-start:12px;bottom:12px;background:rgba(255,255,255,.92);color:#1f1f1f;font-size:14px;font-weight:600;padding:6px 12px;border-radius:999px}'
            '@media(max-width:760px){.ipa-wgal{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}'
            '@media(max-width:600px){.h-hero{font-size:clamp(28px,calc(var(--ipa-w,390px)*0.12),52px)!important;overflow-wrap:break-word}.h-sec{font-size:clamp(24px,calc(var(--ipa-w,390px)*0.09),40px)!important;overflow-wrap:break-word}div[style*="padding: 28px 32px"][style*="space-between"]{flex-wrap:wrap;padding:24px 22px!important}.ipa-root p a{overflow-wrap:anywhere}}'
            ':host([data-narrow]) .h-hero{font-size:clamp(28px,calc(var(--ipa-w,390px)*0.12),52px)!important;overflow-wrap:break-word}:host([data-narrow]) .h-sec{font-size:clamp(24px,calc(var(--ipa-w,390px)*0.09),40px)!important;overflow-wrap:break-word}'
            ':host([data-narrow]) div:has(>.ipa-soc){flex-wrap:nowrap!important;gap:6px!important;justify-content:center}:host([data-narrow]) .ipa-soc{width:38px;height:38px;margin:0;flex:none}:host([data-narrow]) .ipa-soc svg{width:17px;height:17px}'
            ':host([data-narrow]) .ipa-root{overflow-wrap:break-word}:host([data-narrow]) h2{font-size:clamp(24px,calc(var(--ipa-w,390px)*0.092),40px)!important;overflow-wrap:break-word}:host([data-narrow]) h3{overflow-wrap:break-word}:host([data-narrow]) section,:host([data-narrow]) footer{text-align:center}:host([data-narrow]) section [style*="display: flex"]:not([style*="space-between"]),:host([data-narrow]) footer [style*="display: flex"]{justify-content:center}:host([data-narrow]) section [style*="flex-direction: column"]{align-items:center}:host([data-narrow]) section div[style*="space-between"]{text-align:start}:host([data-narrow]) section img[style*="width: 96px"],:host([data-narrow]) section svg,:host([data-narrow]) footer img{margin-left:auto;margin-right:auto}:host([data-narrow]) section > div > div > svg,:host([data-narrow]) section div[style*="border-radius: 24px"] > svg{display:block}:host([data-narrow]) section div[style*="display: grid"][style*="max-width: 380px"]{margin-left:auto;margin-right:auto;text-align:start;max-width:250px!important}:host([data-narrow]) [style*="padding: 72px 64px"]{padding:44px 22px!important}:host([data-narrow]) [style*="padding: 56px 40px"]{padding:40px 20px!important}:host([data-narrow]) [style*="padding: 36px 32px"],:host([data-narrow]) [style*="padding: 32px 32px"]{padding-left:20px!important;padding-right:20px!important}'
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
_EXTRA = {
 'Payments for services already provided are non-refundable.': {'pt':'Pagamentos por serviços já realizados não são reembolsáveis.','es':'Los pagos por servicios ya realizados no son reembolsables.','he':'תשלומים עבור שירותים שכבר ניתנו אינם ניתנים להחזר.','ar':'المدفوعات مقابل الخدمات التي تم تقديمها غير قابلة للاسترداد.'},
 'Billing errors, such as a duplicate charge, will be corrected.': {'pt':'Erros de cobrança, como uma cobrança em duplicidade, serão corrigidos.','es':'Los errores de facturación, como un cobro duplicado, serán corregidos.','he':'טעויות בחיוב, כמו חיוב כפול, יתוקנו.','ar':'سيتم تصحيح أخطاء الفوترة، مثل الخصم المكرر.'},
 'Brazilian beauty, done with care.': {'pt':'Beleza brasileira, feita com carinho.','es':'Belleza brasileña, hecha con cuidado.','he':'יופי ברזילאי, בקפידה ובאהבה.','ar':'جمال برازيلي بعناية واهتمام.'},
 'We are a Brazilian beauty spa in Dr. Phillips, focused on what we do best: brows, waxing and hair. Our purpose is to make every client walk out feeling confident and cared for, with the technique, the warmth and the attention to detail of Brazilian beauty.': {'pt':'Somos um spa de beleza brasileiro em Dr. Phillips, focado no que fazemos de melhor: sobrancelhas, depilação e cabelo. Nosso propósito é que cada cliente saia confiante e bem cuidada, com a técnica, o carinho e a atenção aos detalhes da beleza brasileira.','es':'Somos un spa de belleza brasileño en Dr. Phillips, enfocado en lo que mejor hacemos: cejas, depilación y cabello. Nuestro propósito es que cada clienta salga segura y bien cuidada, con la técnica, la calidez y la atención al detalle de la belleza brasileña.','he':'אנחנו ספא יופי ברזילאי ב-Dr. Phillips, שמתמקד במה שאנחנו עושים הכי טוב: גבות, שעווה ושיער. המטרה שלנו היא שכל לקוחה תצא בתחושת ביטחון ותשומת לב, עם הטכניקה, החום והדיוק של היופי הברזילאי.','ar':'نحن سبا تجميل برازيلي في دكتور فيليبس، نركّز على ما نتقنه: الحواجب وإزالة الشعر بالشمع والشعر. هدفنا أن تخرج كل عميلة واثقة ومُعتنى بها، بتقنية الجمال البرازيلي ودفئه واهتمامه بالتفاصيل.'},
 'Every area, done with care.': {'pt':'Cada área, com todo o cuidado.','es':'Cada zona, con todo el cuidado.','he':'כל אזור, בקפידה.','ar':'كل منطقة، بعناية فائقة.'},
 'Face and body, for women and men.': {'pt':'Rosto e corpo, para mulheres e homens.','es':'Rostro y cuerpo, para mujeres y hombres.','he':'פנים וגוף, לנשים ולגברים.','ar':'الوجه والجسم، للنساء والرجال.'},
 'Legs': {'pt':'Pernas','es':'Piernas','he':'רגליים','ar':'الساقان'},
 'Underarms': {'pt':'Axilas','es':'Axilas','he':'בית שחי','ar':'الإبطان'},
 'Arms': {'pt':'Braços','es':'Brazos','he':'ידיים','ar':'الذراعان'},
 'Back': {'pt':'Costas','es':'Espalda','he':'גב','ar':'الظهر'},
 'Full face': {'pt':'Rosto inteiro','es':'Rostro completo','he':'פנים מלאות','ar':'الوجه كاملاً'},
 'Lip': {'pt':'Buço','es':'Labio superior','he':'שפם','ar':'الشفة العليا'},
 'Men · chest': {'pt':'Homens · peito','es':'Hombres · pecho','he':'גברים · חזה','ar':'رجال · الصدر'},
 'Men · legs': {'pt':'Homens · pernas','es':'Hombres · piernas','he':'גברים · רגליים','ar':'رجال · الساقان'},
}
_lsrc = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legal_src.json')))
for _l in ['pt', 'es', 'he', 'ar']:
    _t = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legal_%s.json' % _l)))
    assert len(_t) == len(_lsrc)
    for _a, _b in zip(_lsrc, _t):
        if _b and _b != _a: _I.setdefault(_l, {})[_a] = _b
for _l in ['pt', 'es', 'he', 'ar']:
    _v6 = _I.get(_l, {}).get('6. Right to Refuse Refunds')
    if _v6: _I[_l]['5. Right to Refuse Refunds'] = _v6.replace('6', '5', 1).replace('٦', '٥', 1)
for _pg in FAQ_NEW.values():
    for _q, _a, _t in _pg:
        _EXTRA[_q] = {l: v[0] for l, v in _t.items()}
        _EXTRA[_a] = {l: v[1] for l, v in _t.items()}
for _k, _v in _EXTRA.items():
    for _l, _t in _v.items():
        _I.setdefault(_l, {})[_k] = _t
I18N_JSON = json.dumps(_I, ensure_ascii=False)


def _narrowize(css):
    """Duplicate @media(max-width>=600) rules under :host([data-narrow]) so they apply when the
    host is narrow even if the page viewport is wide (Wix mobile preview)."""
    out = []
    for m in re.finditer(r'@media\s*\(max-width:\s*(\d+)px\)\s*\{', css):
        if int(m.group(1)) < 600: continue
        i = m.end(); depth = 1; j = i
        while j < len(css) and depth:
            if css[j] == '{': depth += 1
            elif css[j] == '}': depth -= 1
            j += 1
        body = css[i:j-1]
        for r in re.finditer(r'([^{}]+)\{([^{}]*)\}', body):
            sels = ','.join(':host([data-narrow]) ' + x.strip() for x in r.group(1).split(',') if x.strip())
            out.append(sels + '{' + r.group(2) + '}')
    return css + '\n' + ''.join(out)

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
    const setW = () => { let m = Infinity, p = this.parentElement; while (p && p !== document.documentElement) { const cw = p.clientWidth; if (cw > 0 && cw < m) m = cw; p = p.parentElement; } if (m < Infinity && Math.abs(this.offsetWidth - m) > 1) { this.style.maxWidth = m + 'px'; this.style.width = m + 'px'; } const w = Math.min(this.clientWidth || m, m); if (w && w < Infinity) { this.style.setProperty('--ipa-w', w + 'px'); this.toggleAttribute('data-narrow', w < 600); } }; setW(); try { new ResizeObserver(setW).observe(this); } catch (e) { window.addEventListener('resize', setW); }
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
    (() => {
      const root = r.querySelector('.ipa-root'); if (!root || !('IntersectionObserver' in window)) return;
      const sel = 'section h1, section h2, section > .wrap > p, section > div > p, section .tiles > *, section .cards > *, section .two > *, section .split > *, section .three > *, section .wrap > div > div[style*="border-radius"], section img, section iframe, section [style*="display: flex"] > a, footer > .wrap > *';
      const all = Array.prototype.slice.call(root.querySelectorAll(sel));
      const set = new Set();
      all.forEach(el => { let p = el.parentElement, nested = false; while (p && p !== root) { if (set.has(p)) { nested = true; break; } p = p.parentElement; } if (!nested) set.add(el); });
      const logo = root.querySelector('section img[src*="logo3d"]');
      set.forEach(el => el.classList.add(el === logo ? 'rv-logo' : 'rv'));
      const kids = new Map();
      set.forEach(el => { const k = el.parentElement; const n = kids.get(k) || 0; kids.set(k, n + 1); el.style.setProperty('--d', Math.min(n, 5) * 70 + 'ms'); });
      root.classList.add('ipa-m');
      const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8px 0px', threshold: 0.08 });
      set.forEach(el => io.observe(el));
      setTimeout(() => set.forEach(el => { const b = el.getBoundingClientRect(); if (b.top < innerHeight && b.bottom > 0) el.classList.add('in'); }), 1200);
    })();
    r.querySelectorAll('a[href^="#"]').forEach(a => { if (a.hasAttribute('data-install')) return; a.addEventListener('click', e => { const id = a.getAttribute('href').slice(1); const el = id && r.getElementById(id); if (el) { e.preventDefault(); el.scrollIntoView({behavior:'smooth'}); } else if (id==='top') { e.preventDefault(); this.scrollIntoView({behavior:'smooth'}); } }); });
    if (m) {
      const openM = () => { m.classList.remove('closing', 'open'); m.hidden = false; requestAnimationFrame(() => requestAnimationFrame(() => m.classList.add('open'))); };
      const closeM = () => { m.classList.add('closing'); m.classList.remove('open'); setTimeout(() => { m.hidden = true; m.classList.remove('closing'); }, 160); };
      r.querySelectorAll('[data-install]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openM(); }));
      m.querySelector('.ipa-x').addEventListener('click', closeM);
      m.addEventListener('click', e => { if (e.target === m) closeM(); });
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
    css = (':host{display:block;width:100%;max-width:100vw;overflow-x:clip}.ipa-root{max-width:100%;overflow-x:clip}*{box-sizing:border-box}' + style.replace('body{', '.ipa-root{') +
           '\nimg{max-width:100%}a{color:#4d4d4d;text-decoration:none}\n' + MODAL_CSS + LANG_CSS)
    html_ = '<div class="ipa-root">' + LANGBAR + body + '</div>'
    modal = INSTALL
    css = _narrowize(css) + MOTION_CSS
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

# ---------- legal pages ----------
LEGAL = {
 'ipa-refund': ('Refund and Cancellation', 'At Ipanema Beauty & Spa, we value your time and ours. This policy explains how cancellations, reschedules, and refunds are handled.', [
   ('1. Cancellations & Reschedules', ['Plans change, and we understand. We kindly ask for at least 24 hours’ notice if you need to cancel or reschedule, so we can offer your time to another client.', 'Cancellations or reschedules with less than 24 hours’ notice may be subject to a fee. Microblading follows its own deposit policy (see section 2).']),
   ('2. Microblading Deposit', ['Microblading is the only service that requires a deposit. A $63.75 deposit is paid at booking, online through our website or through Square. It is part of the $212.50 session price, and the remaining $148.75 is paid at the salon.', 'The deposit is never refunded in cash.', 'If you cancel or reschedule at least 48 hours in advance, the full deposit is credited to your next appointment.', 'Cancellations with less than 48 hours’ notice, no-shows, or arriving more than 15 minutes late forfeit the deposit.', 'This policy applies equally to every client.']),
   ('3. No-Shows', ['If you can’t make it, please let us know as early as possible by phone, text or WhatsApp.', 'No-shows may be subject to a fee, and repeated no-shows may result in limited online booking in the future.']),
   ('4. Refunds', ['Payments for services already provided are non-refundable.', 'Billing errors, such as a duplicate charge, will be corrected.']),
   ('5. Right to Refuse Refunds', ['We reserve the right to decline partial or full refunds if the request falls outside of this policy.'])]),
 'ipa-terms': ('Terms and Conditions', 'Welcome to Ipanema Beauty & Spa. By accessing or using our website and booking our services, you agree to the following terms and conditions.', [
   ('1. Services', ['All services listed on our website are subject to availability.', 'Prices may vary depending on service type and duration.', 'We reserve the right to update or change services and pricing at any time.']),
   ('2. Appointments', ['Appointments can be booked online, by phone, or in person.', 'Please arrive on time for your scheduled appointment. Late arrivals may result in reduced service time.', 'If you need to cancel or reschedule, please give us at least 24 hours’ notice (48 hours for Microblading). Late cancellations and no-shows may be subject to a fee. Microblading requires a deposit, described below.']),
   ('3. Payments', ['Payments are due at the time of service.', 'We accept cash, debit and credit cards, and Zelle.', 'Microblading is the only exception: a $63.75 non-refundable deposit is paid at booking (online or through Square) and counts toward the $212.50 session price. With at least 48 hours’ notice it is credited to your next appointment; see our Refund and Cancellation policy.']),
   ('4. Refunds and Cancellations', ['Payments for services already provided are non-refundable.', 'Billing errors, such as a duplicate charge, will be corrected.']),
   ('5. Website Use', ['The content on this website (text, images, design, logo) is owned by Ipanema Beauty & Spa and may not be copied or used without permission.', 'You agree not to use this website for any unlawful or harmful activity.']),
   ('6. Limitation of Liability', ['While we strive to provide the best care and services, Ipanema Beauty & Spa is not responsible for any indirect damages, allergic reactions, or outcomes beyond normal professional standards.', 'Please inform your esthetician or stylist of any allergies, sensitivities, or health conditions before your service.']),
   ('7. Changes to These Terms', ['We may update these Terms & Conditions at any time. Changes will be effective immediately when posted on this page.'])]),
 'ipa-privacy': ('Privacy Policy', 'At Ipanema Beauty & Spa, your privacy is very important to us. This Privacy Policy explains how we collect, use, and protect your personal information when you visit our website and book our services.', [
   ('1. Information We Collect', ['When you use our website or contact us, we may collect the following information:', '• Name, email address, and phone number', '• Billing information (when making a payment)', '• Booking details (service type, date, time)', '• Messages or inquiries you send us through forms or email']),
   ('2. How We Use Your Information', ['We use your information to:', '• Confirm and manage your appointments', '• Communicate with you about your booking or inquiries', '• Improve our services and website', '• Send promotional offers or updates (only if you agree)']),
   ('3. Sharing of Information', ['We do not sell or trade your personal information.', 'Your information may only be shared with:', '• Payment processors (to complete transactions securely)', '• Service providers that help us operate the website (always under confidentiality)', '• When required by law']),
   ('4. Data Security', ['We take reasonable measures to protect your personal information from unauthorized access, disclosure, or misuse.']),
   ('5. Cookies and Tracking', ['Our website may use cookies to improve user experience, track visits, and help us understand how the website is used. You can disable cookies in your browser settings at any time.']),
   ('6. Your Rights', ['You have the right to:', '• Request access to your personal data', '• Ask us to correct or delete your data', '• Opt out of receiving promotional emails', 'To exercise these rights, contact us at <a href="mailto:ipanemabeautyandspa@gmail.com" style="color:#1f1f1f;font-weight:600">ipanemabeautyandspa@gmail.com</a>.'])]),
}
_hj = json.loads(re.search(r'const HTML = (".*?");\n', (OUT / 'ipa-home.js').read_text(encoding='utf-8'), re.S).group(1))
_foot = re.search(r'<footer.*?</footer>', _hj, re.S).group(0)
_home_css = json.loads(re.search(r'const CSS = (".*?");\n', (OUT / 'ipa-home.js').read_text(encoding='utf-8'), re.S).group(1))
for tag, (title, intro, secs) in LEGAL.items():
    cards = ''.join('<div style="background:#f5f5f7;border-radius:24px;padding:30px 30px 22px;margin-top:16px"><h2 style="margin:0 0 12px;font-size:21px;font-weight:700;letter-spacing:-0.01em;color:#1f1f1f">%s</h2>%s</div>' % (h, ''.join('<p style="margin:0 0 10px;font-size:17px;line-height:1.6;color:#3d3d3d">%s</p>' % p for p in ps)) for h, ps in secs)
    page = ('<div class="ipa-root">' + LANGBAR + '<section style="background:#ffffff;padding:72px 0 96px"><div class="wrap" style="max-width:820px">'
            '<p style="margin:0;font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#6b6b6b">Policies</p>'
            '<h1 style="margin:14px 0 0;font-size:clamp(40px,7vw,64px);line-height:1.05;font-weight:700;letter-spacing:-0.04em;color:#1f1f1f">%s</h1>'
            '<p style="margin:14px 0 0;font-size:15px;color:#8a8a8a">Last updated: 10/20/2026</p>'
            '<p style="margin:26px 0 12px;font-size:20px;line-height:1.55;color:#4d4d4d">%s</p>%s'
            '<p style="margin:34px 0 0;font-size:17px"><a href="%s/privacy-policy" target="_top" style="color:#1f1f1f;font-weight:600;margin-inline-end:22px">Privacy</a><a href="%s/copy-of-privacy-policy" target="_top" style="color:#1f1f1f;font-weight:600;margin-inline-end:22px">Terms</a><a href="%s/copy-of-terms-and-conditions" target="_top" style="color:#1f1f1f;font-weight:600">Refund &amp; Cancellation</a></p>'
            '</div></section>%s</div>') % (title, intro, cards, SITE, SITE, SITE, _foot)
    (OUT / f'{tag}.js').write_text(encoding='utf-8', data=TPL % {'tag': tag, 'css': json.dumps(_home_css + '.ipa-root{font-family:Inter,-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;color:#333}@media(max-width:600px){.ipa-root section div[style*="border-radius:24px"]{padding:24px 20px 16px!important}}:host([data-narrow]) section{text-align:start!important}:host([data-narrow]) section h1,:host([data-narrow]) section > div > p:first-child{text-align:start}'), 'html': json.dumps(page), 'modal': json.dumps(''), 'i18n': I18N_JSON})
    (OUT / f'{tag}.html').write_text(f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{tag}</title><body style="margin:0"><script src="{tag}.js"></script><{tag}></{tag}></body>')
print('legal ok')
