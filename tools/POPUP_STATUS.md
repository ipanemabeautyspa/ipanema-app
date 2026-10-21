# Popup 10% (primeira visita) — status 2026-10-21

Feito no editor Wix (Dev Mode ligado):
- masterPage.js: abre o lightbox "Welcome" 4s depois da 1a visita (local storage 'ipaWelcome').
- backend/welcome.web.js: registerWelcome(name,email,phone) -> procura contato por e-mail/telefone;
  se existe => {status:'returning'}; senao cria contato com etiqueta "Welcome 10%" => {status:'new'}.
- Popup "Welcome": exibicao automatica = Nao; 780x500; fundo 0% opacidade;
  custom element #customElement1 (URL .../site/ipa-welcome.js, tag ipa-welcome), 780x500.
- Codigo da pagina do popup: liga ipa-submit -> registerWelcome -> setAttribute('result'); ipa-close -> fecha.

Falta:
- Conferir posicao X/Y do elemento (encostar no canto do popup), cor do overlay (escuro), apagar o X padrao.
- Automacao Wix: etiqueta "Welcome 10%" adicionada -> e-mail com o codigo (ex.: WELCOME10).
- Salvar, publicar, testar no site ao vivo.
