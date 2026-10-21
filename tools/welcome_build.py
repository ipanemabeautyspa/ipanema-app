import json, re, os, pathlib
OUT = pathlib.Path('/home/claude/ipanema-app/site')
APP = 'https://app.ipanemabeautyandspa.com'
T = {
 'en': {'eyebrow':'Welcome to Ipanema','title':'Take 10% off your first visit.','sub':'Join our list and we’ll email you your welcome code.','name':'Name','email':'Email','phone':'Mobile phone','btn':'Get my 10% off','fine':'New clients only. One-time use. Not combinable with other offers.','no':'No thanks','ok_t':'Check your email.','ok_s':'Your 10% welcome code is on its way. Show it at the front desk on your first visit.','back_t':'Welcome back!','back_s':'You’re already part of the Ipanema family, so this first-visit offer isn’t available. Ask about our birthday 10% and Give $10, Get $10.','err':'Something went wrong. Please try again or message us on WhatsApp.','req':'Please enter your name, a valid email and your mobile phone.','book':'Book now'},
 'pt': {'eyebrow':'Bem-vinda à Ipanema','title':'Ganhe 10% na sua primeira visita.','sub':'Cadastre-se e enviaremos seu código de boas-vindas por e-mail.','name':'Nome','email':'E-mail','phone':'Celular','btn':'Quero meus 10%','fine':'Só para clientes novas. Uso único. Não soma com outras ofertas.','no':'Agora não','ok_t':'Confira seu e-mail.','ok_s':'Seu código de 10% está a caminho. Mostre na recepção na sua primeira visita.','back_t':'Que bom ver você de novo!','back_s':'Você já faz parte da família Ipanema, então esta oferta de primeira visita não se aplica. Pergunte sobre os 10% de aniversário e a indicação Ganhe $10, Dê $10.','err':'Algo deu errado. Tente de novo ou fale com a gente no WhatsApp.','req':'Preencha seu nome, um e-mail válido e seu celular.','book':'Agendar'},
 'es': {'eyebrow':'Bienvenida a Ipanema','title':'Obtén 10% en tu primera visita.','sub':'Únete a nuestra lista y te enviaremos tu código de bienvenida por correo.','name':'Nombre','email':'Correo electrónico','phone':'Celular','btn':'Quiero mi 10%','fine':'Solo clientas nuevas. Un solo uso. No se combina con otras ofertas.','no':'No, gracias','ok_t':'Revisa tu correo.','ok_s':'Tu código de 10% va en camino. Muéstralo en recepción en tu primera visita.','back_t':'¡Qué bueno verte otra vez!','back_s':'Ya eres parte de la familia Ipanema, así que esta oferta de primera visita no aplica. Pregunta por el 10% de cumpleaños y Da $10, Recibe $10.','err':'Algo salió mal. Inténtalo de nuevo o escríbenos por WhatsApp.','req':'Escribe tu nombre, un correo válido y tu celular.','book':'Reservar'},
 'he': {'eyebrow':'ברוכה הבאה לאיפנמה','title':'10% הנחה בביקור הראשון שלך.','sub':'הצטרפי לרשימה שלנו ונשלח לך את קוד ההטבה במייל.','name':'שם','email':'אימייל','phone':'טלפון נייד','btn':'אני רוצה 10% הנחה','fine':'ללקוחות חדשות בלבד. שימוש חד־פעמי. לא ניתן לשלב עם מבצעים אחרים.','no':'לא תודה','ok_t':'בדקי את המייל שלך.','ok_s':'קוד ההנחה של 10% בדרך אלייך. הציגי אותו בקבלה בביקור הראשון.','back_t':'שמחות לראות אותך שוב!','back_s':'את כבר חלק ממשפחת איפנמה, ולכן הטבת הביקור הראשון אינה זמינה. שאלי על 10% ביום ההולדת ועל תני $10, קבלי $10.','err':'משהו השתבש. נסי שוב או כתבי לנו בוואטסאפ.','req':'נא למלא שם, אימייל תקין וטלפון נייד.','book':'קביעת תור'},
 'ar': {'eyebrow':'مرحبًا بكم في إيبانيما','title':'خصم 10% على زيارتك الأولى.','sub':'انضم إلى قائمتنا وسنرسل لك رمز الترحيب عبر البريد الإلكتروني.','name':'الاسم','email':'البريد الإلكتروني','phone':'رقم الجوال','btn':'أريد خصم 10%','fine':'للعملاء الجدد فقط. استخدام لمرة واحدة. لا يُجمع مع عروض أخرى.','no':'لا، شكرًا','ok_t':'تحقق من بريدك الإلكتروني.','ok_s':'رمز خصم 10% في الطريق إليك. اعرضه في الاستقبال في زيارتك الأولى.','back_t':'أهلًا بعودتك!','back_s':'أنت بالفعل من عائلة إيبانيما، لذا لا ينطبق عرض الزيارة الأولى. اسأل عن خصم 10% في شهر ميلادك وعرض أعطِ $10 واحصل على $10.','err':'حدث خطأ ما. حاول مرة أخرى أو راسلنا عبر واتساب.','req':'يرجى إدخال الاسم وبريد إلكتروني صحيح ورقم الجوال.','book':'احجز الآن'},
}
CSS = ''':host{display:block;width:100%;height:100%}*{box-sizing:border-box}
.w{font-family:Inter,-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,"Noto Sans Hebrew","Noto Sans Arabic",sans-serif;-webkit-font-smoothing:antialiased;color:#1f1f1f;background:#fff;border-radius:28px;overflow:auto;display:grid;grid-template-columns:42% 58%;width:100%;height:100%;min-height:440px;position:relative}
.ph{background:#e9e3cf url(APPURL/img/w/brow-076.jpg) center/cover no-repeat}
.bd{padding:20px 36px 14px;display:flex;flex-direction:column;justify-content:center}
.ey{margin:0;font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#6b6b6b}
h2{margin:8px 0 0;font-size:31px;line-height:1.06;font-weight:700;letter-spacing:-.03em}
.sub{margin:12px 0 0;font-size:16px;line-height:1.5;color:#4d4d4d}
form{margin-top:16px;display:flex;flex-direction:column;gap:9px}
input{width:100%%;height:46px;border:1px solid #d6d6d6;border-radius:14px;padding:0 16px;font:inherit;font-size:16px;color:#1f1f1f;background:#fafafa;outline:none}
input:focus{border-color:#333;background:#fff}
button.go{height:50px;border:0;border-radius:999px;background:#333;color:#fff;font:inherit;font-size:16px;font-weight:600;cursor:pointer;margin-top:4px}
button.go[disabled]{opacity:.6}
.fine{margin:10px 0 0;font-size:11.5px;line-height:1.45;color:#8a8a8a}
.msg{margin:10px 0 0;font-size:14px;color:#b3261e;min-height:0}
.x{position:absolute;top:14px;inset-inline-end:14px;width:40px;height:40px;border-radius:50%%;border:0;background:rgba(255,255,255,.9);font-size:20px;color:#4d4d4d;cursor:pointer;z-index:2}
.no{margin-top:8px;background:none;border:0;color:#6b6b6b;font:inherit;font-size:14px;cursor:pointer;text-decoration:underline}
.done h2{font-size:30px}.done a{display:inline-flex;align-items:center;justify-content:center;height:50px;padding:0 28px;border-radius:999px;background:#333;color:#fff;text-decoration:none;font-weight:600;margin-top:20px}
@media(max-width:640px){.w{grid-template-columns:1fr;grid-template-rows:150px auto;border-radius:22px}.bd{padding:24px 22px 20px}h2{font-size:27px}}
:host{--ease-out:cubic-bezier(0.23,1,0.32,1)}
:host([data-narrow]) .w{grid-template-columns:1fr;grid-template-rows:118px auto;border-radius:22px}
:host([data-narrow]) .bd{padding:18px 20px 14px;justify-content:flex-start}
:host([data-narrow]) h2{font-size:25px}:host([data-narrow]) .sub{font-size:15px;margin-top:8px}:host([data-narrow]) form{margin-top:14px;gap:8px}
:host([data-narrow]) input{height:44px}:host([data-narrow]) button.go{height:48px}:host([data-narrow]) .fine{margin-top:8px}
h2{text-wrap:balance}
.w{transition:opacity 260ms var(--ease-out),transform 260ms var(--ease-out)}
.w.pre{opacity:0;transform:scale(0.96)}
.w.out{opacity:0;transform:scale(0.97);transition-duration:150ms}
.bd > *{animation:wi 520ms var(--ease-out) both}
.bd > *:nth-child(2){animation-delay:60ms}.bd > *:nth-child(3){animation-delay:120ms}.bd > *:nth-child(4){animation-delay:180ms}.bd > *:nth-child(5){animation-delay:240ms}.bd > *:nth-child(n+6){animation-delay:280ms}
.ph{animation:wf 600ms var(--ease-out) both}
@keyframes wi{from{opacity:0;transform:translateY(10px)}}
@keyframes wf{from{opacity:0}}
button.go,.x,.no,.done a{transition:transform 160ms var(--ease-out),background-color 150ms ease,color 150ms ease}
button.go:active,.x:active,.done a:active{transform:scale(0.97)}
@media (hover:hover) and (pointer:fine){button.go:hover,.done a:hover{background:#1f1f1f}.x:hover{background:#fff}.no:hover{color:#1f1f1f}}
input{transition:border-color 150ms ease,background-color 150ms ease,box-shadow 150ms ease}
input:focus{box-shadow:0 0 0 4px rgba(51,51,51,.08)}
button:focus-visible,a:focus-visible{outline:2px solid #333;outline-offset:3px}
.msg.shake{animation:sh 320ms var(--ease-out)}
@keyframes sh{20%{transform:translateX(-6px)}50%{transform:translateX(5px)}80%{transform:translateX(-2px)}}
@media (prefers-reduced-motion:reduce){.w,.w.pre,.w.out{transform:none}.bd > *,.msg.shake{animation:wf 250ms ease both}button.go:active,.x:active,.done a:active{transform:none}}
'''.replace('APPURL', APP).replace('%%','%')
JS = r'''/* Ipanema Beauty & Spa — ipa-welcome (generated) */
(function(){
if (customElements.get('ipa-welcome')) return;
const T = %(t)s; const CSS = %(css)s;
const LS=['en','pt','es','he','ar'];
class E extends HTMLElement {
  static get observedAttributes(){ return ['result']; }
  connectedCallback(){
    if (this._r) return; this._r = 1;
    if (!document.getElementById('ipa-inter')) { const l=document.createElement('link'); l.id='ipa-inter'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'; document.head.appendChild(l); }
    let lang=''; try{ lang=new URLSearchParams(location.search).get('lang')||localStorage.getItem('ipa-site-lang')||''; }catch(e){}
    if (LS.indexOf(lang)<0){ const b=(navigator.language||'en').slice(0,2).toLowerCase(); lang=LS.indexOf(b)>=0?b:'en'; }
    this.t = T[lang]; this.lang = lang;
    this.root = this.attachShadow({mode:'open'});
    const setN = () => { const w = this.clientWidth; if (w) this.toggleAttribute('data-narrow', w < 560); }; setN(); try { new ResizeObserver(setN).observe(this); } catch (e) {}
    this.render();
    const w0 = this.root.querySelector('.w'); w0.classList.add('pre'); requestAnimationFrame(() => requestAnimationFrame(() => w0.classList.remove('pre')));
  }
  render(state){
    const t=this.t, rtl=(this.lang==='he'||this.lang==='ar');
    let body;
    if (state==='new' || state==='returning') {
      const ok = state==='new';
      body = '<div class="bd done"><h2>'+(ok?t.ok_t:t.back_t)+'</h2><p class="sub">'+(ok?t.ok_s:t.back_s)+'</p><div><a href="https://www.ipanemabeautyandspa.com/services-5" target="_top">'+t.book+'</a></div></div>';
    } else {
      body = '<div class="bd"><p class="ey">'+t.eyebrow+'</p><h2>'+t.title+'</h2><p class="sub">'+t.sub+'</p>'+
        '<form novalidate><input name="name" autocomplete="name" placeholder="'+t.name+'" required><input name="email" type="email" autocomplete="email" placeholder="'+t.email+'" required><input name="phone" type="tel" autocomplete="tel" placeholder="'+t.phone+'" required>'+
        '<button class="go" type="submit">'+t.btn+'</button></form><p class="msg" role="alert"></p><p class="fine">'+t.fine+'</p><button class="no" type="button">'+t.no+'</button></div>';
    }
    this.root.innerHTML = '<style>'+CSS+'</style><div class="w" dir="'+(rtl?'rtl':'ltr')+'" lang="'+this.lang+'"><button class="x" aria-label="Close">×</button><div class="ph" role="img" aria-label="Brows at Ipanema Beauty & Spa"></div>'+body+'</div>';
    const close=()=>{ const w=this.root.querySelector('.w'); if(w) w.classList.add('out'); setTimeout(()=>this.dispatchEvent(new CustomEvent('ipa-close',{bubbles:true,composed:true})),150); };
    this.root.querySelector('.x').onclick=close; const no=this.root.querySelector('.no'); if(no) no.onclick=close;
    const f=this.root.querySelector('form');
    if (f) f.onsubmit=(e)=>{ e.preventDefault();
      const d={name:f.name.value.trim(), email:f.email.value.trim().toLowerCase(), phone:f.phone.value.trim(), lang:this.lang};
      const msg=this.root.querySelector('.msg');
      if(!d.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email) || d.phone.replace(/\D/g,'').length<10){ msg.textContent=t.req; msg.classList.remove('shake'); void msg.offsetWidth; msg.classList.add('shake'); return; }
      msg.textContent=''; const b=f.querySelector('button'); b.disabled=true; b.textContent='…';
      this.dispatchEvent(new CustomEvent('ipa-submit',{detail:d,bubbles:true,composed:true}));
      clearTimeout(this._to); this._to=setTimeout(()=>{ if(!this._done){ msg.textContent=t.err; b.disabled=false; b.textContent=t.btn; } }, 15000);
    };
  }
  attributeChangedCallback(n,o,v){
    if(n!=='result'||!v||!this.root) return;
    let r={}; try{ r=JSON.parse(v); }catch(e){ r={status:v}; }
    this._done=true; clearTimeout(this._to);
    if(r.status==='new'||r.status==='returning') this.render(r.status);
    else { const m=this.root.querySelector('.msg'); if(m){ m.textContent=this.t.err; const b=this.root.querySelector('button.go'); if(b){b.disabled=false;b.textContent=this.t.btn;} } this._done=false; }
  }
}
customElements.define('ipa-welcome', E);
})();
'''
(OUT/'ipa-welcome.js').write_text(JS % {'t': json.dumps(T, ensure_ascii=False), 'css': json.dumps(CSS)}, encoding='utf-8')
(OUT/'ipa-welcome.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>ipa-welcome</title><body style="margin:0;background:#666;padding:30px"><div style="max-width:780px;height:470px;margin:auto"><script src="ipa-welcome.js"></script><ipa-welcome></ipa-welcome></div></body>')
print('ok')
