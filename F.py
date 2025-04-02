import requests
from flask import Flask, request
import telegram

# بيانات البوت
BOT_TOKEN = '7638572674:AAEL6pQZk5lCjRLf2CrdFUs_bAXSSqJVUAg'
bot = telegram.Bot(token=BOT_TOKEN)

# مفتاح RapidAPI
RAPIDAPI_KEY = '372942a308msha820f36dc5d1f27p1e5a1cjsn435c1973fc54'

# إعداد التطبيق
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if "instagram.com/reel/" in text:
            bot.send_message(chat_id=chat_id, text="جاري تحميل الريلز... ⏳")

            try:
                url = "https://instagram-reels-downloader-api.p.rapidapi.com/download"
                querystring = {"url": text}
                headers = {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "instagram-reels-downloader-api.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers, params=querystring)
                result = response.json()
                video_url = result.get("video")

                if video_url:
                    bot.send_video(chat_id=chat_id, video=video_url, caption="🎬 تم تحميل الريلز!")
                else:
                    bot.send_message(chat_id=chat_id, text="❌ ما قدرت أجيب الفيديو.")
            except Exception as e:
                bot.send_message(chat_id=chat_id, text=f"⚠️ صار خطأ: {e}")
        else:
            bot.send_message(chat_id=chat_id, text="📎 أرسل رابط ريلز من إنستقرام.")

    return "ok"

@app.route("/")
def home():
    return "البوت شغال ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
