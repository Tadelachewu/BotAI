import os
import telebot
import requests
import time
import json
import traceback
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# === Load .env Variables ===
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
ENV = os.getenv('ENV', 'development')  # 'development' or 'production'

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("⚠️ BOT_TOKEN and GEMINI_API_KEY are required!")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
app = Flask(__name__)

# === User Data Storage Files ===
LANG_FILE = 'user_languages.json'
NAME_FILE = 'user_names.json'
user_languages, user_names = {}, {}

def load_data():
    try:
        if os.path.exists(LANG_FILE):
            with open(LANG_FILE, 'r') as f:
                user_languages.update(json.load(f))
        if os.path.exists(NAME_FILE):
            with open(NAME_FILE, 'r') as f:
                user_names.update(json.load(f))
    except Exception as e:
        print(f"❌ Failed to load user data: {e}")

def save_data():
    try:
        with open(LANG_FILE, 'w') as f:
            json.dump(user_languages, f)
        with open(NAME_FILE, 'w') as f:
            json.dump(user_names, f)
    except Exception as e:
        print(f"❌ Failed to save user data: {e}")

load_data()

# === Debug Log ===
def debug_log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# === Language Buttons ===
def get_language_buttons():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")
    )
    return markup

# === Gemini AI Request ===
def ask_romantic_ai(user_input, language, user_id):
    headers = {"Content-Type": "application/json"}
    girl = user_names.get(str(user_id), {}).get('girl', 'Zebe')
    boy = user_names.get(str(user_id), {}).get('boy', 'Tadele')

    if language == "am":
        prompt = f"አንተ {boy} መስፍን ነህ፣ የ{girl} ፍቅረኛ።\n\n{girl}: {user_input}\n{boy}:"
    else:
        prompt = f"You are {boy} Mesfin, {girl}'s romantic boyfriend.\n\n{girl}: {user_input}\n{boy}:"

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "topP": 1,
            "topK": 1,
            "maxOutputTokens": 2048
        }
    }

    try:
        res = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            headers=headers, json=data, timeout=30
        )
        res.raise_for_status()
        output = res.json()
        return output['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        debug_log(f"❌ Gemini Error: {e}\n{traceback.format_exc()}")
        return "💔 Gemini couldn't reply. Please try again."

# === /start ===
@bot.message_handler(commands=['start'])
def welcome(message):
    debug_log(f"/start by {message.from_user.id}")
    bot.send_message(
        message.chat.id,
        "💖 Welcome! Choose your language:",
        reply_markup=get_language_buttons()
    )

# === /setnames ===
@bot.message_handler(commands=['setnames'])
def set_names(message):
    args = message.text.split()[1:]
    if len(args) != 2:
        bot.send_message(message.chat.id, "Usage: /setnames [your_name] [his_name]")
        return
    user_id = str(message.from_user.id)
    user_names[user_id] = {'girl': args[0], 'boy': args[1]}
    save_data()
    lang = user_languages.get(user_id, 'en')
    response = (
        f"✅ Names updated!\nYou: {args[0]}\nHim: {args[1]}"
        if lang == 'en'
        else f"✅ ስሞች ተቀይረዋል!\nአንቺ: {args[0]}\nእሱ: {args[1]}"
    )
    bot.send_message(message.chat.id, response)

# === Language Selection ===
@bot.callback_query_handler(func=lambda call: True)
def set_language(call):
    user_id = str(call.from_user.id)
    lang = call.data.split("_")[1]
    user_languages[user_id] = lang
    save_data()
    bot.answer_callback_query(call.id, "✓ Language selected!")
    message = (
        "🌹 Speak your heart!\nTo set names: /setnames yourname hisname"
        if lang == 'en'
        else "🌹 ልብህን ንገርኝ!\nስሞችን ለማስተካከል: /setnames አንቺ እና እሱ"
    )
    bot.edit_message_text(message, call.message.chat.id, call.message.message_id)

# === Handle Text Messages ===
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    lang = user_languages.get(user_id)
    if not lang:
        bot.send_message(
            message.chat.id,
            "💬 Please choose your language:",
            reply_markup=get_language_buttons()
        )
        return

    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(min(max(1, len(message.text) / 20), 3))
    reply = ask_romantic_ai(message.text, lang, user_id)
    bot.send_message(message.chat.id, reply)

# === Webhook (for Render) ===
#bind thison server env  as https://botai-2789.onrender.com/bot
@app.route('/bot', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.data.decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid request', 403

@app.route('/')
def home():
    return "❤️ Romantic Gemini Bot is running!"

# === Entrypoint ===
if __name__ == '__main__':
    if ENV == 'production':
        debug_log("🚀 Running in production (webhook) mode...")
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        debug_log("🧪 Running in development (polling) mode...")
        bot.remove_webhook()
        while True:
            try:
                bot.polling(none_stop=True, timeout=30)
            except Exception as e:
                debug_log(f"Polling error: {e}")
                time.sleep(10)
