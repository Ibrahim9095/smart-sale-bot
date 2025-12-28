import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# =========================
# PATH SETTINGS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
COMPANIES_FILE = os.path.join(DATA_DIR, "companies.json")

# =========================
# UTILS
# =========================

def _ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for path in [MESSAGES_FILE, CUSTOMERS_FILE, COMPANIES_FILE]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

def _load(path: str) -> List[Dict]:
    _ensure_files()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save(path: str, data: List[Dict]) -> None:
    _ensure_files()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =========================
# MESSAGES
# =========================

def add_message(
    company_id: str,
    platform: str,
    user_id: str,
    role: str,
    text: str,
    username: Optional[str] = None
) -> Dict:
    messages = _load(MESSAGES_FILE)

    message = {
        "id": len(messages) + 1,
        "company_id": company_id,
        "platform": platform,
        "user_id": user_id,
        "username": username,
        "role": role,
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    }

    messages.append(message)
    _save(MESSAGES_FILE, messages)
    return message

def get_messages(
    company_id: Optional[str] = None,
    platform: Optional[str] = None,
    user_id: Optional[str] = None
) -> List[Dict]:
    messages = _load(MESSAGES_FILE)

    if company_id:
        messages = [m for m in messages if m["company_id"] == company_id]
    if platform:
        messages = [m for m in messages if m["platform"] == platform]
    if user_id:
        messages = [m for m in messages if m["user_id"] == user_id]

    return messages

# =========================
# CUSTOMERS
# =========================

def add_customer_if_not_exists(
    company_id: str,
    platform: str,
    user_id: str,
    username: str
) -> Dict:
    customers = _load(CUSTOMERS_FILE)

    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            return c

    customer = {
        "company_id": company_id,
        "platform": platform,
        "user_id": user_id,
        "username": username,
        "created_at": datetime.utcnow().isoformat(),
        "notes": {},
        "psychology": {
            "last_intent": None,
            "active_interest": None,
            "sales_stage": "lead",
            "updated_at": None,
        },
        "interests": [],
    }

    customers.append(customer)
    _save(CUSTOMERS_FILE, customers)
    return customer

def get_customers(company_id: Optional[str] = None) -> List[Dict]:
    customers = _load(CUSTOMERS_FILE)
    if company_id:
        customers = [c for c in customers if c["company_id"] == company_id]
    return customers

# =========================
# INTEREST MEMORY
# =========================

def add_customer_interest(
    company_id: str,
    platform: str,
    user_id: str,
    interest: str
) -> Optional[Dict]:
    customers = _load(CUSTOMERS_FILE)

    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            if interest not in c["interests"]:
                c["interests"].append(interest)

            c["psychology"]["active_interest"] = interest
            c["psychology"]["updated_at"] = datetime.utcnow().isoformat()

            _save(CUSTOMERS_FILE, customers)
            return c
    return None

def get_last_interest(
    company_id: str,
    platform: str,
    user_id: str
) -> Optional[str]:
    customers = _load(CUSTOMERS_FILE)
    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            return c.get("psychology", {}).get("active_interest")
    return None

# =========================
# INTENT
# =========================

def detect_intent(text: str) -> str:
    t = text.lower()

    if any(w in t for w in ["qiymət", "neçədir", "bahadır", "ucuzdur"]):
        return "asking_price"
    if any(w in t for w in ["almaq", "sifariş", "alacam", "götürürəm"]):
        return "buying"
    if any(w in t for w in ["fərqi", "müqayisə", "hansı yaxşıdır"]):
        return "comparing"
    if any(w in t for w in ["narazı", "problem", "şikayət"]):
        return "complaining"

    return "browsing"

def update_customer_intent(
    company_id: str,
    platform: str,
    user_id: str,
    intent: str
) -> Optional[Dict]:
    customers = _load(CUSTOMERS_FILE)

    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            c["psychology"]["last_intent"] = intent
            c["psychology"]["updated_at"] = datetime.utcnow().isoformat()
            _save(CUSTOMERS_FILE, customers)
            return c
    return None

