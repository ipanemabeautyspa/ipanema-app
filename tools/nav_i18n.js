/* ipa-nav-i18n: translates the Wix header menu + Book now button to the visitor's site language */
(function(){
if (window.__ipaNavI18n) return; window.__ipaNavI18n = 1;
var T = {
 pt: {'Brows & Lashes':'Sobrancelhas','Waxing':'Depilação','Hair':'Cabelo','Nails':'Unhas','Visit':'Visite','Book now':'Agende já'},
 es: {'Brows & Lashes':'Cejas','Waxing':'Depilación','Hair':'Cabello','Nails':'Uñas','Visit':'Visítanos','Book now':'Reservar'},
 he: {'Brows & Lashes':'גבות וריסים','Waxing':'שעווה','Hair':'שיער','Nails':'ציפורניים','Visit':'בקרו אותנו','Book now':'קביעת תור'},
 ar: {'Brows & Lashes':'الحواجب','Waxing':'الشمع','Hair':'الشعر','Nails':'الأظافر','Visit':'زورونا','Book now':'احجز الآن'}
};
var LS = ['en','pt','es','he','ar'];
function pick(){ var l=''; try { l = new URLSearchParams(location.search).get('lang') || localStorage.getItem('ipa-site-lang') || ''; } catch(e){}
  if (LS.indexOf(l) < 0) { var b=(navigator.language||'en').slice(0,2).toLowerCase(); l = LS.indexOf(b) >= 0 ? b : 'en'; } return l; }
var lang = pick();
function roots(){ var r=[].slice.call(document.querySelectorAll('nav')); [].forEach.call(document.querySelectorAll('header a'), function(a){ if (r.indexOf(a) < 0) r.push(a); }); return r; }
function run(){
  var d = T[lang] || {};
  roots().forEach(function(root){
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), n;
    while ((n = w.nextNode())) {
      if (n.__ipaEn === undefined) { var k = n.nodeValue.replace(/\s+/g,' ').trim(); if (!(k in T.pt)) continue; n.__ipaEn = n.nodeValue; }
      var en = n.__ipaEn, key = en.replace(/\s+/g,' ').trim(), t = d[key];
      var v = t ? en.match(/^\s*/)[0] + t + en.match(/\s*$/)[0] : en;
      if (n.nodeValue !== v) n.nodeValue = v;
    }
  });
}
var q = 0; function soon(){ if (q) return; q = 1; requestAnimationFrame(function(){ q = 0; run(); }); }
window.addEventListener('ipa-lang', function(e){ if (e && e.detail) lang = e.detail; run(); });
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
try { new MutationObserver(soon).observe(document.body, {childList:true, subtree:true}); } catch(e){}
})();
