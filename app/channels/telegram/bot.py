import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔹 YENİ MEMORY FUNKSİYALARI
from app.storage.memory import (
    add_customer_if_not_exists,
    save_message,
    set_operator_handoff,
    is_operator_handoff_active,
    get_customer_brain
)


# ==============================
# ENV
# ==============================
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPERATOR_CHAT_ID = int(os.getenv("OPERATOR_CHAT_ID", 0))

if not BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN tapılmadı")

# ==============================
# MENU
# ==============================
CHAT_MENU = ReplyKeyboardMarkup(
    [
        ["❓ Sualım var"],
        ["📞 Operatorla danış"],
        ["👋 Sağ ol"]
    ],
    resize_keyboard=True
)

# ==============================
# OPERATOR KEYWORDS
# ==============================
OPERATOR_KEYWORDS = [
    "operator",
    "canlı",
    "insan",
    "menecer",
    "satıcı",
    "📞"
]

# ==============================
# AI RESPONSE (sadə)
# ==============================
def generate_response(text: str, mood: str = "neutral") -> str:
    t = text.lower()

    if "salam" in t:
        return "Salam! Necəsiniz? 😊"
    if "necəsən" in t:
        return "Yaxşıyam, siz necəsiniz?"
    if "sağ ol" in t or "təşəkkür" in t:
        return "Rica edirəm 🙌"
    
    # Mood'a görə cavab
    if mood == "angry":
        return "Başa düşürəm, narahat olmağınızı. Kömək edə bilərəm."
    elif mood == "stressed":
        return "Sakit olun, problemimi həll edək."
    elif mood == "sad":
        return "Üzüldüyünüzü hiss edirəm. Kömək etmək istəyirəm."
    elif mood == "joyful":
        return "Sizin sevinciniz məni də sevindirir! 🎉"

    return random.choice([
        "Sizi anladım. Bir az da izah edə bilərsiniz?",
        "Maraqlıdır. Davam edin.",
        "Bu mövzuda düşünürəm."
    ])

# ==============================
# MAIN HANDLER (TƏK AXIN)
# ==============================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.effective_user

    if not message or not message.text:
        return

    text = message.text.strip()
    if not text:
        return

    company_id = "real_company"
    platform = "telegram"
    user_id = str(user.id)
    username = user.username or user.first_name or "İstifadəçi"

    # 1️⃣ CUSTOMER AUTO-CREATE
    add_customer_if_not_exists(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        username=username
    )

    # 2️⃣ OPERATOR AKTİVDİRSƏ → BOT SUSUR
    if is_operator_handoff_active(company_id, platform, user_id):
        return

    # 3️⃣ OPERATORA KEÇİD (Xüsusi sözlər)
    if any(k in text.lower() for k in OPERATOR_KEYWORDS):
        set_operator_handoff(company_id, platform, user_id, True)

        await message.reply_text(
            "👨‍💼 Sizi operatora yönləndirdik.\n"
            "Zəhmət olmasa gözləyin."
        )

        if OPERATOR_CHAT_ID:
            await context.bot.send_message(
                chat_id=OPERATOR_CHAT_ID,
                text=(
                    "🔔 OPERATOR HANDOFF\n\n"
                    f"👤 {username}\n"
                    f"🆔 {user_id}\n"
                    f"💬 {text}"
                )
            )
        return

    # 4️⃣ PSİXOLOGİYA VƏ NİYYƏT ANALİZİ (DEEPTHINK İLE)
    # Bu artıq save_message daxilində edilir
    
    # 5️⃣ THINKING UX
    await context.bot.send_chat_action(
        chat_id=message.chat_id,
        action="typing"
    )
    await asyncio.sleep(random.uniform(1.2, 2.0))

    # 6️⃣ MOOD'U AL RESPONSE ÜÇÜN
    customer_brain = get_customer_brain(user_id)
    current_mood = customer_brain.get("psychology", {}).get("mood", "neutral")
    
    # 7️⃣ RESPONSE GENERATE
    response = generate_response(text, current_mood)

    # 8️⃣ MESSAGE SAVE (DEEPTHINK ANALİZİ DAXİLİ)
    save_message(
        user_id=user_id,
        message=text,
        response=response,
        company_id=company_id,
        platform=platform,
        username=username
    )

    # 9️⃣ SEND
    await message.reply_text(response, reply_markup=CHAT_MENU)

# ==============================
# START
# ==============================
def main():
    print("🤖 BOT STARTED")
    print("🧠 DEEPTHINK Memory: ACTIVE")
    print("👥 Operator Handoff: ACTIVE")
    print("=" * 40)

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    app.run_polling()

if __name__ == "__main__":
    main()