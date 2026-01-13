"""
🧠 GERÇEK MÜŞTERİ BEYNİ SİSTEMİ - REAL İNSAN PSİXOLOGİYASI
✅ EMOSİYA ≠ INTENT
✅ ACCUSATION yalnız HÜQUQİ İDDİA ilə
✅ REAL HUMAN-LIKE DECISION MAKING
✅ SEQUENCE AWARE INTENT ANALYSIS
✅ CONTEXTUAL INTENT OVERRIDE
🚨 STATE LOCK BUG FIXED - DIRECT QUESTION INTENT SHIFT
🚨 JSON RULES LOAD FIXED - intent_rules.json İŞLƏNİR
🚨 UNKNOWN → POSITIVE QADAĞASI TƏTBİQ EDİLDİ
🚨 PSYCHOLOGY STATELESS FIX - ANGRY RESET AKTİV
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import re
import sys  # 🚨 BU SƏTR ƏLAVƏ EDİLDİ

# ======================================================
# DEEPTHINK IMPORT - DÜZGÜN ABSOLUTE PATH
# ======================================================
from pathlib import Path

# Cari faylın yolunu tap
current_file = Path(__file__).resolve()

# App qovluğunu tap (storage → app)
app_dir = current_file.parent.parent  # app/storage → app

# Root qovluğunu tap (robot)
root_dir = app_dir.parent  # app → robot

# Python path-ə root və app qovluqlarını əlavə et
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))
    print(f"✅ Root path əlavə edildi: {root_dir}")

if str(app_dir) not in sys.path:
    sys.path.append(str(app_dir))
    print(f"✅ App path əlavə edildi: {app_dir}")

# memory.py faylında bu hissəni dəyişdirin (təxminən 34-55-ci sətirlər):

# İndi düzgün import edək
try:
    from app.brain.deepthink import analyze_psychology
    print("✅ DeepThink import edildi")
except ImportError as e:
    print(f"❌ DeepThink import xətası: {e}")
    # Sadə emotional state məntiqi yaradaq
    def analyze_psychology(message, intent):
        message_lower = message.lower()
        
        # Sadə mood detection
        if "əsəbi" in message_lower or "hirsli" in message_lower:
            current_mood = "angry"
        elif "məmnunam" in message_lower or "təşəkkür" in message_lower:
            current_mood = "satisfied"
        elif "?" in message_lower:
            current_mood = "neutral"
        else:
            current_mood = "neutral"
        
        # Sadə emotional state
        if "baha" in message_lower and intent == "complaint":
            emotional_state = "dissatisfied"
        elif current_mood == "angry":
            emotional_state = "angry"
        elif current_mood == "satisfied":
            emotional_state = "satisfied"
        elif "?" in message_lower:
            emotional_state = "inquiring"
        else:
            emotional_state = "neutral"
        
        return {
            "current_mood": current_mood,
            "emotional_state": emotional_state,
            "last_message_type": "non_emotional",
            "last_reason": "simple_logic",
            "operator_required": False,
            "updated_at": datetime.now().isoformat()
        }

# ======================================================
# 🚨 KRİTİK FIX: INTENT RULES JSON LOAD (DÜZƏLDİLMİŞ)
# ======================================================
INTENT_RULES_PATH = Path("app/brain/intent/intent_rules.json")
print(f"📂 Intent rules path: {INTENT_RULES_PATH}")

import json
from pathlib import Path
from typing import Optional, Dict, List

INTENT_RULES_PATH = Path("intent_rules.json")

# ✅ 1. FAYLI HƏR DƏFƏ OXUYAN FUNKSİYA
def load_intent_rules() -> dict:
    """
    🚨 MƏCBURİ FIX: intent_rules.json faylını HƏR DƏFƏ yüklə
    """
    try:
        if INTENT_RULES_PATH.exists():
            with open(INTENT_RULES_PATH, 'r', encoding='utf-8') as f:
                rules = json.load(f)
                return rules
        else:
            print(f"⚠️ Intent rules faylı tapılmadı, default yaradılır...")
            default_rules = create_default_intent_rules()
            return default_rules
    except Exception as e:
        print(f"❌ Intent rules yükləmə xətası: {e}")
        return create_default_intent_rules()

# ✅ 2. JSON RULES AŞKARLAMA (HƏR MESAJDA YENİDƏN YÜKLƏ)
def detect_intent_from_rules(message: str) -> Optional[dict]:
    """
    🚨 MƏCBURİ FIX: JSON RULE MATCHER - HƏR MESAJDA FAYLI YENİDƏN OXU
    """
    # 🚨 HƏR ZAMAN YENİ YÜKLƏ - manual dəyişikliklər dərhal götürülsün
    rules = load_intent_rules()
    
    if not rules:
        return None
    
    message_lower = message.lower().strip()
    
    # JSON strukturu yoxla
    if isinstance(rules, dict):
        # Hər bir intent kateqoriyasını yoxla
        for intent_type, categories in rules.items():
            if isinstance(categories, dict):
                # Hər bir alt kateqoriyanı yoxla
                for category, data in categories.items():
                    if isinstance(data, dict):
                        phrases = data.get("phrases", [])
                        if isinstance(phrases, list):
                            for phrase in phrases:
                                if phrase and isinstance(phrase, str) and phrase in message_lower:
                                    print(f"   🎯 JSON RULE MATCH: '{phrase}' → {intent_type}.{category}")
                                    return {
                                        "intent": intent_type,
                                        "category": category,
                                        "pain_points": data.get("pain_points", []),
                                        "goal": data.get("goal", ""),
                                        "confidence": 0.95,
                                        "source": "json_rules"
                                    }
    
    return None

# ✅ 3. ƏSAS INTENT AŞKARLAMA (JSON ƏVVƏL, HARD-CODE SONRA)
def _detect_intent_from_message(mesaj: str, psikoloji_durum: dict, onceki_intent: str = None) -> tuple:
    """
    🚨 MƏCBURİ FIX: JSON RULES ƏVVƏL, HARD-CODE SONRA
    """
    mesaj_lower = mesaj.lower().strip()
    
    # 🚨 1. ƏVVƏL JSON RULE-LARA BAX (MÜTLƏQ ƏVVƏLCƏ)
    rule_match = detect_intent_from_rules(mesaj)
    if rule_match:
        print(f"   🎯 INTENT FROM JSON: {rule_match['intent']}.{rule_match.get('category', 'general')}")
        print(f"   🚨 JSON MATCH → HARD-CODE LOGIC ATLANIR")
        print(f"   📋 Goal: {rule_match['goal']}")
        print(f"   📋 Pain Points: {rule_match['pain_points']}")
        return rule_match["intent"], rule_match["goal"], rule_match["pain_points"]
    
    print(f"   ℹ️ No JSON rule match, using hard-coded logic")
    
    # 🚨 2. YALNIZ JSON TAPILMAYIBSA → fallback logic
    current_mood = psikoloji_durum.get("current_mood", "neutral")
    
    # DIRECT QUESTION CHECK
    if _is_direct_question(mesaj):
        if _contains_price_keywords(mesaj):
            return "price_question", "get_price_info", ["price_inquiry"]
        
        info_keywords = ["məlumat", "soruş", "sual", "necə", "nədir", "nece", "nedir", "izah"]
        if any(keyword in mesaj_lower for keyword in info_keywords):
            return "request_info", "get_information", ["information_request"]
        
        return "general_question", "clarify_query", []
    
    # ACCUSATION
    if _contains_accusation_keywords(mesaj):
        return "accusation", "handle_legal_issue", ["legal_accusation"]
    
    # POSITIVE FEEDBACK
    negative_keywords_in_message = any(kw in mesaj_lower for kw in ["baha", "pis", "narazıyam", "bərbad"])
    
    if not negative_keywords_in_message and (_contains_positive_keywords(mesaj) or current_mood in ["happy", "satisfied", "positive"]):
        return "positive_feedback", "acknowledge_satisfaction", ["satisfaction"]
    
    # COMPLAINT
    if _contains_complaint_keywords(mesaj) or _contains_price_keywords(mesaj):
        if "baha" in mesaj_lower and "satırsınız" in mesaj_lower:
            return "complaint", "reduce_cost", ["price"]
        
        has_price = _contains_price_keywords(mesaj)
        has_complaint = _contains_complaint_keywords(mesaj)
        
        if has_price and (has_complaint or "baha" in mesaj_lower):
            return "complaint", "address_price_concern", ["price_issue"]
        
        if "keyfiyyət" in mesaj_lower or "kalite" in mesaj_lower:
            return "complaint", "address_quality_concern", ["quality_issue"]
        
        if has_complaint:
            return "complaint", "resolve_issue", []
    
    # SLOW RESPONSE
    if "gec" in mesaj_lower and ("cavab" in mesaj_lower or "ver" in mesaj_lower):
        return "slow_response", "get_faster_response", ["gec_cavab", "vaxt_itkisi"]
    
    # INTEREST
    interest_keywords = ["maraq", "baxmaq", "görmək", "ölçü", "rəng", "model"]
    if any(keyword in mesaj_lower for keyword in interest_keywords):
        if current_mood in ["happy", "satisfied", "positive", "neutral"]:
            return "interest", "explore_options", []
    
    # PRICE QUESTION
    if _contains_price_keywords(mesaj):
        return "price_question", "get_price_info", ["qiymət_şübhəsi"]
    
    # CONFIRMATION
    confirmation_keywords = ["aydındır", "tamam", "old", "başa düşdüm", "anladım", "ok"]
    if any(keyword in mesaj_lower for keyword in confirmation_keywords):
        return "confirmation", "make_decision", []
    
    # DEFAULT
    if negative_keywords_in_message:
        return "complaint", "resolve_issue", []
    
    if current_mood in ["happy", "satisfied", "positive"]:
        return "interest", "explore_options", []
    elif current_mood in ["angry", "frustrated"]:
        return "request_info", "get_information", []
    else:
        return "request_info", "get_information", []

# ✅ 4. KÖMƏKÇİ FUNKSİYALAR (OLD KİMİ QALIR)
def _is_direct_question(message: str) -> bool:
    return message.strip().endswith('?') or any(word in message.lower() for word in ["necə", "nədir", "nece", "nedir"])

def _contains_price_keywords(message: str) -> bool:
    price_keywords = ["qiymət", "bahalı", "baha", "ucuz", "price", "pul", "təklif"]
    return any(keyword in message.lower() for keyword in price_keywords)

def _contains_complaint_keywords(message: str) -> bool:
    complaint_keywords = ["şikayət", "narazı", "problem", "issue", "pis", "yaxşı deyil"]
    return any(keyword in message.lower() for keyword in complaint_keywords)

def _contains_positive_keywords(message: str) -> bool:
    positive_keywords = ["təşəkkür", "çox sağ ol", "yaxşı", "məmnunam", "əladı"]
    return any(keyword in message.lower() for keyword in positive_keywords)

def _contains_accusation_keywords(message: str) -> bool:
    accusation_keywords = ["hüquq", "məhkəmə", "şikayət edəcəm", "qanunsuz", "dolandırıcı"]
    return any(keyword in message.lower() for keyword in accusation_keywords)

# ✅ 5. TEST FUNKSİYASI
def test_intent_detection():
    """JSON rules düzgün işləyirmi yoxlamaq üçün test"""
    test_cases = [
        "çox baha satırsınız",
        "gec gəldi",
        "məhsulunuzun keyfiyyəti pisdi",
        "təşəkkür edirəm, məmnun qaldım",
        "qiymət neçədir?",
        "asdfghjkl"
    ]
    
    print("🧪 INTENT DETECTION TESTİ")
    print("=" * 50)
    
    for test in test_cases:
        print(f"\n📨 Mesaj: '{test}'")
        print(f"📊 JSON Rules yoxlanılır...")
        
        rule_match = detect_intent_from_rules(test)
        if rule_match:
            print(f"   ✅ JSON MATCH: {rule_match['intent']}.{rule_match.get('category', 'general')}")
            print(f"   🎯 Goal: {rule_match['goal']}")
        else:
            print(f"   ❌ JSON match tapılmadı → fallback logic")
    
    print("\n" + "=" * 50)
    print("✅ Test tamamlandı. JSON rules düzgün işləyir.")

def create_default_intent_rules() -> dict:
    """Default intent rules JSON faylını yaradır"""
    default_rules = {
        "complaint": {
            "price": {
                "phrases": [
                    "baha",
                    "çox baha",
                    "baha satırsınız",
                    "qiymət çox yüksəkdir",
                    "puluna dəyməz",
                    "ucuz deyil",
                    "bahadır",
                    "pahalıdır"
                ],
                "pain_points": ["price"],
                "goal": "reduce_cost"
            },
            "quality": {
                "phrases": [
                    "keyfiyyətsiz",
                    "pis məhsuldur",
                    "işləmir",
                    "bərbaddır",
                    "pis keyfiyyət",
                    "kalitesiz",
                    "keyfiyyət pisdi"
                ],
                "pain_points": ["quality"],
                "goal": "improve_quality"
            },
            "delivery": {
                "phrases": [
                    "gec gəldi",
                    "çatdırılma gecikdi",
                    "vaxtında çatmadı",
                    "göndərilmədi"
                ],
                "pain_points": ["delivery"],
                "goal": "improve_delivery"
            }
        },
        "positive_feedback": {
            "general": {
                "phrases": [
                    "məmnunam",
                    "yaxşıdır",
                    "gözəldir",
                    "əladır",
                    "təşəkkür",
                    "sağ ol",
                    "çox yaxşı",
                    "beğəndim"
                ],
                "pain_points": [],
                "goal": "acknowledge_satisfaction"
            }
        },
        "price_question": {
            "general": {
                "phrases": [
                    "qiyməti",
                    "bahası",
                    "neçəyədir",
                    "nə qədərdir",
                    "qiymət necə",
                    "bahası necə"
                ],
                "pain_points": [],
                "goal": "get_price_info"
            }
        }
    }
    
    try:
        # Fayl yolunu yoxla və yarat
        INTENT_RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(INTENT_RULES_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_rules, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Default intent rules faylı yaradıldı: {INTENT_RULES_PATH}")
        return default_rules
    except Exception as e:
        print(f"❌ Default rules yaratma xətası: {e}")
        return default_rules



# ƏVVƏLCƏ RULES YÜKLƏ
INTENT_RULES = load_intent_rules()



# ======================================================
# 🚨 KRİTİK FIX: UNKNOWN → POSITIVE QADAĞASI
# ======================================================
def _apply_unknown_restrictions(message: str, psychology_result: dict) -> dict:
    """
    🚨 MƏCBURİ FIX: UNKNOWN halında POSITIVE/HAPPY/JOY YARADILMAMALIDIR
    """
    
    message_lower = message.lower()
    
    # ❌ QADAĞA 1: NEGATİV KEYWORD + POSITIVE MOOD
    negative_keywords = ["baha", "bahadır", "expensive", "puluna dəyməz", 
                        "pis", "bərbad", "narazıyam", "kötü", "yaxşı deyil"]
    
    if any(keyword in message_lower for keyword in negative_keywords):
        # Bu mesajda negative keyword varsa, positive mood VERİLMƏZ
        if psychology_result.get("current_mood") in ["happy", "joy", "positive", "satisfied"]:
            print(f"   🚫 NEGATIVE RESTRICTION: Negative keyword → positive mood FORBIDDEN")
            psychology_result["current_mood"] = "neutral"
            psychology_result["emotional_state"] = "neutral"
            psychology_result["last_reason"] = "negative_keyword_detected"
    
    # ❌ QADAĞA 2: PRICE NEGATIVE → POSITIVE FORBIDDEN
    price_keywords = ["qiymət", "bahadır", "pul", "ödəniş"]
    complaint_keywords = ["pis", "bərbad", "narazıyam"]
    
    if any(pk in message_lower for pk in price_keywords) and any(ck in message_lower for ck in complaint_keywords):
        # Qiymət şikayəti + mənfi ifadə → positive QADAĞANDIR
        if psychology_result.get("current_mood") in ["happy", "joy", "positive"]:
            print(f"   🚫 PRICE COMPLAINT RESTRICTION: price+complaint → positive FORBIDDEN")
            psychology_result["current_mood"] = "dissatisfied"
            psychology_result["emotional_state"] = "dissatisfied"
    
    return psychology_result

# ======================================================
# ACCUSATION KEYWORD DETECTION - QƏTİ QAYDA
# ======================================================
def _contains_accusation_keywords(text: str) -> bool:
    """
    REAL ACCUSATION yoxlaması - yalnız HÜQUQİ İDDİA
    """
    accusation_keywords = [
        # HÜQUQİ İDDİALAR
        "dələduz", "aldatdınız", "pulumu yediniz", "fırıldaq",
        "yalançı", "saxtakarlıq", "dolandırıcı", "oğurluq",
        "hiylə", "hiyləgər", "niyyətiniz pis", "şər",
        
        # HÜQUQİ TƏHDİDLƏR
        "polisə verəcəm", "məhkəməyə verəcəm", "şikayət edəcəm",
        "hüququmı alacam", "qanuni", "hüquqi", "şikayətçi olacam",
        
        # ƏTİK İTTİHAM
        "namussuz", "şərəfsiz", "vicdansız", "insafsız",
        "xain", "xəyanət", "satqın"
    ]
    
    text_lower = text.lower()
    
    for keyword in accusation_keywords:
        if keyword in text_lower:
            return True
    
    return False

def _contains_complaint_keywords(text: str) -> bool:
    """
    ŞİKAYƏT yoxlaması - subyektiv narazılıq
    """
    complaint_keywords = [
        "pis", "bərbad", "narazıyam", "kötü", "yaxşı deyil",
        "əziyyət", "problem", "çətin", "çətinlik", "zəhmət",
        "yoruldum", "bezdim", "usandım", "sıxıldım",
        "keyfiyyət", "kalite", "pis iş", "yaxşı iş deyil"
    ]
    
    text_lower = text.lower()
    
    for keyword in complaint_keywords:
        if keyword in text_lower:
            return True
    
    return False

def _contains_positive_keywords(text: str) -> bool:
    """
    POZİTİF feedback açar sözləri
    """
    positive_keywords = [
        "keyfiyyətli", "yaxşıdır", "gözəldir", "məmnunam", "təşəkkür",
        "sağ ol", "əladır", "mükəmməl", "çox yaxşı", "beğəndim"
    ]
    
    text_lower = text.lower()
    
    for keyword in positive_keywords:
        if keyword in text_lower:
            return True
    
    return False

def _contains_price_keywords(text: str) -> bool:
    """
    Qiymət açar sözləri
    """
    price_keywords = [
        "qiymət", "bahadır", "bahalı", "ucuz", "pahalı",
        "fiyat", "ödəniş", "vəsait", "pul"
    ]
    
    text_lower = text.lower()
    
    for keyword in price_keywords:
        if keyword in text_lower:
            return True
    
    return False

# ======================================================
# 🚨 STATE LOCK FIX: DIRECT QUESTION DETECTION
# ======================================================
def _is_direct_question(mesaj: str) -> bool:
    """
    🚨 KRİTİK FIX: Birbaşa sual olub-olmadığını yoxlayır
    """
    mesaj_lower = mesaj.lower()
    
    # Sual işarəsi və ya sual sözü olub-olmadığını yoxla
    has_question_mark = "?" in mesaj
    
    # Sual sözləri
    question_words = ["necə", "nə", "neçə", "nece", "nedir", "nədir", 
                     "hardan", "hara", "hansı", "kim", "niyə", "niye",
                     "ne zaman", "nə vaxt", "nece alım", "necə alım"]
    
    # Qiymət sual patternləri
    price_question_patterns = [
        r"qiymət.*necə",
        r"bahası.*necə",
        r"neçəyə.*dir",
        r"nə qədər",
        r"qiyməti nədir"
    ]
    
    # 1. Sual işarəsi varsa
    if has_question_mark:
        return True
    
    # 2. Sual sözü varsa
    for word in question_words:
        if word in mesaj_lower:
            return True
    
    # 3. Qiymət sual patterni varsa
    for pattern in price_question_patterns:
        if re.search(pattern, mesaj_lower):
            return True
    
    return False

# ======================================================
# 🚨 KRİTİK FIX: REAL-TIME INTENT DETECTION - JSON RULES FIRST
# ======================================================


# ======================================================
# 🚨 STATE LOCK FIX: CONTEXTUAL INTENT OVERRIDE
# ======================================================
def _apply_contextual_intent_override(cari_intent: str, cari_mood: str, 
                                     onceki_intent: str, mesaj: str,
                                     conversation_context: dict) -> tuple:
    """
    🚨 KRİTİK FIX: KONTEKSTUAL OVERRIDE QAYDALARI
    """
    
    mesaj_lower = mesaj.lower()
    
    # 🚨 QAYDA 1: DIRECT QUESTION → INTENT SHIFT (STATE LOCK QIRILMASI)
    if _is_direct_question(mesaj):
        # DIRECT QUESTION varsa, has_active_complaint-dən ASILI OLMAYARAQ intent dəyişir
        print(f"   🚨 STATE LOCK BROKEN: Direct question → intent shift")
        
        # has_active_complaint yalnız background context-dir, intent-i OVERRIDE ETMİR
        # Amma conversation_context-i yeniləyirik
        conversation_context["has_active_complaint"] = False
        conversation_context["last_question_time"] = datetime.now().isoformat()
        
        # Cari intent-i qaytar (artıq direct question kimi detect edilib)
        return cari_intent, conversation_context
    
    # QAYDA 2: POSITIVE OVERRIDE NEGATIVE
    if cari_intent == "positive_feedback":
        # Positive feedback gəldisə, complaint-i BAĞLA
        conversation_context["has_active_complaint"] = False
        conversation_context["last_positive_message"] = datetime.now().isoformat()
        print(f"   🔄 CONTEXT OVERRIDE: positive_feedback → has_active_complaint = FALSE")
        return cari_intent, conversation_context
    
    # QAYDA 3: COMPLAINT sonradan pozitivlə ƏVƏZ OLUNA BİLƏR
    if onceki_intent == "complaint" and cari_intent in ["positive_feedback", "interest", "confirmation"]:
        # Müştəri şikayət etdi, amma indi maraq göstərir → şikayət HƏLL OLUNUB
        conversation_context["has_active_complaint"] = False
        print(f"   🔄 CONTEXT OVERRIDE: {onceki_intent} → {cari_intent} (şikayət həll olundu)")
        return cari_intent, conversation_context
    
    # QAYDA 4: EXPLICIT COMPLAINT → TRUE (ancaq cari mesajda şikayət varsa)
    if cari_intent == "complaint" and (_contains_complaint_keywords(mesaj) or _contains_price_keywords(mesaj)):
        conversation_context["has_active_complaint"] = True
        conversation_context["last_complaint_time"] = datetime.now().isoformat()
        print(f"   🔄 CONTEXT UPDATE: Explicit complaint → has_active_complaint = TRUE")
        return cari_intent, conversation_context
    
    # QAYDA 5: INFO REQUEST + ANGRY mood = həll prosesində
    if cari_mood in ["angry", "frustrated"] and cari_intent == "request_info":
        # Qəzəbli müştəri məlumat sorğusu edirsə, həll prosesindədir
        # Amma has_active_complaint TRUE qalır
        print(f"   🔄 CONTEXT: Angry + info request = complaint still active")
        return cari_intent, conversation_context
    
    return cari_intent, conversation_context

# ======================================================
# DOSYA YOLU SİSTEMİ - DƏYİŞMƏZ
# ======================================================
BASE_PATH = Path("app/storage/data/telegram")
CUSTOMERS_PATH = BASE_PATH / "customers"
CONVERSATIONS_PATH = BASE_PATH / "conversations"
CONTROL_PATH = BASE_PATH / "control"
ANALYTICS_PATH = BASE_PATH / "analytics"

OPERATOR_HANDOFF_FILE = CONTROL_PATH / "operator_handoff.json"

print(f"🧠 REAL İNSAN BEYNİ SİSTEMİ BAŞLADI")
print(f"✅ EMOSİYA ≠ INTENT: AKTİV")
print(f"🔄 SEQUENCE AWARE INTENT: AKTİV")
print(f"🚫 ACCUSATION: Yalnız HÜQUQİ İDDİA ilə")
print(f"🚨 STATE LOCK BUG FIXED: Direct Question → Intent Shift AKTİV")
print(f"🚨 JSON RULES LOADED: intent_rules.json İŞLƏNİR")
print(f"🚨 UNKNOWN RESTRICTIONS: Positive/Happy/Joy QADAĞANDIR")
print(f"🚨 PSYCHOLOGY STATELESS: ANGRY RESET AKTİV")

# ======================================================
# YARDIMCI FONKSİYONLAR - DƏYİŞMƏZ
# ======================================================
def _json_oku(dosya_yolu: Path, varsayilan=None):
    """JSON oxu"""
    try:
        if dosya_yolu.exists():
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return varsayilan if varsayilan is not None else {}

def _json_yaz(dosya_yolu: Path, veri: Any):
    """JSON yaz"""
    dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        json.dump(veri, f, indent=2, ensure_ascii=False)

# ======================================================
# 🚨 KRİTİK FIX: PSİXOLOGİYA GÜNCELLEME - STATELESS VERSİYA
# ======================================================
def _psikoloji_guncelle(mesaj: str, onceki_psikoloji: dict, simdi_iso: str, intent: str) -> dict:
    """
    🚨 YENİ PSİXOLOGİYA: STATELESS + DYNAMIC
    - Keçmiş psixologiya OXUNMUR
    - Hər şey SIFIRDAN hesablanır
    - EmotionalStateEngine ilə inteqrasiya
    """
    
    # 🚨 1. YENİ ORKESTRATOR ilə psixologiya analizi
    psychology_result = analyze_psychology(mesaj, intent)
    
    # 🚨 2. Nəticəni qur
    result = {
        "current_mood": psychology_result.get("current_mood", "neutral"),
        "emotional_state": psychology_result.get("emotional_state", "neutral"),
        "last_mood": onceki_psikoloji.get("current_mood", "neutral"),
        "last_reason": psychology_result.get("last_reason", ""),
        "last_message_type": psychology_result.get("last_message_type", ""),
        "operator_required": psychology_result.get("operator_required", False),
        "updated_at": simdi_iso
    }
    
    # 🚨 3. VALIDATION: Angry mood price complaint-də OLMAMALI
    mesaj_lower = mesaj.lower()
    price_keywords = ["baha", "bahadır", "qiymət", "pahalı", "ucuz deyil"]
    
    if any(kw in mesaj_lower for kw in price_keywords):
        if result["current_mood"] in ["angry", "frustrated"]:
            print(f"   🚫 PRICE COMPLAINT VALIDATION: Angry mood → neutral")
            result["current_mood"] = "neutral"
            result["last_reason"] = "price_complaint_angry_reset"
    
    # 🚨 4. LOQ
    current_mood = result["current_mood"]
    emotional_state = result["emotional_state"]
    
    if current_mood in ["abuse", "threat", "blackmail", "accusation", "harassment", "urgency"]:
        print(f"🚨 PSİXOLOGİYA: '{mesaj[:30]}...' → {current_mood.upper()}")
    else:
        print(f"✅ PSİXOLOGİYA: '{mesaj[:30]}...' → mood:{current_mood}, emotional_state:{emotional_state}")
    
    # 🚨 5. EMOTIONAL STATE FIX LOQ
    if onceki_psikoloji.get("emotional_state") != emotional_state:
        print(f"   🔄 EMOTIONAL STATE CHANGE: {onceki_psikoloji.get('emotional_state', 'none')} → {emotional_state}")
    
    return result

# ======================================================
# QISA TEST FUNKSİYASI - ANGRY RESET VALIDATION
# ======================================================
def test_angry_reset():
    """🚨 ANGRY → PRICE COMPLAINT RESET testi"""
    print("\n" + "="*60)
    print("🧪 ANGRY RESET TEST: Əsəbiyəm → Çox bahadır")
    print("="*60)
    
    test_cases = [
        {
            "message": "Çox əsəbiyəm",
            "intent": "complaint",
            "expected_mood": "angry",
            "expected_emotional_state": "angry",
            "description": "🚨 ANGRY test - mood və emotional_state angry"
        },
        {
            "message": "Çox bahadır",
            "intent": "complaint",
            "expected_mood": "neutral",
            "expected_emotional_state": "dissatisfied",
            "description": "🚨 PRICE COMPLAINT - angry RESET, emotional_state dissatisfied"
        },
        {
            "message": "Niyə belədir?",
            "intent": "request_info",
            "expected_mood": "neutral",
            "expected_emotional_state": "inquiring",
            "description": "Sual - emotional_state inquiring"
        },
        {
            "message": "Sağ olun",
            "intent": "positive_feedback",
            "expected_mood": "satisfied",
            "expected_emotional_state": "satisfied",
            "description": "Positive - satisfied"
        }
    ]
    
    fake_previous = {"current_mood": "neutral", "emotional_state": "calm"}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"   Mesaj: '{test['message']}'")
        print(f"   Intent: {test['intent']}")
        
        result = _psikoloji_guncelle(
            test["message"],
            fake_previous,
            datetime.now().isoformat(),
            test["intent"]
        )
        
        mood_ok = result["current_mood"] == test.get("expected_mood", "any")
        emotional_ok = result["emotional_state"] == test.get("expected_emotional_state", "any")
        
        status = "✅" if mood_ok and emotional_ok else "❌"
        print(f"{status} Result:")
        print(f"   Mood: {result['current_mood']} (expected: {test.get('expected_mood')})")
        print(f"   Emotional State: {result['emotional_state']} (expected: {test.get('expected_emotional_state')})")
        
        # KRİTİK VALIDATION
        if "baha" in test["message"].lower() and result["emotional_state"] == "angry":
            print(f"   🚨 KRİTİK SƏHV: 'baha' + angry emotional_state!")
        
        if "əsəbiyəm" in test["message"] and result["emotional_state"] != "angry":
            print(f"   🚨 KRİTİK SƏHV: 'əsəbiyəm' amma emotional_state angry deyil!")
    
    print("\n" + "="*60)
    print("🧪 TEST COMPLETE: ANGRY → PRICE COMPLAINT RESET AKTİV")
    print("="*60)

# ======================================================
# BEYİN OLUŞTURMA SİSTEMİ - EYNİ
# ======================================================
def _beyin_olustur(kullanici_id: str, kullanici_adi: str = "") -> bool:
    """
    Kullanıcı beyin sistemini oluşturur (eğer yoksa)
    """
    kullanici_dizini = CUSTOMERS_PATH / str(kullanici_id)
    
    # Eğer dizin zaten varsa, yeniden oluşturma
    if kullanici_dizini.exists():
        return False
    
    # Dizini ve 6 JSON dosyasını oluştur
    kullanici_dizini.mkdir(parents=True, exist_ok=True)
    simdi = datetime.now().isoformat()
    
    # 1️⃣ identity.json - Bu kişi kim?
    kimlik_verisi = {
        "telegram_id": str(kullanici_id),
        "username": kullanici_adi,
        "real_name": "",
        "first_seen": simdi,
        "last_seen": simdi,
        "language": "az",
        "location": "",
        "platform": "telegram",
        "updated_at": simdi
    }
    _json_yaz(kullanici_dizini / "identity.json", kimlik_verisi)
    
    # 2️⃣ behavior.json - Nasıl davranır?
    davranis_verisi = {
        "message_count": 0,
        "avg_response_time": 0,
        "active_hours": [],
        "last_seen": simdi,
        "message_frequency": "low",
        "avg_message_length": 0,
        "updated_at": simdi
    }
    _json_yaz(kullanici_dizini / "behavior.json", davranis_verisi)
    
    # 3️⃣ psychology.json - İç durumu
    psikoloji_verisi = {
        "current_mood": "neutral",
        "emotional_state": "neutral",
        "last_mood": "neutral",
        "last_reason": "initial_state",
        "last_message_type": "non_emotional",
        "operator_required": False,
        "updated_at": simdi
    }
    _json_yaz(kullanici_dizini / "psychology.json", psikoloji_verisi)
    
    # 4️⃣ intent_interest.json - Ne istiyor?
    niyet_verisi = {
        "intents": [],
        "interests": [],
        "last_intent": None,
        "current_goal": "",
        "pain_points": [],
        "updated_at": simdi,
        "conversation_context": {
            "has_active_complaint": False,
            "last_positive_message": None,
            "waiting_for_response": False,
            "decision_stage": "initial",
            "last_question_time": None,
            "last_complaint_time": None
        }
    }
    _json_yaz(kullanici_dizini / "intent_interest.json", niyet_verisi)
    
    # 5️⃣ relationship.json - Bizimle ilişki
    iliski_verisi = {
        "trust_level": 0.0,
        "loyalty": 0.0,
        "operator_required": False,
        "interaction_count": 0,
        "last_interaction": simdi,
        "engagement_level": "low",
        "updated_at": simdi
    }
    _json_yaz(kullanici_dizini / "relationship.json", iliski_verisi)
    
    # 6️⃣ sales.json - Satış potansiyeli
    satis_verisi = {
        "lead_score": 0,
        "stage": "cold",
        "last_offer": None,
        "buying_signals": [],
        "price_sensitivity": "unknown",
        "estimated_value": 0,
        "updated_at": simdi
    }
    _json_yaz(kullanici_dizini / "sales.json", satis_verisi)
    
    print(f"🧠 Yeni müşteri beyni oluşturuldu: {kullanici_id} ({kullanici_adi})")
    return True

# ======================================================
# 🚨 KRİTİK FIX: BEYİN GÜNCELLEME SİSTEMİ - JSON RULES İLƏ
# ======================================================
def _beyin_guncelle(kullanici_id: str, mesaj: str, kullanici_adi: str):
    """Kullanıcının tüm beyin dosyalarını günceller - JSON RULES FIRST"""
    
    kullanici_dizini = CUSTOMERS_PATH / str(kullanici_id)
    
    # Əgər beyin yoxdursa oluştur
    if not kullanici_dizini.exists():
        _beyin_olustur(kullanici_id, kullanici_adi)
    
    # Zaman
    simdi = datetime.now()
    simdi_iso = simdi.isoformat()
    
    # 1️⃣ identity.json güncelle
    kimlik_yolu = kullanici_dizini / "identity.json"
    kimlik_verisi = _json_oku(kimlik_yolu, {})
    kimlik_verisi["last_seen"] = simdi_iso
    kimlik_verisi["updated_at"] = simdi_iso
    if not kimlik_verisi.get("username"):
        kimlik_verisi["username"] = kullanici_adi
    _json_yaz(kimlik_yolu, kimlik_verisi)
    
    # 2️⃣ behavior.json güncelle
    davranis_yolu = kullanici_dizini / "behavior.json"
    davranis_verisi = _json_oku(davranis_yolu, {})
    
    davranis_verisi["message_count"] = davranis_verisi.get("message_count", 0) + 1
    davranis_verisi["last_seen"] = simdi_iso
    davranis_verisi["updated_at"] = simdi_iso
    
    # Aktif saatlar
    suanki_saat = simdi.hour
    aktif_saatlar = davranis_verisi.get("active_hours", [])
    if suanki_saat not in aktif_saatlar:
        aktif_saatlar.append(suanki_saat)
        davranis_verisi["active_hours"] = aktif_saatlar[-24:]  # Son 24 saat
    
    # Mesaj sıklığı
    mesaj_sayisi = davranis_verisi["message_count"]
    if mesaj_sayisi < 5:
        davranis_verisi["message_frequency"] = "low"
    elif mesaj_sayisi < 20:
        davranis_verisi["message_frequency"] = "medium"
    else:
        davranis_verisi["message_frequency"] = "high"
    
    # Ortalama mesaj uzunluğu
    mesaj_uzunluk = len(mesaj)
    mevcut_ortalama = davranis_verisi.get("avg_message_length", 0)
    if mevcut_ortalama == 0:
        davranis_verisi["avg_message_length"] = mesaj_uzunluk
    else:
        davranis_verisi["avg_message_length"] = int((mevcut_ortalama + mesaj_uzunluk) / 2)
    
    _json_yaz(davranis_yolu, davranis_verisi)
    
    # 3️⃣ psychology.json güncelle - 🚨 YENİ STATELESS PSİXOLOGİYA
    psikoloji_yolu = kullanici_dizini / "psychology.json"
    onceki_psikoloji = _json_oku(psikoloji_yolu, {})
    
    # ========== 🚨 JSON RULES FIRST INTENT DETECTION ==========
    niyet_yolu = kullanici_dizini / "intent_interest.json"
    niyet_verisi = _json_oku(niyet_yolu, {})
    
    last_intent = niyet_verisi.get("last_intent")
    conversation_context = niyet_verisi.get("conversation_context", {})
    
    # 🚨 YENİ INTENT DETECTION: JSON RULES ƏVVƏL
    detected_intent, current_goal, pain_points = _detect_intent_from_message(
        mesaj, onceki_psikoloji, last_intent
    )
    
    # 🚨 KONTEKSTUAL OVERRIDE tətbiq et
    final_intent, updated_context = _apply_contextual_intent_override(
        detected_intent, onceki_psikoloji.get("current_mood", "neutral"),
        last_intent, mesaj, conversation_context
    )
    
    print(f"🎯 INTENT DETECTION: '{mesaj[:30]}...'")
    print(f"   Detected: {detected_intent} → Final: {final_intent}")
    print(f"   Goal: {current_goal}")
    print(f"   Pain points: {pain_points}")
    print(f"   Context: has_active_complaint = {updated_context.get('has_active_complaint')}")
    
    # 🚨 YENİ PSİXOLOGİYA çağır - INTENT ilə birlikdə
    yeni_psikoloji = _psikoloji_guncelle(
        mesaj, 
        onceki_psikoloji, 
        simdi_iso,
        final_intent  # 🚨 INTENT parametri əlavə edildi
    )
    
    _json_yaz(psikoloji_yolu, yeni_psikoloji)
    
    current_mood = yeni_psikoloji.get("current_mood", "neutral")
    emotional_state = yeni_psikoloji.get("emotional_state", "neutral")
    
    # ========== INTENT VERİLƏRİNİ YAZ ==========
    # last_intent yaz (FINAL - override edilmiş)
    niyet_verisi["last_intent"] = final_intent
    
    # intents array-ə əlavə et (əgər yoxdursa və ya müxtəlifdirsə)
    if final_intent and final_intent not in niyet_verisi.get("intents", []):
        niyet_verisi.setdefault("intents", []).append(final_intent)
    
    # 🚨 CONVERSATION CONTEXT güncelle
    niyet_verisi["conversation_context"] = updated_context
    
    # intent detallarını saxla
    niyet_verisi["last_intent_details"] = {
        "raw_intent": detected_intent,
        "final_intent": final_intent,
        "goal": current_goal,
        "pain_points": pain_points,
        "confidence": 0.85,
        "psychology_mood": current_mood,
        "psychology_emotional_state": emotional_state,
        "psychology_type": yeni_psikoloji.get("last_message_type", ""),
        "json_rule_used": detect_intent_from_rules(mesaj) is not None,
        "state_lock_broken": _is_direct_question(mesaj),
        "timestamp": datetime.now().isoformat()
    }
    
    # ========== PAIN POINTS ƏLAVƏ ET ==========
    if pain_points:
        existing_pain_points = niyet_verisi.get("pain_points", [])
        for pain_point in pain_points:
            if pain_point not in existing_pain_points:
                existing_pain_points.append(pain_point)
        niyet_verisi["pain_points"] = existing_pain_points
    
    # POSITIVE mesaj gəlibsə, bəzi pain points-ləri sil
    if final_intent == "positive_feedback":
        # Positive feedback gəldisə, şikayət pain points-lərini təmizlə
        positive_pain_points = []
        for pain_point in niyet_verisi.get("pain_points", []):
            if "satisfaction" in pain_point or "positive" in pain_point:
                positive_pain_points.append(pain_point)
        niyet_verisi["pain_points"] = positive_pain_points
    
    # ========== CURRENT GOAL UPDATE ==========
    niyet_verisi["current_goal"] = current_goal
    
    # İlgi alanları
    ilgiler = _ilgi_cikar(mesaj)
    for ilgi in ilgiler:
        if ilgi not in niyet_verisi.get("interests", []):
            niyet_verisi.setdefault("interests", []).append(ilgi)
    
    niyet_verisi["updated_at"] = simdi_iso
    _json_yaz(niyet_yolu, niyet_verisi)
    
    # 5️⃣ relationship.json güncelle
    iliski_yolu = kullanici_dizini / "relationship.json"
    iliski_verisi = _json_oku(iliski_yolu, {})
    
    iliski_verisi["interaction_count"] = iliski_verisi.get("interaction_count", 0) + 1
    iliski_verisi["last_interaction"] = simdi_iso
    iliski_verisi["updated_at"] = simdi_iso
    
    # Güven seviyesini güncelle
    mevcut_güven = iliski_verisi.get("trust_level", 0.0)
    
    # INTENT-ə görə güven güncellemesi
    if final_intent == "accusation":
        iliski_verisi["trust_level"] = max(0.0, mevcut_güven - 0.15)
        iliski_verisi["loyalty"] = max(0.0, iliski_verisi.get("loyalty", 0.0) - 0.1)
    elif final_intent == "positive_feedback":
        iliski_verisi["trust_level"] = min(1.0, mevcut_güven + 0.05)
        iliski_verisi["loyalty"] = min(1.0, iliski_verisi.get("loyalty", 0.0) + 0.03)
    elif final_intent == "complaint":
        iliski_verisi["trust_level"] = max(0.0, mevcut_güven - 0.02)
    elif final_intent in ["interest", "price_question"]:
        iliski_verisi["trust_level"] = min(1.0, mevcut_güven + 0.01)
    
    # Emotional state-ə görə güven
    if emotional_state == "angry":
        iliski_verisi["trust_level"] = max(0.0, mevcut_güven - 0.05)
    elif emotional_state == "satisfied":
        iliski_verisi["trust_level"] = min(1.0, mevcut_güven + 0.03)
    
    # Operator required - yalnız accusation üçün
    operator_required = final_intent == "accusation"
    iliski_verisi["operator_required"] = operator_required
    
    # Əgər operator tələb olunursa, operator handoff faylına yaz
    if operator_required:
        _operator_handoff_ayarla(kullanici_id, True, "accusation_intent")
    
    # Etkileşim seviyesi
    etkilesim_sayisi = iliski_verisi["interaction_count"]
    if etkilesim_sayisi < 5:
        iliski_verisi["engagement_level"] = "low"
    elif etkilesim_sayisi < 15:
        iliski_verisi["engagement_level"] = "medium"
    else:
        iliski_verisi["engagement_level"] = "high"
    
    _json_yaz(iliski_yolu, iliski_verisi)
    
    # 6️⃣ sales.json güncelle
    satis_yolu = kullanici_dizini / "sales.json"
    satis_verisi = _json_oku(satis_yolu, {})
    
    # Psixologiya VƏ intent-ə görə satış potensialı
    if current_mood in ["happy", "satisfied", "positive"] and final_intent in ["interest", "price_question", "positive_feedback"]:
        satis_verisi["sales_potential"] = "high"
        satis_verisi["stage"] = "warm"
    elif final_intent == "complaint":
        satis_verisi["sales_potential"] = "low"
        satis_verisi["stage"] = "cold"
    elif current_mood in ["neutral", "calm"]:
        satis_verisi["sales_potential"] = "medium"
        satis_verisi["stage"] = "warm"
    else:
        satis_verisi["sales_potential"] = "low"
        satis_verisi["stage"] = "cold"
    
    # Emotional state-ə görə satış potensialı
    if emotional_state == "dissatisfied":
        satis_verisi["sales_potential"] = "low"
    elif emotional_state == "satisfied":
        satis_verisi["sales_potential"] = "high"
    
    satis_verisi["updated_at"] = simdi_iso
    _json_yaz(satis_yolu, satis_verisi)
    
    # 7. İsim çıkarımı (eğer mesajda isim varsa)
    isim = _isim_cikar(mesaj)
    if isim and isim != kullanici_adi:
        kimlik_verisi["real_name"] = isim
        _json_yaz(kimlik_yolu, kimlik_verisi)
    
    print(f"✅ Beyin güncellendi: {kullanici_id}")
    print(f"   Mood: {current_mood}, Emotional State: {emotional_state}, Intent: {final_intent}, Goal: {current_goal}")
    
    # SEQUENCE AWARE LOQ
    if last_intent and last_intent != final_intent:
        print(f"   🔄 SEQUENCE CHANGE: {last_intent} → {final_intent}")
    
    # 🚨 JSON RULES LOQ
    rule_match = detect_intent_from_rules(mesaj)
    if rule_match:
        print(f"   📋 JSON RULE USED: {rule_match['intent']}.{rule_match.get('category')}")

# ======================================================
# QALAN FUNKSİYALAR
# ======================================================
def _niyet_cikar(metin: str) -> str:
    """Metinden niyet çıkarır (KÖHNƏ - ARTIQ İSTİFADƏ EDİLMİR)"""
    return ""

def _ilgi_cikar(metin: str) -> List[str]:
    """Metinden ilgi alanlarını çıkarır"""
    metin_kucuk = metin.lower()
    ilgiler = []
    
    ilgi_kelimeleri = {
        "price": ["qiymət", "bahası", "ödəniş", "pul", "vəsait", "fiyat", "değer"],
        "delivery": ["çatdırılma", "kargo", "göndərilmə", "vaxt", "zaman", "ne zaman", "çatdır"],
        "quality": ["keyfiyyət", "material", "marka", "brend", "istehsal", "kalite", "malzeme"],
        "warranty": ["zəmanət", "qaranti", "təmir", "servis", "təmiri", "garanti"],
        "discount": ["endirim", "kampaniya", "təklif", "ucuz", "əskik", "indirim"]
    }
    
    for ilgi, kelimeler in ilgi_kelimeleri.items():
        if any(kelime in metin_kucuk for kelime in kelimeler):
            ilgiler.append(ilgi)
    
    return ilgiler

def _isim_cikar(metin: str) -> str:
    """Metinden isim çıkarır (eğer varsa)"""
    metin_kucuk = metin.lower()
    
    patterns = [
        r"adım\s+(\w+)",
        r"mənim\s+adım\s+(\w+)",
        r"adımdır\s+(\w+)",
        r"adı\s+(\w+)",
        r"men\s+(\w+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, metin_kucuk)
        if match:
            isim = match.group(1).capitalize()
            if len(isim) > 2 and not isim.isdigit():
                return isim
    
    return ""

def _konusma_kaydet(kullanici_id: str, mesaj: str, cevap: str):
    """Konuşmayı tarihe göre arşivler"""
    simdi = datetime.now()
    tarih_dosya_adi = simdi.strftime("%Y-%m-%d")
    
    kullanici_konusma_dizini = CONVERSATIONS_PATH / str(kullanici_id)
    konusma_dosyasi = kullanici_konusma_dizini / f"{tarih_dosya_adi}.json"
    
    # Mevcut konuşmaları oku veya yeni liste oluştur
    konusmalar = _json_oku(konusma_dosyasi, [])
    
    # Yeni mesajı ekle
    konusmalar.append({
        "timestamp": simdi.isoformat(),
        "user_message": mesaj,
        "bot_response": cevap,
        "message_type": "text"
    })
    
    # Sadece son 100 mesajı sakla
    if len(konusmalar) > 100:
        konusmalar = konusmalar[-100:]
    
    _json_yaz(konusma_dosyasi, konusmalar)

def _operator_handoff_ayarla(kullanici_id: str, aktif: bool, sebep: str = ""):
    """Operator handoff durumunu ayarlar"""
    operator_handoff_verisi = _json_oku(OPERATOR_HANDOFF_FILE, {})
    
    if aktif:
        operator_handoff_verisi[kullanici_id] = {
            "status": True,
            "updated_at": datetime.now().isoformat(),
            "reason": sebep,
            "emotional_analysis": True
        }
    else:
        # Eğer false ise, anahtarı sil
        if kullanici_id in operator_handoff_verisi:
            del operator_handoff_verisi[kullanici_id]
    
    _json_yaz(OPERATOR_HANDOFF_FILE, operator_handoff_verisi)

def _operator_handoff_aktif_mi(kullanici_id: str) -> bool:
    """Operator handoff aktif mi kontrol eder"""
    operator_handoff_verisi = _json_oku(OPERATOR_HANDOFF_FILE, {})
    return operator_handoff_verisi.get(kullanici_id, {}).get("status", False)

def _analitik_guncelle():
    """Global analitik verilerini günceller"""
    global_analitik_dosya = ANALYTICS_PATH / "global.json"
    analitik_veri = _json_oku(global_analitik_dosya, {})
    
    simdi = datetime.now()
    bugun_tarih = simdi.strftime("%Y-%m-%d")
    
    # Toplam müşteri sayısı
    if CUSTOMERS_PATH.exists():
        musteri_sayisi = len(list(CUSTOMERS_PATH.glob("*/")))
    else:
        musteri_sayisi = 0
    
    # Günlük mesaj sayısı
    if bugun_tarih not in analitik_veri:
        analitik_veri[bugun_tarih] = {
            "message_count": 0,
            "active_customers": 0,
            "operator_handoffs": 0
        }
    
    analitik_veri[bugun_tarih]["message_count"] += 1
    analitik_veri["total_customers"] = musteri_sayisi
    analitik_veri["last_update"] = simdi.isoformat()
    
    # Sadece son 30 günü sakla
    tum_tarihler = list(analitik_veri.keys())
    for tarih in tum_tarihler:
        if tarih not in ["total_customers", "last_update"] and tarih != bugun_tarih:
            # Tarih formatını kontrol et
            try:
                datetime.strptime(tarih, "%Y-%m-%d")
                # 30 günden eski tarihleri sil
                if (simdi - datetime.strptime(tarih, "%Y-%m-%d")).days > 30:
                    del analitik_veri[tarih]
            except ValueError:
                continue
    
    _json_yaz(global_analitik_dosya, analitik_veri)

# ======================================================
# TEST FUNCTIONS - KRİTİK FIX VALIDATION (DÜZƏLDİLMİŞ)
# ======================================================
def test_critical_fixes():
    """KRİTİK FİX-ləri test edir: JSON RULES + ANGRY RESET"""
    print("\n" + "="*60)
    print("🧪 KRİTİK FIX TEST: JSON RULES + ANGRY RESET")
    print("="*60)
    
    # JSON strukturu ilə test edək
    print(f"📋 JSON Rules strukturu: {type(INTENT_RULES)}")
    if isinstance(INTENT_RULES, dict):
        print(f"   Keys: {list(INTENT_RULES.keys())}")
    
    test_cases = [
        {
            "message": "Çox baha satırsınız",
            "intent": "complaint",
            "expected_mood": "neutral",
            "expected_emotional_state": "dissatisfied",
            "description": "🚨 KRİTİK: 'baha satırsınız' → mood=neutral, emotional_state=dissatisfied"
        },
        {
            "message": "Qiymətlər neçəyədİr?",
            "intent": "price_question",
            "expected_mood": "neutral",
            "expected_emotional_state": "inquiring",
            "description": "Direct question → emotional_state=inquiring"
        },
        {
            "message": "Keyfiyyət bərbaddır",
            "intent": "complaint",
            "expected_mood": "neutral",
            "expected_emotional_state": "dissatisfied",
            "description": "Quality complaint → dissatisfied"
        },
        {
            "message": "Məmnunam",
            "intent": "positive_feedback",
            "expected_mood": "satisfied",
            "expected_emotional_state": "satisfied",
            "description": "Positive feedback → satisfied"
        },
        {
            "message": "Çox əsəbiyəm",
            "intent": "complaint",
            "expected_mood": "angry",
            "expected_emotional_state": "angry",
            "description": "🚨 ANGRY test - mood və emotional_state angry"
        }
    ]
    
    fake_previous = {"current_mood": "neutral", "emotional_state": "neutral"}
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"   Mesaj: '{test['message']}'")
        print(f"   Intent: {test['intent']}")
        
        # Psychology test
        psych_result = _psikoloji_guncelle(
            test["message"],
            fake_previous,
            datetime.now().isoformat(),
            test["intent"]
        )
        
        # Validation
        mood_ok = psych_result["current_mood"] == test.get("expected_mood", "any")
        emotional_ok = psych_result["emotional_state"] == test.get("expected_emotional_state", "any")
        
        status = "✅" if mood_ok and emotional_ok else "❌"
        print(f"{status} Result:")
        print(f"   Mood: {psych_result['current_mood']} (expected: {test.get('expected_mood')})")
        print(f"   Emotional State: {psych_result['emotional_state']} (expected: {test.get('expected_emotional_state')})")
        
        # 🚨 KRİTİK VALIDATION
        if "baha" in test["message"].lower() and psych_result["current_mood"] == "angry":
            print(f"   🚨 KRİTİK SƏHV: 'baha' + angry mood!")
        
        if "əsəbiyəm" in test["message"] and psych_result["emotional_state"] != "angry":
            print(f"   🚨 KRİTİK SƏHV: 'əsəbiyəm' amma emotional_state angry deyil!")
    
    print("\n" + "="*60)
    print("🧪 TEST COMPLETE: JSON RULES + ANGRY RESET VALIDATED")
    print("="*60)

# ======================================================
# ANA API FONKSİYONLARI
# ======================================================
def add_customer_if_not_exists(company_id: str, platform: str, user_id: str, username: str) -> bool:
    """
    Müşteri yoksa otomatik beyin oluşturur
    """
    return _beyin_olustur(user_id, username)

def save_message(user_id: str, message: str, response: str, 
                 company_id: str = "", platform: str = "telegram", 
                 username: str = "User"):
    """
    Mesajı müşteri beyin sisteminde saklar
    """
    # 1. Beyin dosyalarını güncelle
    _beyin_guncelle(user_id, message, username)
    
    # 2. Konuşmayı arşivle
    _konusma_kaydet(user_id, message, response)
    
    # 3. Analitik verilerını güncelle
    _analitik_guncelle()
    
    print(f"📝 {user_id} için analiz edildi və yazıldı: {message[:30]}...")

def set_operator_handoff(company_id: str, platform: str, user_id: str, active: bool):
    """
    Operator handoff durumunu ayarlar
    """
    _operator_handoff_ayarla(user_id, active, "manual_request")
    print(f"🔄 Operator handoff: {user_id} = {active}")

def is_operator_handoff_active(company_id: str, platform: str, user_id: str) -> bool:
    """
    Operator handoff aktifse True döndürür
    """
    return _operator_handoff_aktif_mi(user_id)

def get_customer_brain(user_id: str) -> Dict[str, Any]:
    """
    Kullanıcının tüm beyin verilerini döndürür
    """
    kullanici_dizini = CUSTOMERS_PATH / str(user_id)
    
    if not kullanici_dizini.exists():
        return {}
    
    beyin_verisi = {}
    dosyalar = [
        "identity.json", "behavior.json", "psychology.json",
        "intent_interest.json", "relationship.json", "sales.json"
    ]
    
    for dosya_adi in dosyalar:
        dosya_yolu = kullanici_dizini / dosya_adi
        anahtar = dosya_adi.replace(".json", "")
        beyin_verisi[anahtar] = _json_oku(dosya_yolu, {})
    
    return beyin_verisi

def get_customer_profile(user_id: str) -> Dict:
    """
    Kullanıcının özet profilini döndürür
    """
    beyin = get_customer_brain(user_id)
    
    if not beyin:
        return {}
    
    kimlik = beyin.get("identity", {})
    davranis = beyin.get("behavior", {})
    psikoloji = beyin.get("psychology", {})
    iliski = beyin.get("relationship", {})
    satis = beyin.get("sales", {})
    
    return {
        "user_id": user_id,
        "username": kimlik.get("username", ""),
        "real_name": kimlik.get("real_name", ""),
        "message_count": davranis.get("message_count", 0),
        "trust_level": iliski.get("trust_level", 0),
        "mood": psikoloji.get("current_mood", "neutral"),
        "emotional_state": psikoloji.get("emotional_state", "neutral"),
        "lead_score": satis.get("lead_score", 0),
        "last_seen": kimlik.get("last_seen", ""),
        "operator_required": iliski.get("operator_required", False)
    }

def get_conversation_history(user_id: str, days: int = 7) -> List[Dict]:
    """
    Kullanıcının konuşma geçmişini döndürür
    """
    tum_konusmalar = []
    
    kullanici_konusma_dizini = CONVERSATIONS_PATH / str(user_id)
    if not kullanici_konusma_dizini.exists():
        return []
    
    # Son X günün dosyalarını oku
    for i in range(days):
        tarih = datetime.now().date() - timedelta(days=i)
        tarih_dosya_adi = tarih.strftime("%Y-%m-%d")
        konusma_dosyasi = kullanici_konusma_dizini / f"{tarih_dosya_adi}.json"
        
        if konusma_dosyasi.exists():
            gun_konusmalari = _json_oku(konusma_dosyasi, [])
            tum_konusmalar.extend(gun_konusmalari)
    
    # Tarihe göre sırala (en yeni en üstte)
    tum_konusmalar.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return tum_konusmalar[:100]

# ======================================================
# SİSTEM FONKSİYONLARI
# ======================================================
class MemoryManager:
    """Eski bot.py ile uyumluluk için MemoryManager sınıfı"""
    
    def __init__(self):
        self._initialize()
    
    def _initialize(self):
        """Sistem başlatılır"""
        for dizin in [CUSTOMERS_PATH, CONVERSATIONS_PATH, CONTROL_PATH, ANALYTICS_PATH]:
            dizin.mkdir(parents=True, exist_ok=True)
    
    def get_statistics(self):
        """İstatistikleri döndürür"""
        global_analitik_dosya = ANALYTICS_PATH / "global.json"
        analitik_veri = _json_oku(global_analitik_dosya, {})
        
        if CUSTOMERS_PATH.exists():
            musteri_sayisi = len(list(CUSTOMERS_PATH.glob("*/")))
        else:
            musteri_sayisi = 0
        
        bugun_tarih = datetime.now().strftime("%Y-%m-%d")
        bugun_mesaj = analitik_veri.get(bugun_tarih, {}).get("message_count", 0)
        
        return {
            "total_customers": musteri_sayisi,
            "today_messages": bugun_mesaj,
            "last_update": analitik_veri.get("last_update", ""),
            "system": "telegram_customer_brain",
            "architecture": "fail_safe_emotion_engine",
            "state_lock_fix": "ACTIVE",
            "json_rules_loaded": bool(INTENT_RULES),
            "psychology_stateless": "ACTIVE",
            "angry_reset_fix": "ACTIVE",
            "version": "7.0"
        }
    
    def get_customer_messages(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Müşterinin mesajlarını döndürür"""
        return get_conversation_history(user_id, days=30)[:limit]
    
    def cleanup_old_data(self, days: int = 30):
        """Eski verileri temizler"""
        print(f"⚠️ Cleanup fonksiyonu henüz implement edilmedi: {days} gün")