# =========================
# INTEREST DETECTION
# =========================

KEYWORDS = {
    "gödəkçə": ["gödəkçə", "kurtka", "jaket"],
    "ayaqqabı": ["ayaqqabı", "krossovka"],
    "saat": ["saat", "watch"],
    "köynək": ["köynək", "shirt"],
    "şalvar": ["şalvar", "jeans", "cins"],
    "paltar": ["paltar", "dress"],
}

def detect_interest(text: str) -> Optional[str]:
    text = text.lower()
    for interest, words in KEYWORDS.items():
        for w in words:
            if w in text:
                return interest
    return None

# =========================
# 🔥 REFERENTIAL MEMORY (STEP 2.4)
# =========================

REFERENTIAL_KEYWORDS = [
    "bayaq",
    "az əvvəl",
    "dünən",
    "keçən dəfə",
    "əvvəl danışdığımız",
    "danışdığımız məhsul",
    "o məhsul",
]

def is_referencing_previous(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in REFERENTIAL_KEYWORDS)

# =========================
# SALES STAGE
# =========================

def detect_sales_stage(intent: str, active_interest: Optional[str]) -> str:
    if intent == "buying" and active_interest:
        return "ready_to_buy"
    if intent == "asking_price" and active_interest:
        return "decision"
    if active_interest:
        return "interest"
    return "lead"

def update_sales_stage(
    company_id: str,
    platform: str,
    user_id: str,
    stage: str
) -> Optional[Dict]:
    customers = _load(CUSTOMERS_FILE)

    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            c["psychology"]["sales_stage"] = stage
            c["psychology"]["updated_at"] = datetime.utcnow().isoformat()
            _save(CUSTOMERS_FILE, customers)
            return c
    return None

# =========================
# 🔥 HARD RESET ONLY
# =========================

def reset_customer_memory(
    company_id: str,
    platform: str,
    user_id: str
) -> Optional[Dict]:
    customers = _load(CUSTOMERS_FILE)

    for c in customers:
        if c["company_id"] == company_id and c["platform"] == platform and c["user_id"] == user_id:
            c["psychology"]["active_interest"] = None
            c["psychology"]["sales_stage"] = "lead"
            c["psychology"]["last_intent"] = None
            c["psychology"]["updated_at"] = datetime.utcnow().isoformat()
            c["interests"] = []
            _save(CUSTOMERS_FILE, customers)
            return c
    return None

# =========================
# BOT REPLY STRATEGY
# =========================

def build_bot_reply(stage: str, active_interest: Optional[str]) -> str:
    if stage == "lead":
        return "Xoş gəldiniz 👋 Hansı məhsula baxmaq istəyirsiniz?"

    if stage == "interest":
        if active_interest:
            return f"{active_interest.capitalize()} ilə maraqlanırsınız 🙂 Qiymət və modellər barədə deyə bilərəm."
        return "Hansı məhsul sizi maraqlandırır? 🙂"

    if stage == "decision":
        if active_interest:
            return f"{active_interest.capitalize()} üçün qiymətlər modelə görə dəyişir 🙂 Hansı modeli istəyirsiniz?"
        return "Qiymətlər məhsula görə dəyişir 🙂"

    if stage == "ready_to_buy":
        if active_interest:
            return f"Əladır 👍 {active_interest.capitalize()} üçün ölçü və modeli deyin."
        return "Əladır 👍 Hansı məhsulu sifariş edək?"

    return "Necə kömək edə bilərəm? 😊"

# =========================
# COMPANIES
# =========================

def get_company_by_api_key(api_key: str) -> Optional[Dict]:
    companies = _load(COMPANIES_FILE)
    for company in companies:
        if company.get("api_key") == api_key:
            return company
    return None

def get_company_by_id(company_id: str) -> Optional[Dict]:
    companies = _load(COMPANIES_FILE)
    for company in companies:
        if company.get("company_id") == company_id:
            return company
    return None