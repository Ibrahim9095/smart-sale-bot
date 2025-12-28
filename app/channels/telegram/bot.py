import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.storage.memory import (
    add_message,
    add_customer_if_not_exists,
    detect_intent,
    update_customer_intent,
    detect_interest,
    add_customer_interest,
    get_customers,
    detect_sales_stage,
    update_sales_stage,
    build_bot_reply,
    reset_customer_memory,
)

# ==============================
# ENV
# ==============================
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN tapılmadı (.env yoxla)")

# ==============================
# SMART RESET CONFIG
# ==============================

SOFT_GREETINGS = [
    "salam",
    "salamlar",
    "salam 🙂",
    "salam 👋",
    "hello",
    "hi",
]

HARD_RESET_KEYWORDS = [
    "başqa məhsul",
    "fikrimi dəyişdim",
    "yenidən başlayaq",
    "yenidən",
    "sıfırla",
    "restart",
]

def detect_reset_type(text: str) -> str:
    t = text.lower().strip()

    for k in HARD_RESET_KEYWORDS:
        if k in t:
            return "hard"

    if t in SOFT_GREETINGS:
        return "soft"

    return "none"

# ==============================
# HANDLER
# ==============================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    company_id = "demo_company"
    platform = "telegram"
    user_id = str(user.id)
    username = user.username or user.first_name or "unknown"

    print("🔥 HANDLE_TEXT:", text)

    # 1️⃣ CUSTOMER tap / yarat
    add_customer_if_not_exists(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        username=username,
    )

    # ==============================
    # 🧠 SMART RESET + CONTEXTUAL SALAM
    # ==============================
    reset_type = detect_reset_type(text)

    customers = get_customers(company_id=company_id)
    last_interest = None

    for c in customers:
        if c["user_id"] == user_id and c["platform"] == platform:
            last_interest = c.get("psychology", {}).get("active_interest")
            break

    # 🔴 HARD RESET
    if reset_type == "hard":
        reset_customer_memory(
            company_id=company_id,
            platform=platform,
            user_id=user_id,
        )

        bot_text = (
            "Oldu 👍\n"
            "İndi yeni mövzudan başlayaq.\n"
            "Hansı məhsula baxmaq istəyirsiniz?"
        )

        add_message(
            company_id=company_id,
            platform=platform,
            user_id="bot",
            role="bot",
            username="SmartSaleBot",
            text=bot_text,
        )

        await update.message.reply_text(bot_text)
        return

    # 🟡 SOFT SALAM – KEÇMİŞİ XATIRLA
    if reset_type == "soft":
        if last_interest:
            bot_text = (
                f"Salam 👋\n"
                f"Bəli, bayaq {last_interest} ilə maraqlanırdınız 🙂\n"
                f"Davam edək?"
            )
        else:
            bot_text = "Salam 👋 Buyurun, necə kömək edə bilərəm? 😊"

        add_message(
            company_id=company_id,
            platform=platform,
            user_id="bot",
            role="bot",
            username="SmartSaleBot",
            text=bot_text,
        )

        await update.message.reply_text(bot_text)
        return

    # ==============================
    # 2️⃣ USER mesajını saxla
    # ==============================
    add_message(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        role="user",
        username=username,
        text=text,
    )

    # ==============================
    # 3️⃣ INTENT
    # ==============================
    intent = detect_intent(text)
    update_customer_intent(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        intent=intent,
    )

    # ==============================
    # 4️⃣ INTEREST
    # ==============================
    active_interest = None

    interest_now = detect_interest(text)
    if interest_now:
        active_interest = interest_now
        add_customer_interest(
            company_id=company_id,
            platform=platform,
            user_id=user_id,
            interest=interest_now,
        )
        print("🎯 ACTIVE INTEREST (new):", active_interest)

    if not active_interest:
        active_interest = last_interest

    # ==============================
    # 5️⃣ SALES STAGE
    # ==============================
    stage = detect_sales_stage(intent, active_interest)
    update_sales_stage(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        stage=stage,
    )
    print("🧭 SALES STAGE:", stage)

    # ==============================
    # 6️⃣ BOT REPLY
    # ==============================
    bot_text = build_bot_reply(stage, active_interest)

    if not bot_text:
        bot_text = "Buyurun 😊 Necə kömək edə bilərəm?"

    # ==============================
    # 7️⃣ BOT mesajını saxla
    # ==============================
    add_message(
        company_id=company_id,
        platform=platform,
        user_id="bot",
        role="bot",
        username="SmartSaleBot",
        text=bot_text,
    )

    await update.message.reply_text(bot_text)

# ==============================
# START
# ==============================
def main():
    print("🤖 Telegram bot START OLDU (SMART CONTEXT BRAIN)")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()