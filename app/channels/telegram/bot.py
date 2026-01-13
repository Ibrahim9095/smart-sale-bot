"""
🤖 TELEGRAM BOT v2.0
✅ TAM DEEPTHINK INTEGRASIYA
✅ PSİXOLOGİYA + INTENT ANALİZİ
✅ OPERATOR HANDOFF MÜTƏRQİB
"""

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

# 🔹 CORE MEMORY FUNKSİYALARI
from app.storage.memory import (
    add_customer_if_not_exists,
    save_message,
    set_operator_handoff,
    is_operator_handoff_active,
    get_customer_brain,
    get_customer_profile,
    initialize_memory_system
)

# 🔹 DEEPTHINK IMPORT
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from app.brain.deepthink import deepthink
from app.brain.intent.intent_think import intent_think
# 🔹 PROJECT ROOT PATH TAP
ROOT_PATH = Path(__file__).parent.parent.parent  # app/channels/telegram → robot
sys.path.append(str(ROOT_PATH))

print(f"📂 Root path: {ROOT_PATH}")

# İndi import edə bilərik
try:
    from app.brain.deepthink import deepthink
    print("✅ DeepThink import edildi")
except ImportError as e:
    print(f"❌ DeepThink import xətası: {e}")
    exit(1)

try:
    # QEYD: intent_think intent qovluğundadır!
    from app.brain.intent.intent_think import intent_think
    print("✅ IntentThink import edildi")
except ImportError as e:
    print(f"❌ IntentThink import xətası: {e}")
    print("⚠️ Intent sistemi olmadan davam edilir...")
    intent_think = None
# ==============================
# ENV
# ==============================
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPERATOR_CHAT_ID = int(os.getenv("OPERATOR_CHAT_ID", 0))

if not BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN tapılmadı")

# ==============================
# SYSTEM INIT
# ==============================
print("=" * 60)
print("🧠 REAL MÜŞTERİ BEYNİ SİSTEMİ v2.0")
print("✅ DEEPTHINK PSİXOLOGİYA + INTENT AKTİV")
print("❌ UNKNOWN: QADAĞAN EDİLDİ")
print("=" * 60)

# Memory sistemini başlat
initialize_memory_system()

