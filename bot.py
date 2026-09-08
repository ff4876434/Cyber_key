import os
from threading import Thread
from flask import Flask
import telebot
import firebase_admin
from firebase_admin import credentials, firestore

# --- WEB SERVER БАРОИ 24/7 ХОСТИНГ ДАР RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ПАЙВАСТШАВӢ БА FIREBASE ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase connected successfully!")
except Exception as e:
    print(f"Firebase Error: {e}")

# --- ТОКЕНИ АСЛИИ БОТИ ШУМО ---
TOKEN = "8831981869:AAFvZYTlvg747qzRScCSVnraNSWZi7mQDlo"
bot = telebot.TeleBot(TOKEN)

# --- ФАРМОНИ /START ВА САНҶИШИ ЛИНКИ СОМОНА ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    
    # Санҷиши гузариш аз сомона (?start=from_website)
    if len(args) > 1 and args[1] == "from_website":
        try:
            # Аз коллексияи 'keys' калиди озодро меҷӯяд
            keys_ref = db.collection('keys').where('is_used', '==', False).limit(1)
            docs = list(keys_ref.stream())
            
            if len(docs) > 0:
                key_doc = docs[0]
                key_data = key_doc.to_dict()
                actual_key = key_data.get('key_value')
                
                # Мақоми калидро ба истифодашуда (true) табдил медиҳад
                db.collection('keys').document(key_doc.id).update({'is_used': True})
                
                bot.reply_to(message, f"🎉 Ташаккур! Рекламаро гузаштед.\n\n🔑 Калиди VIP-и шумо:\n`{actual_key}`", parse_mode="Markdown")
            else:
                bot.reply_to(message, "⚠️ Мутаассифона, ҳоло калидҳои озод дар база тамом шудаанд!")
        except Exception as e:
            bot.reply_to(message, "⚠️ Хатогӣ дар пайвастшавӣ ба базаи калидҳо.")
    else:
        # Агар касе бе сомона мустақиман ботро кушояд
        bot.reply_to(message, "❌ Салом! Барои гирифтани калид аввал ба сайти мо рафта, 3 рекламаро дида, тугмаи Telegram-ро пахш кунед.")

if __name__ == "__main__":
    keep_alive()
    print("Bot startup successfully...")
    bot.infinity_polling()