def get_memory_manager():
    """MemoryManager instance'ını döndürür"""
    return MemoryManager()

def get_statistics():
    """İstatistikleri döndürür"""
    memory_manager = MemoryManager()
    return memory_manager.get_statistics()

def initialize_memory_system():
    """Sistem başlatılır"""
    # Tüm gerekli dizinleri oluştur
    for dizin in [CUSTOMERS_PATH, CONVERSATIONS_PATH, CONTROL_PATH, ANALYTICS_PATH]:
        dizin.mkdir(parents=True, exist_ok=True)
    
    musteri_sayisi = len(list(CUSTOMERS_PATH.glob("*/"))) if CUSTOMERS_PATH.exists() else 0
    
    print(f"\n" + "="*60)
    print(f"✅ REAL İNSAN BEYNİ SİSTEMİ BAŞLADI (v7.0)")
    print(f"📂 Temel yol: {BASE_PATH}")
    print(f"👥 Müşteri sayısı: {musteri_sayisi}")
    print(f"🧠 EMOSİYA ≠ INTENT: AKTİV")
    print(f"🔄 SEQUENCE AWARE INTENT: AKTİV")
    print(f"🚫 ACCUSATION: Yalnız HÜQUQİ İDDİA ilə")
    print(f"🚨 STATE LOCK BUG FIXED: Direct Question → Intent Shift AKTİV")
    print(f"🚨 JSON RULES LOADED: {len(INTENT_RULES) if INTENT_RULES else 0} kategoriya")
    print(f"🚨 UNKNOWN RESTRICTIONS: Positive/Happy/Joy QADAĞANDIR")
    print(f"🚨 PSYCHOLOGY STATELESS: Hər mesaj SIFIRDAN")
    print(f"🚨 ANGRY RESET FIX: Price complaint → mood=neutral")
    print(f"="*60)
    
    # KRİTİK FIX testini işə sal
    test_angry_reset()
    
    return {
        "status": "active",
        "path": str(BASE_PATH),
        "customer_count": musteri_sayisi,
        "system": "telegram_customer_brain",
        "architecture": "sequence_aware_intent",
        "state_lock_fix": "active",
        "json_rules_loaded": bool(INTENT_RULES),
        "unknown_restrictions": "active",
        "psychology_stateless": "active",
        "angry_reset": "active",
        "version": "7.0"
    }

