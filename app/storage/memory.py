"""
🧠 GERÇEK MÜŞTERİ BEYNİ SİSTEMİ - TELEGRAM
✅ Sadece: app/storage/data/telegram/customers/<telegram_user_id>/
✅ Her kullanıcı için 6 JSON: identity, behavior, psychology, intent_interest, relationship, sales
✅ Ayrı kontrol: app/storage/data/telegram/control/operator_handoff.json
❌ HİÇBİR global customer JSON (customers.json, messages.json YOK)
❌ Müşteri içinde control.json YOK
❌ HİÇBİR kök JSON dosyası
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import re

# ======================================================
# DOSYA YOLU SİSTEMİ - KESİN VE DEĞİŞMEZ
# ======================================================
BASE_PATH = Path("app/storage/data/telegram")
CUSTOMERS_PATH = BASE_PATH / "customers"
CONVERSATIONS_PATH = BASE_PATH / "conversations"
CONTROL_PATH = BASE_PATH / "control"
ANALYTICS_PATH = BASE_PATH / "analytics"

OPERATOR_HANDOFF_FILE = CONTROL_PATH / "operator_handoff.json"

print(f"🧠 Müşteri Beyin Sistemi Başlatılıyor: {BASE_PATH}")

# ======================================================
# YARDIMCI FONKSİYONLAR
# ======================================================
def _json_oku(dosya_yolu: Path, varsayilan=None):
    """JSON dosyasını okur, yoksa varsayılan değeri döndürür"""
    try:
        if dosya_yolu.exists():
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return varsayilan if varsayilan is not None else {}

def _json_yaz(dosya_yolu: Path, veri: Any):
    """JSON dosyasına yazar, gerekli dizinleri oluşturur"""
    dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
    with open(dosya_yolu, 'w', encoding='utf-8') as f:
        json.dump(veri, f, indent=2, ensure_ascii=False)

# ======================================================
# BEYİN OLUŞTURMA SİSTEMİ - OTOMATİK
# ======================================================
def _beyin_olustur(kullanici_id: str, kullanici_adi: str = "") -> bool:
    """
    Kullanıcı beyin sistemini oluşturur (eğer yoksa)
    Returns: True if created, False if already exists
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
        "mood": "neutral",
        "stress_level": 0.0,
        "decision_speed": "unknown",
        "confidence_level": 0.5,
        "emotional_state": "neutral",
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
        "updated_at": simdi
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
# BEYİN GÜNCELLEME SİSTEMİ
# ======================================================
def _beyin_guncelle(kullanici_id: str, mesaj: str, kullanici_adi: str):
    """Kullanıcının tüm beyin dosyalarını günceller"""
    kullanici_dizini = CUSTOMERS_PATH / str(kullanici_id)
    
    # Eğer beyin yoksa oluştur
    if not kullanici_dizini.exists():
        _beyin_olustur(kullanici_id, kullanici_adi)
    
    simdi = datetime.now()
    simdi_iso = simdi.isoformat()
    
    # 1️⃣ identity.json güncelle (last_seen)
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
    
    # 3️⃣ psychology.json güncelle (duygusal analiz)
    psikoloji_yolu = kullanici_dizini / "psychology.json"
    psikoloji_verisi = _json_oku(psikoloji_yolu, {})
    
    # Duygusal analiz
    duygu = _duygu_analizi(mesaj)
    psikoloji_verisi["mood"] = duygu
    psikoloji_verisi["emotional_state"] = duygu
    psikoloji_verisi["updated_at"] = simdi_iso
    
    # Stress seviyesi
    if duygu == "negative":
        psikoloji_verisi["stress_level"] = min(10.0, psikoloji_verisi.get("stress_level", 0.0) + 0.5)
    elif duygu == "positive":
        psikoloji_verisi["stress_level"] = max(0.0, psikoloji_verisi.get("stress_level", 0.0) - 0.3)
    
    _json_yaz(psikoloji_yolu, psikoloji_verisi)
    
    # 4️⃣ intent_interest.json güncelle
    niyet_yolu = kullanici_dizini / "intent_interest.json"
    niyet_verisi = _json_oku(niyet_yolu, {})
    
    # Niyet çıkarımı
    tespit_niyet = _niyet_cikar(mesaj)
    if tespit_niyet:
        niyet_verisi["last_intent"] = tespit_niyet
        if tespit_niyet not in niyet_verisi.get("intents", []):
            niyet_verisi.setdefault("intents", []).append(tespit_niyet)
    
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
    if duygu == "positive":
        mevcut_güven = iliski_verisi.get("trust_level", 0.0)
        iliski_verisi["trust_level"] = min(1.0, mevcut_güven + 0.02)
        iliski_verisi["loyalty"] = min(1.0, iliski_verisi.get("loyalty", 0.0) + 0.01)
    elif duygu == "negative":
        mevcut_güven = iliski_verisi.get("trust_level", 0.0)
        iliski_verisi["trust_level"] = max(0.0, mevcut_güven - 0.05)
    
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
    
    # Satış sinyalleri
    satis_sinyalleri = satis_verisi.get("buying_signals", [])
    
    satis_kelimeleri = ["almaq", "satın", "qiymət", "bahası", "sifariş", "ödəniş", "alış", "fiyat"]
    if any(kelime in mesaj.lower() for kelime in satis_kelimeleri):
        satis_sinyalleri.append({
            "timestamp": simdi_iso,
            "signal": mesaj[:50],
            "type": "buying_interest"
        })
        satis_verisi["buying_signals"] = satis_sinyalleri[-10:]  # Son 10 sinyal
        
        # Lead skorunu artır
        mevcut_skor = satis_verisi.get("lead_score", 0)
        satis_verisi["lead_score"] = min(100, mevcut_skor + 5)
        
        # Aşamayı güncelle
        if satis_verisi["lead_score"] > 70:
            satis_verisi["stage"] = "hot"
        elif satis_verisi["lead_score"] > 40:
            satis_verisi["stage"] = "warm"
        elif satis_verisi["lead_score"] > 10:
            satis_verisi["stage"] = "aware"
    
    satis_verisi["updated_at"] = simdi_iso
    _json_yaz(satis_yolu, satis_verisi)
    
    # İsim çıkarımı (eğer mesajda isim varsa)
    isim = _isim_cikar(mesaj)
    if isim and isim != kullanici_adi:
        kimlik_verisi["real_name"] = isim
        _json_yaz(kimlik_yolu, kimlik_verisi)

