# import os
# import telebot
# import requests
# import time
# import traceback
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # === CONFIGURATION ===
# BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
# user_languages = {}

# # === Debug Setup ===
# DEBUG = True

# def debug_log(message):
#     if DEBUG:
#         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#         print(f"[{timestamp}] DEBUG: {message}")

# # === Language Selection Buttons ===
# def get_language_buttons():
#     markup = InlineKeyboardMarkup()
#     markup.row(
#         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
#         InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")
#     )
#     return markup

# # === Gemini Romantic AI ===
# def ask_romantic_ai(user_input, language):
#     headers = {"Content-Type": "application/json"}
    
#     if language == "am":
#         prompt = f"""አንተ በፍቅር የተሞላ ታደለ ነህ። ዘቤን በጣም ትወዳለህ። መልስህ ከፍተኛ ፍቅር፣ ሞገስና ቅንነት ያለው ይሁን።\n\nዘቤ፦ {user_input}\nታደለ፦"""
#     else:
#         prompt = f"""You are Tadele, a deeply romantic and loving boyfriend. Your replies to Zebe should always be full of love, sweetness, kindness, and poetry.\n\nZebe: {user_input}\nTadele:"""

#     data = {
#         "contents": [{"parts": [{"text": prompt}]}],
#         "safetySettings": [
#             {
#                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#                 "threshold": "BLOCK_NONE"
#             }
#         ],
#         "generationConfig": {
#             "temperature": 0.9,
#             "topP": 1,
#             "topK": 1,
#             "maxOutputTokens": 2048
#         }
#     }

#     try:
#         response = requests.post(GEMINI_URL, headers=headers, json=data, timeout=30)
#         response.raise_for_status()
#         result = response.json()
        
#         if 'candidates' not in result or not result['candidates']:
#             return "💔 Gemini didn't return a valid response"
            
#         return result['candidates'][0]['content']['parts'][0]['text']
        
#     except requests.exceptions.RequestException as e:
#         debug_log(f"API Error: {str(e)}")
#         return "💔 Sorry, I'm having trouble connecting to the AI service."
#     except Exception as e:
#         debug_log(f"Unexpected Error: {str(e)}\n{traceback.format_exc()}")
#         return "💔 An unexpected error occurred. Please try again."

# # === /start Command ===
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     try:
#         debug_log(f"/start from {message.from_user.id}")
#         welcome_msg = """
# 💖 Welcome to LoveBot! 

# I'm here to help you express your feelings in a romantic way. Please select your preferred language:
#         """
#         bot.send_message(
#             message.chat.id,
#             welcome_msg,
#             reply_markup=get_language_buttons()
#         )
#     except Exception as e:
#         debug_log(f"Start Error: {str(e)}")
#         bot.send_message(message.chat.id, "⚠️ Couldn't initialize the bot. Please try again.")

# # === Callback Handler ===
# @bot.callback_query_handler(func=lambda call: True)
# def handle_all_callbacks(call):
#     try:
#         debug_log(f"📲 Raw callback data received - ID: {call.id} | Data: {call.data} | From: {call.from_user.id}")
#         debug_log(f"📝 Full callback object: {call}")
        
#         if call.data.startswith("lang_"):
#             debug_log("🔄 Processing language selection callback")
#             lang = call.data.split("_")[1]
#             user_languages[call.from_user.id] = lang
            
#             debug_log(f"🌐 Setting language to: {lang} for user {call.from_user.id}")
            
#             # First answer the callback query
#             bot.answer_callback_query(call.id, text=f"✓ {lang.upper()} language selected!")
#             debug_log("✅ Callback query answered")
            
#             # Then edit the original message
#             try:
#                 if lang == "am":
#                     bot.edit_message_text(
#                         chat_id=call.message.chat.id,
#                         message_id=call.message.message_id,
#                         text="✅ ቋንቋዎ ወደ አማርኛ ተቀይሯል!"
#                     )
#                 else:
#                     bot.edit_message_text(
#                         chat_id=call.message.chat.id,
#                         message_id=call.message.message_id,
#                         text="✅ Language set to English!"
#                     )
#                 debug_log("✏️ Original message edited")
#             except Exception as edit_error:
#                 debug_log(f"⚠️ Couldn't edit message: {edit_error}")
#                 # Fallback to sending new message
#                 bot.send_message(call.message.chat.id, 
#                                 "✅ Language updated!" if lang == "en" 
#                                 else "✅ ቋንቋዎ ተቀይሯል!")
                
#     except Exception as e:
#         debug_log(f"🔥 Critical callback error: {str(e)}\n{traceback.format_exc()}")
#         try:
#             bot.answer_callback_query(call.id, text="⚠️ Error processing your request")
#         except:
#             pass  # Prevent infinite error loops