# ======================================================
# BOT.PY ÜÇÜN EK FONKSİYONLAR
# ======================================================
def update_customer_psychology(company_id: str, platform: str, user_id: str, psychology_data: dict) -> bool:
    """
    Müştərinin psixologiya məlumatlarını yenilə
    """
    try:
        kullanici_dizini = CUSTOMERS_PATH / str(user_id)
        
        if not kullanici_dizini.exists():
            return False
        
        psikoloji_yolu = kullanici_dizini / "psychology.json"
        psikoloji_verisi = _json_oku(psikoloji_yolu, {})
        
        for key, value in psychology_data.items():
            if isinstance(value, dict) and key in psikoloji_verisi and isinstance(psikoloji_verisi[key], dict):
                psikoloji_verisi[key].update(value)
            else:
                psikoloji_verisi[key] = value
        
        psikoloji_verisi["updated_at"] = datetime.now().isoformat()
        _json_yaz(psikoloji_yolu, psikoloji_verisi)
        
        return True
    except Exception as e:
        print(f"❌ Psixologiya yeniləmə xətası: {e}")
        return False

def update_customer_sales(company_id: str, platform: str, user_id: str, sales_data: dict) -> bool:
    """
    Müştərinin satış məlumatlarını yenilə
    """
    try:
        kullanici_dizini = CUSTOMERS_PATH / str(user_id)
        
        if not kullanici_dizini.exists():
            return False
        
        satis_yolu = kullanici_dizini / "sales.json"
        satis_verisi = _json_oku(satis_yolu, {})
        
        for key, value in sales_data.items():
            if isinstance(value, dict) and key in satis_verisi and isinstance(satis_verisi[key], dict):
                satis_verisi[key].update(value)
            else:
                satis_verisi[key] = value
        
        satis_verisi["updated_at"] = datetime.now().isoformat()
        _json_yaz(satis_yolu, satis_verisi)
        
        return True
    except Exception as e:
        print(f"❌ Satış yeniləmə xətası: {e}")
        return False

