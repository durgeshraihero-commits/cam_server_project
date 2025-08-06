import os
from flask import Flask, render_template, request
import telebot

# ==== CONFIGURATION ====
BOT_TOKEN = "8257336150:AAGjrGA6AQERkWuKG0hTVAjs_7oTqMzXw14"  # Your bot token
CHAT_ID = "6314556756"  # Your chat ID

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)


# ==== ROUTES ====

@app.route('/')
def index():
    # This will load templates/index.html and show your image
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image found", 400

    image = request.files['image']

    # Send image to Telegram chat
    bot.send_photo(CHAT_ID, image)

    return "Image sent to Telegram!", 200


if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=5000)