def _duygu_analizi(metin: str) -> str:
    """Metinden duygu çıkarır"""
    metin_kucuk = metin.lower()
    
    pozitif_kelimeler = ["yaxşı", "şad", "əla", "təşəkkür", "sağ ol", "qane", "mükəmməl", "super", "çox gözəl"]
    negatif_kelimeler = ["pis", "kədərli", "qəzəbli", "narahat", "problem", "şikayət", "acı", "pislik", "yox"]
    heyecanli_kelimeler = ["təəccüb", "vau", "heyran", "maraqlı", "heyət", "möhtəşəm", "vay"]
    
    pozitif_sayi = sum(1 for kelime in pozitif_kelimeler if kelime in metin_kucuk)
    negatif_sayi = sum(1 for kelime in negatif_kelimeler if kelime in metin_kucuk)
    heyecanli_sayi = sum(1 for kelime in heyecanli_kelimeler if kelime in metin_kucuk)
    
    if pozitif_sayi > negatif_sayi and pozitif_sayi > heyecanli_sayi:
        return "positive"
    elif negatif_sayi > pozitif_sayi and negatif_sayi > heyecanli_sayi:
        return "negative"
    elif heyecanli_sayi > pozitif_sayi and heyecanli_sayi > negatif_sayi:
        return "excited"
    elif "?" in metin:
        return "curious"
    else:
        return "neutral"

def _niyet_cikar(metin: str) -> str:
    """Metinden niyet çıkarır"""
    metin_kucuk = metin.lower()
    
    niyetler = {
        "buy": ["almaq", "satın", "qiymət", "bahası", "sifariş", "alış", "alım", "fiyat"],
        "ask": ["sual", "soruş", "necə", "nədir", "deyin", "bildirin", "kim", "harada", "nece"],
        "complain": ["şikayət", "problem", "pis", "yaxşı deyil", "əziyyət", "narazı", "kömək"],
        "greeting": ["salam", "salamlar", "hello", "hi", "salamat", "sabahınız", "axşamınız"],
        "thank": ["təşəkkür", "sağ ol", "minnətdaram", "təşəkkürlər", "çox sağ ol", "sağol"],
        "compare": ["müqayisə", "fərq", "hansı", "daha yaxşı", "ən yaxşı", "necə fərqlənir"]
    }
    
    for niyet, kelimeler in niyetler.items():
        if any(kelime in metin_kucuk for kelime in kelimeler):
            return niyet
    
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
    
    # "Benim adım X", "Adım X", "X diye çağırın" gibi kalıplar
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

