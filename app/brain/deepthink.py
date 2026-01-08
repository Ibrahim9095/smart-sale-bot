"""
DEEPTHINK - RULE-BASED EMOTION ENGINE v3.0
✅ STRICT PRIORITY ORDER: abuse → threat → blackmail → accusation → harassment → urgency → anger → frustration → sadness → stress → joy → satisfaction → thinking_state → non_emotional
✅ CRITICAL CATEGORIES ALWAYS ESCALATE
✅ NO EMOTION GUESSING
✅ UNKNOWN → unknown.json ONLY
✅ MANUAL UPDATES WORK IMMEDIATELY
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class DeepThink:
    """Rule-based emotion analyzer with STRICT priority for critical categories"""
    
    def __init__(self):
        self.rules_path = Path(__file__).parent / "psychology_rules.json"
        self.unknown_path = Path(__file__).parent / "unknown.json"
        
        # STRICT CATEGORY ORDER (CRITICAL FIRST)
        self.category_order = [
            "abuse",          # Təhqir, söyüş
            "threat",         # Təhdid
            "blackmail",      # Şantaj
            "accusation",     # İttiham
            "harassment",     # Təzyiq, israr
            "urgency",        # Acil kömək
            "anger",          # Qəzəb
            "frustration",    # Məyusluq
            "sadness",        # Kədər
            "stress",         # Stress
            "joy",            # Sevinç
            "satisfaction",   # Razılıq
            "thinking_state", # Düşüncə
            "non_emotional"   # Emosiyasız
        ]
        
        # CATEGORY → CURRENT_MOOD MAPPING (EXACT CATEGORY NAME)
        self.category_to_mood = {
            "abuse": "abuse",
            "threat": "threat",
            "blackmail": "blackmail",
            "accusation": "accusation",
            "harassment": "harassment",
            "urgency": "urgency",
            "anger": "angry",
            "frustration": "frustrated",
            "sadness": "sad",
            "stress": "stressed",
            "joy": "happy",
            "satisfaction": "satisfied",
            "thinking_state": "thinking",
            "non_emotional": "neutral"
        }
        
        # CATEGORY → EMOTIONAL_STATE
        self.category_to_emotional_state = {
            "abuse": "hostile",
            "threat": "threatening",
            "blackmail": "manipulative",
            "accusation": "accusing",
            "harassment": "insistent",
            "urgency": "urgent",
            "anger": "angry",
            "frustration": "frustrated",
            "sadness": "sad",
            "stress": "tense",
            "joy": "joyful",
            "satisfaction": "satisfied",
            "thinking_state": "thinking",
            "non_emotional": "calm"
        }
        
        # CRITICAL CATEGORIES (ALWAYS ESCALATE TO OPERATOR)
        self.critical_categories = [
            "abuse",
            "threat", 
            "blackmail",
            "accusation",
            "harassment",
            "urgency"
        ]
    
    def _load_rules(self) -> Dict:
        """Qaydaları yüklə - HƏR DƏFƏ YENIDƏN"""
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Rules file error: {e}")
            return {}
    
    def _save_to_unknown(self, phrase: str, suspected_category: str = None):
        """Unknown ifadəni unknown.json-a yaz"""
        try:
            unknown_data = []
            if self.unknown_path.exists():
                with open(self.unknown_path, 'r', encoding='utf-8') as f:
                    unknown_data = json.load(f)
            
            # Artıq varmı? (normalize edərək yoxla)
            normalized_phrase = self._normalize_message(phrase)
            existing = next((item for item in unknown_data 
                           if self._normalize_message(item.get("phrase", "")) == normalized_phrase), None)
            
            if not existing:
                new_entry = {
                    "phrase": phrase[:200],
                    "suspected_category": suspected_category,
                    "timestamp": datetime.now().isoformat(),
                    "count": 1
                }
                unknown_data.append(new_entry)
            else:
                # Artıq varsa, count artır
                existing["count"] = existing.get("count", 0) + 1
                existing["last_seen"] = datetime.now().isoformat()
                
            with open(self.unknown_path, 'w', encoding='utf-8') as f:
                json.dump(unknown_data, f, indent=2, ensure_ascii=False)
                
            print(f"📝 UNKNOWN: '{phrase[:50]}...' → unknown.json (suspected: {suspected_category})")
                
        except Exception as e:
            print(f"⚠️ Unknown save error: {e}")
    
    def _normalize_message(self, message: str) -> str:
        """Mesajı normalizə et"""
        if not message or not isinstance(message, str):
            return ""
        
        message = message.lower().strip()
        # Türk/Azərbaycan hərflərini saxlayaraq normalizasiya
        message = re.sub(r'[^\w\sğüşıöçəĞÜŞİÖÇƏ]', ' ', message)
        message = re.sub(r'\s+', ' ', message)
        return message.strip()
    
    def _check_phrase_match(self, message: str, phrase: str) -> bool:
        """Bir ifadənin uyğun olub olmadığını yoxla"""
        if not phrase or not message:
            return False
        
        # Normalizə et
        norm_message = self._normalize_message(message)
        norm_phrase = self._normalize_message(phrase)
        
        if not norm_phrase or not norm_message:
            return False
        
        # 1. Tam uyğunluq
        if norm_phrase == norm_message:
            return True
        
        # 2. Substring uyğunluğu (söz sərhədlərinə bax)
        words = norm_message.split()
        
        # Əgər ifadə tək sözdürsə, söz sırasında yoxla
        if ' ' not in norm_phrase:
            return norm_phrase in words
        
        # Əgər ifadə birdən çox sözdürsə, substring kimi yoxla
        return norm_phrase in norm_message
    
    def _check_category_match(self, message: str, category_data: Dict) -> tuple[bool, str]:
        """Kateqoriyanın ifadələrindən hər hansı biri uyğun gəlirmi?"""
        phrases = category_data.get("phrases", [])
        
        for phrase in phrases:
            if self._check_phrase_match(message, phrase):
                return True, phrase
        
        return False, ""
    
    def _get_suspected_category(self, message: str) -> str:
        """Mesaja görə şübhəli kateqoriyanı təxmin et (sadəcə unknown.json üçün)"""
        message_lower = message.lower()
        
        # Şübhəli sözlərə görə təxmin
        abuse_words = ["axmaq", "dəli", "səfeh", "mal", "şərəfsiz", "it", "donuz"]
        threat_words = ["polis", "məhkəmə", "şikayət", "bağlat", "cavab ver", "peşman"]
        accusation_words = ["dələduz", "aldad", "fırıldaq", "yalan", "haqsızlıq"]
        
        for word in abuse_words:
            if word in message_lower:
                return "abuse"
        
        for word in threat_words:
            if word in message_lower:
                return "threat"
                
        for word in accusation_words:
            if word in message_lower:
                return "accusation"
        
        return "unknown"
    
    def analyze(self, message: str, platform: str = "telegram") -> Optional[Dict[str, Any]]:
        """
        Mesajı təhlil et - YALNIZ BİR KATEQORİYA
        
        Qayıdır: 
        - Dict (əgər kateqoriya tapılsa)
        - None (əgər UNKNOWN-dursa)
        """
        # ========== 1. NORMALIZASIYA ==========
        normalized = self._normalize_message(message)
        if not normalized:
            return None
        
        # ========== 2. QAYDALARI YENIDƏN YÜKLƏ ==========
        rules = self._load_rules()
        if not rules:
            print("❌ No rules found")
            return None
        
        # ========== 3. STRICT ORDER İLƏ YOXLA ==========
        matched_category = None
        matched_phrase = ""
        
        for category_name in self.category_order:
            if category_name in rules:
                category_data = rules[category_name]
                
                match_found, phrase = self._check_category_match(normalized, category_data)
                if match_found:
                    matched_category = category_name
                    matched_phrase = phrase
                    
                    # ✅ FIRST MATCH WINS - DURUR
                    print(f"✅ MATCH: '{message[:30]}...' → {category_name} (phrase: '{phrase}')")
                    break
        
        # ========== 4. HEÇ BİR KATEQORİYA TAPILMASA ==========
        if not matched_category:
            suspected = self._get_suspected_category(message)
            self._save_to_unknown(message, suspected)
            return None  # ❌ UNKNOWN - psychology.json-a YAZILMIR
        
        # ========== 5. MOOD DƏYƏRİNİ AL ==========
        mood = self.category_to_mood.get(matched_category, "neutral")
        emotional_state = self.category_to_emotional_state.get(matched_category, "calm")
        
        # ========== 6. OPERATOR TƏLƏB OLUNURMU? ==========
        operator_required = False
        if matched_category in self.critical_categories:
            operator_required = True
        else:
            # Kateqoriya məlumatlarından oxu
            category_data = rules[matched_category]
            if category_data.get("operator_required", False):
                operator_required = True
        
        # ========== 7. LAST_REASON FORMAT ==========
        last_reason = f"{matched_category}_detected"
        if matched_phrase:
            last_reason = f"{matched_category}_phrase: {matched_phrase[:20]}"
        
        # ========== 8. NƏTİCƏ (YALNIZ TƏLƏB OLUNAN SAHƏLƏR) ==========
        result = {
            "current_mood": mood,
            "emotional_state": emotional_state,
            "last_mood": mood,  # Eyni qalır (memory.py dəyişəcək)
            "last_reason": last_reason,
            "last_message_type": matched_category,
            "operator_required": operator_required,
            "updated_at": datetime.now().isoformat(),
            # Debug məlumatları (production-da silinə bilər)
            "_debug_matched_phrase": matched_phrase,
            "_debug_matched_category": matched_category
        }
        
        # ========== 9. CRITICAL CATEGORY UYARISI ==========
        if operator_required:
            print(f"   ⚠️ CRITICAL: {matched_category.upper()} → OPERATOR REQUIRED")
        
        return result
    
    def get_unknown_count(self) -> int:
        """Unknown ifadələrin sayını qaytar"""
        try:
            if self.unknown_path.exists():
                with open(self.unknown_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return len(data)
            return 0
        except:
            return 0
    
    def clear_unknown(self) -> bool:
        """unknown.json faylını təmizlə"""
        try:
            with open(self.unknown_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            return True
        except:
            return False


# Global instance
deepthink = DeepThink()