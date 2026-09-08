import telebot
import firebase_admin
from firebase_admin import credentials, db

# 1. Пайвастшавӣ ба Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyberhostvip-default-rtdb.firebaseio.com/' # Агар суроғаи дигар бошад, иваз кунед
})

# 2. Пайвастшавӣ ба Бот
BOT_TOKEN = "8831981869:AAFvZYTlvg747qzRScCSVnraNSWZi7mQDlo"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = message.text
    # Агар корбар аз сайт омада бошад (start=get_vip_key)
    if 'get_vip_key' in text:
        chat_id = str(message.chat.id)
        ref = db.reference(f'keys/{chat_id}')
        key_data = ref.get()
        
        if key_data and 'key' in key_data:
            bot.reply_to(message, f"🔑 **Калиди VIP-и шумо:**\n`{key_data['key']}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Калид пайдо нашуд. Лутфан аввал дар вебсайт тугмаи 'Get Key'-ро зер кунед.")
    else:
        bot.reply_to(message, "Салом! Ба боти Cyber Host VIP хуш омадед. Барои гирифтани калид аз вебсайт истифода баред.")

print("Бот фаъол шуд...")
bot.infinity_polling()