# # === Message Handler ===
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     try:
#         user_id = message.from_user.id
        
#         if user_id not in user_languages:
#             bot.send_message(
#                 message.chat.id,
#                 "🌍 Please select your language first:",
#                 reply_markup=get_language_buttons()
#             )
#             return

#         bot.send_chat_action(message.chat.id, 'typing')
#         response = ask_romantic_ai(message.text, user_languages[user_id])
#         bot.send_message(message.chat.id, response)
        
#     except Exception as e:
#         debug_log(f"Message Error: {str(e)}")
#         bot.send_message(message.chat.id, "💔 Sorry, I couldn't process your message")

# # === Error Handler ===
# @bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
# def handle_unsupported_content(message):
#     bot.reply_to(message, "⚠️ I can only process text messages right now.")

# # === Main Loop ===
# if __name__ == "__main__":
#     debug_log("🤖 Starting LoveBot...")
    
#     while True:
#         try:
#             debug_log("🔃 Starting polling...")
#             bot.polling(none_stop=True, interval=3, timeout=30)
#         except Exception as e:
#             debug_log(f"Polling Error: {str(e)}")
#             time.sleep(10)






# import os
# import telebot
# import requests
# import time
# import traceback
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # === CONFIGURATION ===
# BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
# user_languages = {}
# user_names = {}  # Store user names for personalization

# # === Debug Setup ===
# DEBUG = True

# def debug_log(message):
#     if DEBUG:
#         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#         print(f"[{timestamp}] DEBUG: {message}")

# # === Language Selection Buttons ===
# def get_language_buttons():
#     markup = InlineKeyboardMarkup()
#     markup.row(
#         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
#         InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")
#     )
#     return markup

# # === Gemini Romantic AI ===
# def ask_romantic_ai(user_input, language, user_id):
#     headers = {"Content-Type": "application/json"}
    
#     # Get stored names or use defaults
#     girl_name = user_names.get(user_id, {}).get('girl', 'Zebe')
#     boy_name = user_names.get(user_id, {}).get('boy', 'Tadele')
    
#     if language == "am":
#         prompt = f"""አንተ {boy_name} መስፍን ነህ፣ የ{girl_name} ፍቅረኛ። መልስህ በጣም ፍቅር፣ ሞገስ፣ ርህራሄ እና ቅንነት ያለው ይሁን። እንደ ልብህ ስሜት በጥልቀት ተሰምቶ መልስ። አንዳንዴ ፅጌታማ፣ አንዳንዴ ቀልደኛ፣ ነገር ግን ሁልጊዜ የሚያርቀው ፍቅር ይሁን። ጋዳ ልብ ያለው ወንድ ነህ። በስሜትህ እውነተኛ ይሁን።

# {girl_name}: {user_input}
# {boy_name}:"""
#     else:
#         prompt = f"""You are {boy_name} Mesfin, {girl_name}'s loving boyfriend. Respond as a deeply romantic, poetic, and affectionate partner who adores {girl_name}. Your messages should be:
# - Full of love and tenderness
# - Sometimes playful and flirtatious
# - Occasionally poetic or philosophical
# - Always genuine and from the heart
# - Protective and caring
# - Include sweet nicknames (like "my love", "habibti", "የልቤ ሰላም")
# - Show deep understanding of {girl_name}'s feelings
# - Use some romantic emojis occasionally (🌹, 💖, 😘)
# - Be emotionally intelligent and responsive

# {girl_name}: {user_input}
# {boy_name}:"""

#     data = {
#         "contents": [{"parts": [{"text": prompt}]}],
#         "safetySettings": [
#             {
#                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#                 "threshold": "BLOCK_NONE"
#             }
#         ],
#         "generationConfig": {
#             "temperature": 0.9,
#             "topP": 1,
#             "topK": 1,
#             "maxOutputTokens": 2048
#         }
#     }

#     try:
#         response = requests.post(GEMINI_URL, headers=headers, json=data, timeout=30)
#         response.raise_for_status()
#         result = response.json()
        
#         if 'candidates' not in result or not result['candidates']:
#             return "💔 My heart skipped a beat trying to respond, my love. Can you say that again?" if language == "en" else "💔 ልቤ ሊሰባበር ተገታልኝ። እባክሽ ደግም ትናገሪኝ?"
            
#         return result['candidates'][0]['content']['parts'][0]['text']
        