# ==============================
# MENU
# ==============================
CHAT_MENU = ReplyKeyboardMarkup(
    [
        ["❓ Sualım var", "📞 Operatorla danış"],
        ["👋 Sağ ol", "ℹ️ Məlumat"],
        ["📊 Mənim profilim"]
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
    "📞",
    "danışmaq",
    "əlaqə"
]

# ==============================
# RESPONSE SYSTEM v2.0
# ==============================
def generate_smart_response(text: str, psychology: dict = None, intent: dict = None) -> str:
    """
    PSİXOLOGİYA + INTENT əsasında ağıllı cavab
    """
    t = text.lower()
    
    # CRITICAL PSİXOLOGİYA → TEKST ÇOX VACİB
    if psychology:
        current_mood = psychology.get("current_mood", "neutral")
        last_message_type = psychology.get("last_message_type", "")
        
        # 🚨 CRITICAL CATEGORIES
        if last_message_type in ["abuse", "threat", "blackmail", "accusation", "harassment"]:
            return (
                "Bu mövzuda operatorla danışmağınız tövsiyə olunur. "
                "Sizi operatora yönləndirdik, gözləyin."
            )
        
        # ⚠️ URGENCY
        if last_message_type == "urgency":
            return (
                "Anladım, dərhal kömək etməyə çalışıram. "
                "Zəhmət olmassa bir az izah edin."
            )
        
        # 😠 ANGER
        if current_mood == "angry":
            return random.choice([
                "Başa düşürəm, narahat olmağınızı. Birlikdə həll edək.",
                "Sakit olun, sizi anlamağa çalışıram.",
                "Narahat olduğunuzu hiss edirəm. Problem nədir?"
            ])
        
        # 😫 STRESSED
        if current_mood == "stressed":
            return random.choice([
                "Sakit olun, hər şeyi addım-addım həll edək.",
                "Təlaş etməyin, kömək etmək üçün buradayam.",
                "Başa düşürəm, gərgin olduğunuzu hiss edirəm."
            ])
        
        # 😢 SAD
        if current_mood == "sad":
            return random.choice([
                "Üzüldüyünüzü hiss edirəm. Kömək etmək istəyirəm.",
                "Başa düşürəm, kədərli olduğunuzu görürəm.",
                "Yaxşı olacaq, birlikdə həll edərik."
            ])
        
        # 😊 HAPPY / SATISFIED
        if current_mood in ["happy", "satisfied"]:
            return random.choice([
                "Sizin sevinciniz məni də sevindirir! 🎉",
                "Gözəl! Necə kömək edə bilərəm?",
                "Razı qalmağınıza sevindim! 😊"
            ])
    
    # INTENT əsasında cavablar
    if intent:
        intent_type = intent.get("intent", "")
        
        if intent_type == "slow_response":
            return random.choice([
                "Bağışlayın, cavabda gecikdiyimə görə. Dərhal kömək edirəm.",
                "Anladım, gec cavab verdiyim üçün üzr istəyirəm. Nəyə kömək edim?",
                "Səbəb olduğum narahatlığa görə üzr istəyirəm. Necə kömək edə bilərəm?"
            ])
        
        elif intent_type == "accusation":
            return (
                "Bu barədə dərhal operatorla əlaqə saxlamanızı tövsiyə edirəm. "
                "Sizi operatora yönləndirirəm."
            )
        
        elif intent_type == "request_help":
            return random.choice([
                "Kömək etmək üçün buradayam! Problem nədir?",
                "Dərhal kömək edəcəyəm. Zəhmət olmasa izah edin.",
                "Kömək lazım olduğu üçün narahat olmayın, həll edəcəyik."
            ])
        
        elif intent_type == "price_question":
            return random.choice([
                "Qiymət məlumatı üçün xüsusi təkliflərimiz var. Hansı məhsulla maraqlanırsınız?",
                "Qiymətlər məhsul və xidmətlərə görə dəyişir. Daha ətraflı məlumat verə bilərəm.",
                "Ən son qiymətlər üçün sizə kömək edim. Hansı məhsul?"
            ])
        
        elif intent_type == "greeting":
            return random.choice([
                "Salam! Necəsiniz? 😊",
                "Salamlar! Sizə necə kömək edə bilərəm?",
                "Xoş gəlmisiniz! Mən sizə kömək etməyə hazıram."
            ])
        
        elif intent_type == "thanks":
            return random.choice([
                "Rica edirəm! 😊",
                "Hər zaman köməyə hazıram! 🙌",
                "Sağ olun! Əlavə sualınız varsa, soruşun."
            ])
        
        elif intent_type == "confusion":
            return random.choice([
                "Başa düşmədiyinizi anlayıram. Daha sadə izah edim.",
                "Qarışıq olduğunu görürəm. Yenidən izah edim.",
                "Anlamadığınızı hiss edirəm. Başqa cür izah edim."
            ])
    
    # DEFAULT RESPONSES
    if "salam" in t:
        return "Salam! Necəsiniz? Sizə necə kömək edə bilərəm? 😊"
    
    if "sağ ol" in t or "təşəkkür" in t:
        return "Rica edirəm! Əlavə sualınız varsa, soruşun. 🙌"
    
    if "necəsən" in t or "necesen" in t:
        return "Yaxşıyam, təşəkkür edirəm! Siz necəsiniz?"
    
    if "məlumat" in t or "info" in t:
        return "Biz müştəri xidmətləri üçün buradayıq. Hansı mövzuda məlumat lazımdır?"
    
    # FALLBACK RESPONSES
    return random.choice([
        "Anladım. Bir az daha izah edə bilərsinizmi?",
        "Maraqlıdır. Davam edin, dinləyirəm.",
        "Bu barədə düşünürəm. Əlavə məlumat versəniz, kömək edim.",
        "Sizi anlamağa çalışıram. Bir az daha aydınlaşdıra bilərsinizmi?",
        "Qeyd etdiyiniz məsələyə diqqət yetirirəm. Davam edin."
    ])

# ==============================
# MAIN HANDLER v2.0
# ==============================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """TƏK AXIN - DEEPTHINK INTEGRASIYA"""
    message = update.message
    user = update.effective_user

    if not message or not message.text:
        return

    text = message.text.strip()
    if not text:
        return

    # IDENTIFIERS
    company_id = "real_company"
    platform = "telegram"
    user_id = str(user.id)
    username = user.username or user.first_name or "İstifadəçi"
    
    print(f"\n📩 YENİ MESAJ: {user_id} ({username}): {text[:50]}...")

    # 1️⃣ MÜŞTERİ YARAT (ƏGƏR YOXDURSA)
    add_customer_if_not_exists(
        company_id=company_id,
        platform=platform,
        user_id=user_id,
        username=username
    )

    # 2️⃣ OPERATOR AKTİVDİRSƏ → BOT SUSUR
    if is_operator_handoff_active(company_id, platform, user_id):
        print(f"   🤐 OPERATOR MODE: Bot susur")
        return

    # 3️⃣ PSİXOLOGİYA ANALİZİ (DEEPTHINK)
    psychology_result = deepthink.analyze(text)
    
    if psychology_result:
        current_mood = psychology_result.get("current_mood", "neutral")
        last_message_type = psychology_result.get("last_message_type", "")
        operator_required = psychology_result.get("operator_required", False)
        
        print(f"   🧠 PSİXOLOGİYA: {current_mood} ({last_message_type})")
        
        if operator_required:
            print(f"   🚨 CRITICAL: {last_message_type.upper()} → OPERATOR REQUIRED")
    else:
        psychology_result = None
        print(f"   ❓ UNKNOWN PHRASE")
    
    # 4️⃣ INTENT ANALİZİ
    intent_result = None
    if psychology_result:
        intent_result = intent_think.analyze(
            text, 
            psychology_result.get("last_message_type")
        )
        
        if intent_result:
            print(f"   🎯 INTENT: {intent_result.get('intent', 'unknown')}")
    
    # 5️⃣ OPERATOR HANDOFF (CRITICAL PSİXOLOGİYA VƏ YA INTENT)
    should_handoff = False
    handoff_reason = ""
    
    if psychology_result and psychology_result.get("operator_required", False):
        should_handoff = True
        handoff_reason = f"critical_psychology:{psychology_result.get('last_message_type', 'unknown')}"
    
    elif intent_result and intent_result.get("intent") in ["accusation"]:
        should_handoff = True
        handoff_reason = f"critical_intent:{intent_result.get('intent', 'unknown')}"
    
    # 6️⃣ MANUAL OPERATOR REQUEST
    if any(k in text.lower() for k in OPERATOR_KEYWORDS):
        should_handoff = True
        handoff_reason = "manual_request"
    
    # 7️⃣ PROFİL SORĞUSU
    if "profil" in text.lower() or "mənim" in text.lower() and ("məlumat" in text.lower() or "info" in text.lower()):
        profile = get_customer_profile(user_id)
        if profile:
            profile_text = (
                f"👤 SİZİN PROFİLİNİZ:\n"
                f"ID: {profile.get('user_id', 'N/A')}\n"
                f"Ad: {profile.get('real_name', 'N/A')}\n"
                f"İstifadəçi adı: {profile.get('username', 'N/A')}\n"
                f"Mesaj sayı: {profile.get('message_count', 0)}\n"
                f"Son görülmə: {profile.get('last_seen', 'N/A')}\n"
                f"Güvən səviyyəsi: {profile.get('trust_level', 0):.1%}\n"
                f"Mood: {profile.get('mood', 'neutral')}"
            )
            await message.reply_text(profile_text, reply_markup=CHAT_MENU)
            return
    
    # 8️⃣ OPERATOR HANDOFF APPLY
    if should_handoff:
        set_operator_handoff(company_id, platform, user_id, True)
        
        handoff_message = "👨‍💼 Sizi operatora yönləndirdik.\nZəhmət olmasa gözləyin."
        
        # Psychology-a görə xüsusi mesaj
        if psychology_result and psychology_result.get("last_message_type") == "urgency":
            handoff_message = "🆘 Dərhal operatorla əlaqə saxlayırıq. Bir dəqiqə gözləyin."
        
        await message.reply_text(handoff_message, reply_markup=CHAT_MENU)
        
        # Operatora bildiriş
        if OPERATOR_CHAT_ID:
            operator_alert = (
                "🔔 YENİ OPERATOR HANDOFF\n\n"
                f"👤 Müştəri: {username}\n"
                f"🆔 ID: {user_id}\n"
                f"💬 Mesaj: {text}\n"
                f"🧠 Psixologiya: {psychology_result.get('current_mood', 'N/A') if psychology_result else 'N/A'}\n"
                f"🎯 Niyyət: {intent_result.get('intent', 'N/A') if intent_result else 'N/A'}\n"
                f"📋 Səbəb: {handoff_reason}"
            )
            
            try:
                await context.bot.send_message(
                    chat_id=OPERATOR_CHAT_ID,
                    text=operator_alert
                )
                print(f"   📤 Operatora bildiriş göndərildi")
            except Exception as e:
                print(f"   ❌ Operator bildirişi xətası: {e}")
        
        return

    # 9️⃣ THINKING UX (USER EXPERIENCE)
    await context.bot.send_chat_action(
        chat_id=message.chat_id,
        action="typing"
    )
    
    # Psychology-a görə typing vaxtı
    typing_delay = 1.2  # default
    if psychology_result:
        current_mood = psychology_result.get("current_mood", "neutral")
        if current_mood in ["angry", "stressed", "urgency"]:
            typing_delay = 0.8  # Tez cavab
        elif current_mood in ["thinking", "confused"]:
            typing_delay = 2.0  # Daha uzun düşünür
    
    await asyncio.sleep(random.uniform(typing_delay, typing_delay + 0.5))

    # 🔟 SMART RESPONSE GENERATE
    response = generate_smart_response(text, psychology_result, intent_result)
    
    print(f"   🤖 CAVAB: {response[:50]}...")

    # 1️⃣1️⃣ MESSAGE SAVE (PSİXOLOGİYA + INTENT DAXİLİ)
    save_message(
        user_id=user_id,
        message=text,
        response=response,
        company_id=company_id,
        platform=platform,
        username=username
    )

    # 1️⃣2️⃣ SEND RESPONSE
    await message.reply_text(response, reply_markup=CHAT_MENU)

# ==============================
# ERROR HANDLER
# ==============================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xəta idarəetmə"""
    print(f"❌ Xəta: {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Bağışlayın, texniki xəta oldu. Bir az sonra yenidən cəhd edin.",
                reply_markup=CHAT_MENU
            )
        except:
            pass

# ==============================
# START BOT
# ==============================
def main():
    print("🤖 TELEGRAM BOT v2.0 BAŞLADI")
    print("🧠 DEEPTHINK: AKTİV")
    print("🎯 INTENT ANALİZ: AKTİV")
    print("👥 OPERATOR HANDOFF: AKTİV")
    print("=" * 60)

    # HTTPX Request (daha stabil)
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    # Application build
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    # Handlers
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    
    # Error handler
    app.add_error_handler(error_handler)

    # Polling
    print("🔄 Bot polling başladı...")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()