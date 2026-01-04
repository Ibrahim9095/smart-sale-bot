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

# 🔹 MEMORY FUNKSİYALARI
from app.storage.memory import (
    add_customer_if_not_exists,
    save_message,
    set_operator_handoff,
    is_operator_handoff_active,
    update_customer_psychology,
    update_customer_sales,
    update_customer_intent,
    update_customer_relationship,
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
def generate_response(text: str) -> str:
    t = text.lower()

    if "salam" in t:
        return "Salam! Necəsiniz? 😊"
    if "necəsən" in t:
        return "Yaxşıyam, siz necəsiniz?"
    if "sağ ol" in t or "təşəkkür" in t:
        return "Rica edirəm 🙌"

    return random.choice([
        "Sizi anladım. Bir az da izah edə bilərsiniz?",
        "Maraqlıdır. Davam edin.",
        "Bu mövzuda düşünürəm."
    ])

# ==============================
# PSİXOLOJİ ANALİZİ
# ==============================
def analyze_psychology(text: str) -> dict:
    """Mesajdan psixoloji vəziyyəti analiz et"""
    text_lower = text.lower()
    
    anger_words = ["pis", "axmaq", "idiot", "ləğv", "bərbad", "narahat", "acıqlı"]
    anger_level = sum(1 for word in anger_words if word in text_lower)
    
    stress_words = ["kömək", "təcili", "dərhal", "acil", "problem", "çətin"]
    stress_level = sum(1 for word in stress_words if word in text_lower)
    
    positive_words = ["yaxşı", "əla", "mükəmməl", "təşəkkür", "sağ ol", "sevdim"]
    happiness_level = sum(1 for word in positive_words if word in text_lower)
    
    # Ümumi mood
    if anger_level > 2:
        mood = "angry"
    elif stress_level > 2:
        mood = "stressed"
    elif happiness_level > 1:
        mood = "positive"
    else:
        mood = "neutral"
    
    return {
        "current_mood": mood,
        "emotional_state": {
            "anger_level": min(10, anger_level * 2),
            "stress_level": min(10, stress_level * 2),
            "happiness_level": min(10, happiness_level * 3),
            "patience_level": max(1, 5 - anger_level)
        }
    }

# ==============================
# NİYYƏT ANALİZİ
# ==============================
def analyze_intent(text: str) -> dict:
    """Mesajdan niyyəti analiz et"""
    text_lower = text.lower()
    
    intent = "support"
    interests = []
    
    # Satış niyyəti
    sales_words = ["qiymət", "almaq", "satın", "məhsul", "endirim", "kampaniya"]
    if any(word in text_lower for word in sales_words):
        intent = "sales_inquiry"
        interests.append("pricing")
    
    # Problem niyyəti
    problem_words = ["problem", "şikayət", "pis", "kömək", "yararsız"]
    if any(word in text_lower for word in problem_words):
        intent = "complaint"
        interests.append("support")
    
    # Sual niyyəti
    question_words = ["necə", "nə", "niyə", "harda", "nə vaxt", "kim"]
    if any(word in text_lower for word in question_words) or "?" in text:
        intent = "question"
        interests.append("information")
    
    return {
        "current_intent": intent,
        "interests": interests
    }

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

    # 3️⃣ OPERATORA KEÇİD
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

    # 4️⃣ PSİXOLOJİ VƏ NİYYƏT ANALİZİ
    psychology_data = analyze_psychology(text)
    intent_data = analyze_intent(text)
    
    # 5️⃣ SATIŞ POTENSİALI
    customer_brain = get_customer_brain(user_id)
    message_count = customer_brain.get("behavior", {}).get("message_count", 0)
    
    # Lead score hesabla
    lead_score = min(100, message_count * 5)
    if psychology_data["current_mood"] == "positive":
        lead_score += 20
    elif psychology_data["current_mood"] == "angry":
        lead_score -= 30
    
    # Satış məlumatları
    sales_data = {
        "lead_score": lead_score,
        "sales_stage": "warm" if lead_score > 50 else "cold",
        "conversion_likelihood": lead_score
    }
    
    # Münasibət məlumatları
    relationship_data = {
        "satisfaction_level": 7 if psychology_data["current_mood"] == "positive" else 5
    }
    
    # 6️⃣ MEMORY YENİLƏ
    update_customer_psychology(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        psychology_data=psychology_data
    )
    
    update_customer_intent(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        intent_data=intent_data
    )
    
    update_customer_sales(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        sales_data=sales_data
    )
    
    update_customer_relationship(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        relationship_data=relationship_data
    )
    
    # 7️⃣ THINKING UX
    await context.bot.send_chat_action(
        chat_id=message.chat_id,
        action="typing"
    )
    await asyncio.sleep(random.uniform(1.2, 2.0))

    # 8️⃣ RESPONSE
    response = generate_response(text)

    # 9️⃣ MESSAGE SAVE
    save_message(
        user_id=user_id,
        message=text,
        response=response,
        company_id=company_id,
        platform=platform,
        username=username
    )

    # 🔟 SEND
    await message.reply_text(response, reply_markup=CHAT_MENU)

# ==============================
# START
# ==============================
def main():
    print("🤖 BOT STARTED")
    print("🧠 Memory: ACTIVE")
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