import json,sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(s,name,fn,ascii_):
    i=s.find('\nconst %s = '%name); j=s.find('\n',i+5)
    v=json.loads(s[i+len('\nconst %s = '%name):j].rstrip(';'))
    v=fn(v)
    return s[:i]+'\nconst %s = '%name+json.dumps(v,ensure_ascii=ascii_)+';'+s[j:]
tile='''<a id="nails" href="https://www.ipanemabeautyandspa.com/book?cat=nails" style="background: #ebe7d2; border-radius: 28px; overflow: hidden; display: flex; flex-direction: column; text-align: center; min-height: 620px; color: #333333" target="_top">
<div style="padding: 56px 40px 0">
<h2 style="margin: 0; font-size: 44px; font-weight: 700; letter-spacing: -0.035em; color: #1f1f1f">Nails</h2>
<p style="margin: 10px 0 0; font-size: 19px; color: #4d4d4d">Manicure, pedicure, gel and builder gel.</p>
<p style="margin: 18px 0 0; font-size: 17px; font-weight: 600; color: #333333">Book now ›</p>
</div>
<img loading="lazy" decoding="async" src="https://app.ipanemabeautyandspa.com/img/w/nails-cloud.webp" alt="Milky builder gel manicure at Ipanema Beauty &amp; Spa" style="margin-top: auto; width: 100%; height: 360px; object-fit: cover; object-position: center 55%; display: block">
</a>
'''
def fh(html):
    assert 'id="nails"' not in html
    a=html.find('<a id="hair"'); b=html.find('</a>\n',a)+5; assert a>0
    return html[:b]+tile+html[b:]
tr={'pt':('Unhas','Manicure, pedicure, gel e builder gel.'),'es':('Uñas','Manicura, pedicura, gel y builder gel.'),'he':('ציפורניים',"מניקור, פדיקור, ג'ל ובילדר ג'ל."),'ar':('الأظافر','مانيكير وباديكير وجل وبيلدر جل.')}
def fi(d):
    for lg,(x,y) in tr.items():
        d[lg]['Nails']=x; d[lg]['Manicure, pedicure, gel and builder gel.']=y
    return d
s=rep(s,'HTML',fh,True); s=rep(s,'I18N',fi,False)
open(dst,'w',encoding='utf-8').write(s)
