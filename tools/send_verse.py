"""Daily verse push: schedules one OneSignal notification per chosen hour (tag verse_hour),
delivered at that hour in each subscriber's own timezone. Runs once a day from GitHub Actions."""
import json, os, sys, urllib.request, datetime, zoneinfo

KEY = os.environ.get('ONESIGNAL_KEY', '').strip()
APP_ID = 'de3c4b19-f481-4b2d-b56a-b19364dda31a'
if not KEY:
    print('ONESIGNAL_KEY not set; nothing sent'); sys.exit(0)

verses = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'verses.json'), encoding='utf-8'))
today = datetime.datetime.now(zoneinfo.ZoneInfo('America/New_York')).date()
idx = min(364, (today - datetime.date(today.year, 1, 1)).days)
refs, texts = verses[idx]
LANGS = ['en', 'pt', 'es', 'he', 'ar']
HEAD = {'en': 'Verse of the day ☀️', 'pt': 'Versículo do dia ☀️', 'es': 'Versículo del día ☀️', 'he': 'פסוק היום ☀️', 'ar': 'آية اليوم ☀️'}

def short(t, n=170):
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'

contents = {l: f'{short(texts[i])} — {refs[i]}' for i, l in enumerate(LANGS)}
headings = {l: HEAD[l] for l in LANGS}
print('Day', today, '->', refs[0])

ok = 0
for h in range(5, 23):
    tod = f'{(h % 12) or 12}:00{"AM" if h < 12 else "PM"}'
    body = {
        'app_id': APP_ID, 'target_channel': 'push',
        'filters': [{'field': 'tag', 'key': 'verse', 'relation': '=', 'value': '1'},
                    {'field': 'tag', 'key': 'verse_hour', 'relation': '=', 'value': str(h)}],
        'headings': headings, 'contents': contents,
        'url': 'https://app.ipanemabeautyandspa.com/',
        'delayed_option': 'timezone', 'delivery_time_of_day': tod,
        'ttl': 6 * 3600,
    }
    req = urllib.request.Request('https://api.onesignal.com/notifications?c=push', data=json.dumps(body).encode(),
                                 headers={'Authorization': f'Key {KEY}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read() or b'{}')
        print(h, tod, 'id' in res and 'scheduled' or res)
        ok += 1
    except urllib.error.HTTPError as e:
        print(h, tod, 'HTTP', e.code, e.read()[:300])
print(f'{ok}/18 scheduled')
sys.exit(0 if ok else 1)