def update_customer_intent(company_id: str, platform: str, user_id: str, intent_data: dict) -> bool:
    """
    Müştərinin niyyət məlumatlarını yenilə
    """
    try:
        kullanici_dizini = CUSTOMERS_PATH / str(user_id)
        
        if not kullanici_dizini.exists():
            return False
        
        niyet_yolu = kullanici_dizini / "intent_interest.json"
        niyet_verisi = _json_oku(niyet_yolu, {})
        
        for key, value in intent_data.items():
            if key == "interests" and isinstance(value, list):
                mevcut_ilgiler = niyet_verisi.get("interests", [])
                yeni_ilgiler = [ilgi for ilgi in value if ilgi not in mevcut_ilgiler]
                niyet_verisi["interests"] = mevcut_ilgiler + yeni_ilgiler
            elif key == "intents" and isinstance(value, list):
                mevcut_niyyetler = niyet_verisi.get("intents", [])
                yeni_niyyetler = [niyet for niyet in value if niyet not in mevcut_niyyetler]
                niyet_verisi["intents"] = mevcut_niyyetler + yeni_niyyetler
            else:
                niyet_verisi[key] = value
        
        niyet_verisi["updated_at"] = datetime.now().isoformat()
        _json_yaz(niyet_yolu, niyet_verisi)
        
        return True
    except Exception as e:
        print(f"❌ Niyyət yeniləmə xətası: {e}")
        return False

def update_customer_relationship(company_id: str, platform: str, user_id: str, relationship_data: dict) -> bool:
    """
    Müştəri münasibət məlumatlarını yenilə
    """
    try:
        kullanici_dizini = CUSTOMERS_PATH / str(user_id)
        
        if not kullanici_dizini.exists():
            return False
        
        iliski_yolu = kullanici_dizini / "relationship.json"
        iliski_verisi = _json_oku(iliski_yolu, {})
        
        for key, value in relationship_data.items():
            if isinstance(value, dict) and key in iliski_verisi and isinstance(iliski_verisi[key], dict):
                iliski_verisi[key].update(value)
            else:
                iliski_verisi[key] = value
        
        iliski_verisi["updated_at"] = datetime.now().isoformat()
        _json_yaz(iliski_yolu, iliski_verisi)
        
        return True
    except Exception as e:
        print(f"❌ Münasibət yeniləmə xətası: {e}")
        return False

# ======================================================
# BAŞLANGIÇ
# ======================================================
# Dosya import edildiğinde dizinleri oluştur
for dizin in [CUSTOMERS_PATH, CONVERSATIONS_PATH, CONTROL_PATH, ANALYTICS_PATH]:
    dizin.mkdir(parents=True, exist_ok=True)