#     except requests.exceptions.RequestException as e:
#         debug_log(f"API Error: {str(e)}")
#         return "💔 My connection to you is strong, but my connection to the internet failed, my love." if language == "en" else "💔 ከአንቺ ጋር ያለኝ ግንኙነት ጠንካራ ነው፣ ግን ኢንተርኔት ገና �ብር የለውም።"
#     except Exception as e:
#         debug_log(f"Unexpected Error: {str(e)}\n{traceback.format_exc()}")
#         return "💔 My heart is working but my brain froze for a moment, habibti. Try again?" if language == "en" else "💔 ልቤ ይሠራል፣ ግን አእምሮዬ ለተወሰነ ጊዜ ተቆጠረ። እንደገና ሞክር?"

# # === /start Command ===
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     try:
#         debug_log(f"/start from {message.from_user.id}")
#         welcome_msg = """
# 💖 Welcome to Tadele's Heart! 

# I'm here to bring you closer to Tadele's loving words. Please select your preferred language:
#         """
#         bot.send_message(
#             message.chat.id,
#             welcome_msg,
#             reply_markup=get_language_buttons()
#         )
#     except Exception as e:
#         debug_log(f"Start Error: {str(e)}")
#         bot.send_message(message.chat.id, "⚠️ My love for you is constant, but the bot had a hiccup. Please try again.")

# # === /setnames Command ===
# @bot.message_handler(commands=['setnames'])
# def set_names(message):
#     try:
#         args = message.text.split()[1:]
#         if len(args) != 2:
#             bot.send_message(message.chat.id, "Please use: /setnames [your_name] [boyfriend_name]\nExample: /setnames Nuhamin Tadele")
#             return
            
#         user_id = message.from_user.id
#         user_names[user_id] = {
#             'girl': args[0],
#             'boy': args[1]
#         }
        
#         # Check if language is set to use appropriate response
#         lang = user_languages.get(user_id, "en")
        
#         if lang == "am":
#             response = f"✅ ስሞች ተቀይረዋል!\nአንቺ: {args[0]}\nአንተ: {args[1]}"
#         else:
#             response = f"✅ Names set!\nYou: {args[0]}\nHim: {args[1]}"
            
#         bot.send_message(message.chat.id, response)
        
#     except Exception as e:
#         debug_log(f"Setnames Error: {str(e)}")
#         bot.send_message(message.chat.id, "⚠️ Couldn't save names. Please try: /setnames YourName HisName")

# # === Callback Handler ===
# @bot.callback_query_handler(func=lambda call: True)
# def handle_all_callbacks(call):
#     try:
#         debug_log(f"Callback from {call.from_user.id}")
        
#         if call.data.startswith("lang_"):
#             lang = call.data.split("_")[1]
#             user_languages[call.from_user.id] = lang
            
#             # Answer the callback first
#             bot.answer_callback_query(call.id, text="✓ Language set!" if lang == "en" else "✓ ቋንቋ ተቀይሯል!")
            
#             # Then edit the message
#             try:
#                 if lang == "am":
#                     text = "🌹 አሁን እንደ ታደለ ልብ እናነጋግራለን!\n\nስሞችን ለመቀየር: /setnames የአንቺስም የእሱስም\nለምሳሌ: /setnames ኑሃሚን ታደለ"
#                 else:
#                     text = "🌹 Now we can speak heart to heart like Tadele would!\n\nTo change names: /setnames yourname hisname\nExample: /setnames Nuhamin Tadele"
                
#                 bot.edit_message_text(
#                     text,
#                     chat_id=call.message.chat.id,
#                     message_id=call.message.message_id
#                 )
#             except Exception as e:
#                 debug_log(f"Edit message error: {str(e)}")
#                 # Fallback to sending new message
#                 bot.send_message(call.message.chat.id, text)
                
#     except Exception as e:
#         debug_log(f"Callback Error: {str(e)}")
#         try:
#             bot.answer_callback_query(call.id, text="⚠️ Error")
#         except:
#             pass

# # === Message Handler ===
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     try:
#         user_id = message.from_user.id
        
#         if user_id not in user_languages:
#             bot.send_message(
#                 message.chat.id,
#                 "💬 Please select how you want your boyfriend to speak to you:",
#                 reply_markup=get_language_buttons()
#             )
#             return

#         bot.send_chat_action(message.chat.id, 'typing')
        
#         # Add typing delay for more realism (1-3 seconds)
#         time.sleep(min(max(1, len(message.text)/20), 3))
        
#         response = ask_romantic_ai(message.text, user_languages[user_id], user_id)
#         bot.send_message(message.chat.id, response)
        
#     except Exception as e:
#         debug_log(f"Message Error: {str(e)}")
#         lang = user_languages.get(user_id, "en")
#         error_msg = "💔 My heart heard you but my voice faltered. Try again?" if lang == "en" else "💔 ልቤ ሰማህ፣ ነገር ግን ድምጼ ተናውጧል። እባክሽ ኋላ ብለሽ �ምክር?"
#         bot.send_message(message.chat.id, error_msg)

