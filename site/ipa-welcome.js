/* Ipanema Beauty & Spa — ipa-welcome (generated) */
(function(){
if (customElements.get('ipa-welcome')) return;
const T = {"en": {"eyebrow": "Welcome to Ipanema", "title": "Take 10% off your first visit.", "sub": "Join our list and we’ll email you your welcome code.", "name": "Name", "email": "Email", "phone": "Mobile phone", "btn": "Get my 10% off", "fine": "New clients only. One-time use. Not combinable with other offers.", "no": "No thanks", "ok_t": "Check your email.", "ok_s": "Your 10% welcome code is on its way. Show it at the front desk on your first visit.", "back_t": "Welcome back!", "back_s": "You’re already part of the Ipanema family, so this first-visit offer isn’t available. Ask about our birthday 10% and Give $10, Get $10.", "err": "Something went wrong. Please try again or message us on WhatsApp.", "req": "Please enter your name, a valid email and your mobile phone.", "book": "Book now"}, "pt": {"eyebrow": "Bem-vinda à Ipanema", "title": "Ganhe 10% na sua primeira visita.", "sub": "Cadastre-se e enviaremos seu código de boas-vindas por e-mail.", "name": "Nome", "email": "E-mail", "phone": "Celular", "btn": "Quero meus 10%", "fine": "Só para clientes novas. Uso único. Não soma com outras ofertas.", "no": "Agora não", "ok_t": "Confira seu e-mail.", "ok_s": "Seu código de 10% está a caminho. Mostre na recepção na sua primeira visita.", "back_t": "Que bom ver você de novo!", "back_s": "Você já faz parte da família Ipanema, então esta oferta de primeira visita não se aplica. Pergunte sobre os 10% de aniversário e a indicação Ganhe $10, Dê $10.", "err": "Algo deu errado. Tente de novo ou fale com a gente no WhatsApp.", "req": "Preencha seu nome, um e-mail válido e seu celular.", "book": "Agendar"}, "es": {"eyebrow": "Bienvenida a Ipanema", "title": "Obtén 10% en tu primera visita.", "sub": "Únete a nuestra lista y te enviaremos tu código de bienvenida por correo.", "name": "Nombre", "email": "Correo electrónico", "phone": "Celular", "btn": "Quiero mi 10%", "fine": "Solo clientas nuevas. Un solo uso. No se combina con otras ofertas.", "no": "No, gracias", "ok_t": "Revisa tu correo.", "ok_s": "Tu código de 10% va en camino. Muéstralo en recepción en tu primera visita.", "back_t": "¡Qué bueno verte otra vez!", "back_s": "Ya eres parte de la familia Ipanema, así que esta oferta de primera visita no aplica. Pregunta por el 10% de cumpleaños y Da $10, Recibe $10.", "err": "Algo salió mal. Inténtalo de nuevo o escríbenos por WhatsApp.", "req": "Escribe tu nombre, un correo válido y tu celular.", "book": "Reservar"}, "he": {"eyebrow": "ברוכה הבאה לאיפנמה", "title": "10% הנחה בביקור הראשון שלך.", "sub": "הצטרפי לרשימה שלנו ונשלח לך את קוד ההטבה במייל.", "name": "שם", "email": "אימייל", "phone": "טלפון נייד", "btn": "אני רוצה 10% הנחה", "fine": "ללקוחות חדשות בלבד. שימוש חד־פעמי. לא ניתן לשלב עם מבצעים אחרים.", "no": "לא תודה", "ok_t": "בדקי את המייל שלך.", "ok_s": "קוד ההנחה של 10% בדרך אלייך. הציגי אותו בקבלה בביקור הראשון.", "back_t": "שמחות לראות אותך שוב!", "back_s": "את כבר חלק ממשפחת איפנמה, ולכן הטבת הביקור הראשון אינה זמינה. שאלי על 10% ביום ההולדת ועל תני $10, קבלי $10.", "err": "משהו השתבש. נסי שוב או כתבי לנו בוואטסאפ.", "req": "נא למלא שם, אימייל תקין וטלפון נייד.", "book": "קביעת תור"}, "ar": {"eyebrow": "مرحبًا بكم في إيبانيما", "title": "خصم 10% على زيارتك الأولى.", "sub": "انضم إلى قائمتنا وسنرسل لك رمز الترحيب عبر البريد الإلكتروني.", "name": "الاسم", "email": "البريد الإلكتروني", "phone": "رقم الجوال", "btn": "أريد خصم 10%", "fine": "للعملاء الجدد فقط. استخدام لمرة واحدة. لا يُجمع مع عروض أخرى.", "no": "لا، شكرًا", "ok_t": "تحقق من بريدك الإلكتروني.", "ok_s": "رمز خصم 10% في الطريق إليك. اعرضه في الاستقبال في زيارتك الأولى.", "back_t": "أهلًا بعودتك!", "back_s": "أنت بالفعل من عائلة إيبانيما، لذا لا ينطبق عرض الزيارة الأولى. اسأل عن خصم 10% في شهر ميلادك وعرض أعطِ $10 واحصل على $10.", "err": "حدث خطأ ما. حاول مرة أخرى أو راسلنا عبر واتساب.", "req": "يرجى إدخال الاسم وبريد إلكتروني صحيح ورقم الجوال.", "book": "احجز الآن"}}; const CSS = ":host{display:block;width:100%;height:100%}*{box-sizing:border-box}\n.w{font-family:Inter,-apple-system,BlinkMacSystemFont,\"Helvetica Neue\",Arial,\"Noto Sans Hebrew\",\"Noto Sans Arabic\",sans-serif;-webkit-font-smoothing:antialiased;color:#1f1f1f;background:#fff;border-radius:28px;overflow:auto;display:grid;grid-template-columns:42% 58%;width:100%;height:100%;min-height:440px;position:relative}\n.ph{background:#e9e3cf url(https://app.ipanemabeautyandspa.com/img/w/brow-076.jpg) center/cover no-repeat}\n.bd{padding:34px 36px 24px;display:flex;flex-direction:column;justify-content:center}\n.ey{margin:0;font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#6b6b6b}\nh2{margin:10px 0 0;font-size:34px;line-height:1.08;font-weight:700;letter-spacing:-.03em}\n.sub{margin:12px 0 0;font-size:16px;line-height:1.5;color:#4d4d4d}\nform{margin-top:20px;display:flex;flex-direction:column;gap:10px}\ninput{width:100%;height:48px;border:1px solid #d6d6d6;border-radius:14px;padding:0 16px;font:inherit;font-size:16px;color:#1f1f1f;background:#fafafa;outline:none}\ninput:focus{border-color:#333;background:#fff}\nbutton.go{height:52px;border:0;border-radius:999px;background:#333;color:#fff;font:inherit;font-size:16px;font-weight:600;cursor:pointer;margin-top:4px}\nbutton.go[disabled]{opacity:.6}\n.fine{margin:12px 0 0;font-size:12px;line-height:1.5;color:#8a8a8a}\n.msg{margin:10px 0 0;font-size:14px;color:#b3261e;min-height:0}\n.x{position:absolute;top:14px;inset-inline-end:14px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.9);font-size:20px;color:#4d4d4d;cursor:pointer;z-index:2}\n.no{margin-top:8px;background:none;border:0;color:#6b6b6b;font:inherit;font-size:14px;cursor:pointer;text-decoration:underline}\n.done h2{font-size:30px}.done a{display:inline-flex;align-items:center;justify-content:center;height:50px;padding:0 28px;border-radius:999px;background:#333;color:#fff;text-decoration:none;font-weight:600;margin-top:20px}\n@media(max-width:640px){.w{grid-template-columns:1fr;grid-template-rows:150px auto;border-radius:22px}.bd{padding:24px 22px 20px}h2{font-size:27px}}\n";
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
    this.render();
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
    const close=()=>this.dispatchEvent(new CustomEvent('ipa-close',{bubbles:true,composed:true}));
    this.root.querySelector('.x').onclick=close; const no=this.root.querySelector('.no'); if(no) no.onclick=close;
    const f=this.root.querySelector('form');
    if (f) f.onsubmit=(e)=>{ e.preventDefault();
      const d={name:f.name.value.trim(), email:f.email.value.trim().toLowerCase(), phone:f.phone.value.trim(), lang:this.lang};
      const msg=this.root.querySelector('.msg');
      if(!d.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email) || d.phone.replace(/\D/g,'').length<10){ msg.textContent=t.req; return; }
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
