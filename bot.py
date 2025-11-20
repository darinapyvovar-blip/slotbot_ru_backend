from telebot import TeleBot, types
from datetime import datetime

BOT_TOKEN = "8403462312:AAFciTNi8qENsleBLD1XoPDiPGTUNqfAGYI"
ADMIN_CHANNEL = -1003272918813
PARTNER_LINK = "https://ru-partner-link.com"
WEBAPP_URL = "https://slotgpt-analyzer-wtye.vercel.app/"

bot = TeleBot(BOT_TOKEN)
seen = set()

def log(text):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(ADMIN_CHANNEL, f"{text}\n🕒 {stamp}")

@bot.message_handler(commands=['start'])
def start(msg):
    u = msg.from_user
    if u.id not in seen:
        seen.add(u.id)
        status = "🆕 Новый пользователь"
    else:
        status = "🔁 Повторный вход"

    log(f"{status}\n👤 {u.first_name}\n🆔 {u.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🚀 Начать регистрацию"))

    bot.send_message(msg.chat.id,
                     "Добро пожаловать! Начните регистрацию:",
                     reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "🚀 Начать регистрацию")
def step1(msg):
    u = msg.from_user
    log(f"🟡 Начал регистрацию\n👤 {u.first_name}\n🆔 {u.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("✅ Я зарегистрировался"))

    bot.send_message(msg.chat.id,
                     f"Перейдите по ссылке:\n{PARTNER_LINK}",
                     reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "✅ Я зарегистрировался")
def step2(msg):
    u = msg.from_user
    log(f"🟢 Подтвердил регистрацию\n👤 {u.first_name}\n🆔 {u.id}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("💸 Я внес депозит"))

    bot.send_message(msg.chat.id,
                     "Теперь внесите депозит 💸",
                     reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "💸 Я внес депозит")
def step3(msg):
    u = msg.from_user
    log(f"🟣 Подтвердил депозит\n👤 {u.first_name}\n🆔 {u.id}")

    # ПОПРАВКА: inline кнопка WebApp — правильный способ
    inline = types.InlineKeyboardMarkup()
    inline.add(
        types.InlineKeyboardButton(
            text="🎰 Открыть анализатор",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
    )

    bot.send_message(msg.chat.id,
                     "Доступ открыт 👇",
                     reply_markup=inline)

@bot.message_handler(content_types=['web_app_data'])
def webapp_callback(msg):
    u = msg.from_user
    log(f"🟠 Пользователь открыл WebApp\n👤 {u.first_name}\n🆔 {u.id}")

bot.polling(non_stop=True)