# ======================================================
# KONUŞMA ARŞİVİ SİSTEMİ
# ======================================================
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

# ======================================================
# OPERATOR HANDOFF SİSTEMİ (CONTROL/ Klasöründe)
# ======================================================
def _operator_handoff_ayarla(kullanici_id: str, aktif: bool):
    """Operator handoff durumunu ayarlar"""
    operator_handoff_verisi = _json_oku(OPERATOR_HANDOFF_FILE, {})
    
    if aktif:
        operator_handoff_verisi[kullanici_id] = {
            "status": True,
            "updated_at": datetime.now().isoformat(),
            "reason": "user_request"
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

# ======================================================
# ANALİTİK SİSTEMİ
# ======================================================
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
# ANA API FONKSİYONLARI (BOT.PY İÇİN)
# ======================================================
def add_customer_if_not_exists(company_id: str, platform: str, user_id: str, username: str) -> bool:
    """
    Müşteri yoksa otomatik beyin oluşturur
    company_id: Şirket ID (sadece imza için)
    platform: "telegram" (sabit)
    user_id: Gerçek Telegram user_id
    username: Telegram kullanıcı adı
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
    
    # 3. Analitik verilerini güncelle
    _analitik_guncelle()
    
    print(f"📝 {user_id} için kaydedildi: {message[:30]}...")

def set_operator_handoff(company_id: str, platform: str, user_id: str, active: bool):
    """
    Operator handoff durumunu ayarlar
    active=True → bot SUSAR
    """
    _operator_handoff_ayarla(user_id, active)
    print(f"🔄 Operator handoff: {user_id} = {active}")

def is_operator_handoff_active(company_id: str, platform: str, user_id: str) -> bool:
    """
    Operator handoff aktifse True döndürür
    """
    return _operator_handoff_aktif_mi(user_id)

# ======================================================
# OKUMA FONKSİYONLARI
# ======================================================
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
        "mood": psikoloji.get("mood", "neutral"),
        "lead_score": satis.get("lead_score", 0),
        "last_seen": kimlik.get("last_seen", "")
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
    
    return tum_konusmalar[:100]  # En fazla 100 mesaj

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
            "system": "telegram_customer_brain"
        }
    
    def get_customer_messages(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Müşterinin mesajlarını döndürür (eski uyumluluk için)"""
        return get_conversation_history(user_id, days=30)[:limit]
    
    def cleanup_old_data(self, days: int = 30):
        """Eski verileri temizler (eski uyumluluk için)"""
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
    
    print(f"✅ Telegram Müşteri Beyin Sistemi Başlatıldı")
    print(f"📂 Temel yol: {BASE_PATH}")
    print(f"👥 Müşteri sayısı: {musteri_sayisi}")
    print(f"📊 Analitik: {ANALYTICS_PATH}")
    print(f"🎛️  Kontrol: {CONTROL_PATH}")
    
    return {
        "status": "active",
        "path": str(BASE_PATH),
        "customer_count": musteri_sayisi,
        "system": "telegram_customer_brain"
    }

# ======================================================
# BAŞLANGIÇ
# ======================================================
# Dosya import edildiğinde dizinleri oluştur
for dizin in [CUSTOMERS_PATH, CONVERSATIONS_PATH, CONTROL_PATH, ANALYTICS_PATH]:
    dizin.mkdir(parents=True, exist_ok=True)
# ======================================================
# YENİ FUNKSİYALAR - BOT.PY ÜÇÜN (ƏN SONA ƏLAVƏ EDİN)
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
        
        # Yeni veriləri əlavə et
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
        
        # Yeni veriləri əlavə et
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
        
        # Yeni veriləri əlavə et
        for key, value in intent_data.items():
            if key == "interests" and isinstance(value, list):
                # İlgi alanlarını birləşdir
                mevcut_ilgiler = niyet_verisi.get("interests", [])
                yeni_ilgiler = [ilgi for ilgi in value if ilgi not in mevcut_ilgiler]
                niyet_verisi["interests"] = mevcut_ilgiler + yeni_ilgiler
            elif key == "intents" and isinstance(value, list):
                # Niyyətləri birləşdir
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
        
        # Yeni veriləri əlavə et
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