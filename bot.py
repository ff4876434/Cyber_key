import os
from threading import Thread
from flask import Flask
import telebot
import firebase_admin
from firebase_admin import credentials

# 1. Веб-сервери Flask барои пешгирӣ аз хатогии Render (Port Timeout)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

# 2. Пайвастшавӣ ба Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyberhostvip-default-rtdb.firebaseio.com/'
})

# 3. Пайвастшавӣ ба Боти Telegram
BOT_TOKEN = "8831981869:AAFvZYTlvg747qzRScCSVnraNSWZi7mQDlo" # Токени пурраи худро дар ин ҷо монед
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Сaлом! Боти CYBER HOST VIP фаъол аст.")

# 4. Ишғолкунӣ ва иҷрои бот
if __name__ == "__main__":
    bot.infinity_polling()