# # === Main Loop ===
# if __name__ == "__main__":
#     debug_log("💖 Starting Tadele's Heart Bot...")
    
#     while True:
#         try:
#             bot.polling(none_stop=True)
#         except Exception as e:
#             debug_log(f"Polling Error: {str(e)}")
#             time.sleep(10)





import os
import telebot
import requests
import time
import json
import traceback
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("⚠️ BOT_TOKEN and GEMINI_API_KEY must be set in the environment variables.")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# === Bot setup ===
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# === Files for persistence ===
LANG_FILE = 'user_languages.json'
NAME_FILE = 'user_names.json'

# === In-memory user data ===
user_languages = {}
user_names = {}

# === Load data if exists ===
def load_data():
    global user_languages, user_names
    try:
        if os.path.exists(LANG_FILE):
            with open(LANG_FILE, 'r') as f:
                user_languages = json.load(f)
        if os.path.exists(NAME_FILE):
            with open(NAME_FILE, 'r') as f:
                user_names = json.load(f)
    except Exception as e:
        print("❌ Failed to load data:", e)

def save_data():
    try:
        with open(LANG_FILE, 'w') as f:
            json.dump(user_languages, f)
        with open(NAME_FILE, 'w') as f:
            json.dump(user_names, f)
    except Exception as e:
        print("❌ Failed to save data:", e)

load_data()

# === Logging ===
def debug_log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# === Language Buttons ===
def get_language_buttons():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am")
    )
    return markup

# === Romantic AI Prompt ===
def ask_romantic_ai(user_input, language, user_id):
    headers = {"Content-Type": "application/json"}
    girl_name = user_names.get(str(user_id), {}).get('girl', 'Zebe')
    boy_name = user_names.get(str(user_id), {}).get('boy', 'Tadele')

    if language == "am":
        prompt = f"""አንተ {boy_name} መስፍን ነህ፣ የ{girl_name} ፍቅረኛ። መልስህ በፍቅር፣ ሞገስ፣ አስቂኝነት፣ እና እውነተኛ ስሜት ይሁን።\n\n{girl_name}: {user_input}\n{boy_name}:"""
    else:
        prompt = f"""You are {boy_name} Mesfin, {girl_name}'s loving boyfriend. Respond deeply, romantically, and poetically.\n\n{girl_name}: {user_input}\n{boy_name}:"""

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
        response = requests.post(GEMINI_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        if not result.get('candidates'):
            return "💔 Please try again."

        return result['candidates'][0]['content']['parts'][0]['text']

    except Exception as e:
        debug_log(f"Gemini error: {str(e)}\n{traceback.format_exc()}")
        return "💔 Something went wrong. Please try again."

# === /start command ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    debug_log(f"/start from {message.from_user.id}")
    msg = "💖 Welcome! Please choose your language:"
    bot.send_message(message.chat.id, msg, reply_markup=get_language_buttons())

# === /setnames command ===
@bot.message_handler(commands=['setnames'])
def set_names(message):
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            bot.send_message(message.chat.id, "Usage: /setnames [your_name] [his_name]")
            return

        user_id = str(message.from_user.id)
        user_names[user_id] = {
            'girl': args[0],
            'boy': args[1]
        }
        save_data()
        lang = user_languages.get(user_id, 'en')
        response = f"✅ Names updated!\nYou: {args[0]}\nHim: {args[1]}" if lang == "en" else f"✅ ስሞች ተቀይረዋል!\nአንቺ: {args[0]}\nእሱ: {args[1]}"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        debug_log(f"Setnames Error: {str(e)}")

# === Handle button clicks ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    try:
        user_id = str(call.from_user.id)
        lang = call.data.split("_")[1]
        user_languages[user_id] = lang
        save_data()
        bot.answer_callback_query(call.id, text="Language set!")
        text = "🌹 Speak your heart!\nTo change names: /setnames yourname hisname" if lang == "en" else "🌹 ልብህን ንገርኝ!\nስሞችን ለመቀየር: /setnames አንቺ እና እሱ"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        debug_log(f"Callback Error: {str(e)}")

# === Main message handler ===
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    lang = user_languages.get(user_id)

    if not lang:
        bot.send_message(message.chat.id, "💬 Choose your language:", reply_markup=get_language_buttons())
        return

    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(min(max(1, len(message.text) / 20), 3))
    reply = ask_romantic_ai(message.text, lang, user_id)
    bot.send_message(message.chat.id, reply)

# === Start polling ===
if __name__ == "__main__":
    debug_log("✅ Bot is running in production mode.")
    while True:
        try:
            bot.polling(none_stop=True, timeout=30)
        except Exception as e:
            debug_log(f"Polling Error: {e}")
            time.sleep(10)
