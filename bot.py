"""
bot.py — بوت تيليجرام بسيط
المكتبات: requests فقط
تشغيل: python bot.py
"""
import os, time, requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN   = os.environ.get('BOT_TOKEN',   '8803704528:AAH_gRbcuOJS6fknXi0sWi6HDLBeJfWXK2E')
WEBAPP_URL  = os.environ.get('WEBAPP_URL',  'https://waredwebsite2.vercel.app/')
CHANNEL_URL = os.environ.get('CHANNEL_URL', 'https://t.me/medo_channel')
SUPPORT_URL = os.environ.get('SUPPORT_URL', 'https://t.me/medo_add')
TG_API      = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(chat_id, text, keyboard=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    if keyboard:
        payload['reply_markup'] = {'inline_keyboard': keyboard}
    requests.post(f"{TG_API}/sendMessage", json=payload, timeout=10)

def handle(update):
    msg  = update.get('message', {})
    text = msg.get('text', '')
    if not text.startswith('/start'):
        return
    chat_id    = msg['chat']['id']
    first_name = msg.get('from', {}).get('first_name', 'مستخدم')
    parts      = text.split()
    ref        = parts[1].replace('ref_', '') if len(parts) > 1 else ''
    url        = f"{WEBAPP_URL}?tg=1&ref={ref}" if ref else f"{WEBAPP_URL}?tg=1"

    send(chat_id,
        f"👋 أهلاً *{first_name}*!\n\n"
        "⚡ *Reward Ads* — اكسب من مشاهدة الإعلانات\n\n"
        "📺 شاهد إعلانات واكسب مكافآت فورية\n"
        "👥 ادعُ أصدقاءك واحصل على عمولة *5%*\n"
        "💳 اسحب أرباحك عبر محافظ الدفع الإلكتروني\n\n"
        "👇 اضغط لفتح التطبيق الآن!",
        keyboard=[
            [{'text': '🚀 افتح التطبيق', 'web_app': {'url': url}}],
            [
                {'text': '📢 قناتنا', 'url': CHANNEL_URL},
                {'text': '🆘 الدعم',  'url': SUPPORT_URL}
            ]
        ]
    )

def main():
    offset = 0
    print("🤖 Bot running...")
    while True:
        try:
            r    = requests.get(f"{TG_API}/getUpdates",
                                params={'offset': offset, 'timeout': 30},
                                timeout=35)
            data = r.json()
            for update in data.get('result', []):
                offset = update['update_id'] + 1
                handle(update)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
