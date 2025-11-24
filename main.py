import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8364612582:AAHekCdqB8afotCloEqtIu9eV_ER5-bmqmA"
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🎤 تحليل صوت المحرك"),
        KeyboardButton("📸 تحليل لوحة العدادات")
    )
    markup.add(
        KeyboardButton("💎 النسخة المدفوعة"),
        KeyboardButton("ℹ️ مساعدة")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🚗 أهلاً بك في *CarScan AI*\n"
        "اختار الخدمة من الأسفل:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: True)
def buttons(message):

    if message.text == "🎤 تحليل صوت المحرك":
        bot.send_message(message.chat.id, "🎙️ أرسل لي صوت المحرك (10 ثواني).")
    
    elif message.text == "📸 تحليل لوحة العدادات":
        bot.send_message(message.chat.id, "📷 أرسل صورة واضحة للوحة العدادات.")
    
    elif message.text == "💎 النسخة المدفوعة":
        bot.send_message(message.chat.id, "💎 النسخة المدفوعة سيتم توفيرها قريباً.")
    
    elif message.text == "ℹ️ مساعدة":
        bot.send_message(message.chat.id, "✳️ أرسل صوت أو صورة وسيتم تحليلها.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(message, "🔍 جاري تحليل صوت المحرك...\n(الذكاء الاصطناعي سيتم إضافته لاحقاً)")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "🔎 جارٍ تحليل لوحة العدادات...\n(سيتم إضافة AI بعد الرفع)")

from flask import Flask, request

app = Flask(__name__)

@app.route("/" + TOKEN, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://your-render-url.onrender.com/" + TOKEN)
    return "OK", 200

app.run(host="0.0.0.0", port=10000)
