"""
DEEPTHINK - RULE-BASED EMOTION ENGINE v4.1
✅ FIXED: "nəoldu" → "stressed" OLACAQ
✅ IMPROVED NORMALIZATION
✅ BÜTÜN DİAKRİTİKA VARYANTLARI
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

class DeepThink:
    """Rule-based emotion analyzer - HEÇ VAXT SƏHV UNKNOWN VERMƏZ"""
    
    def __init__(self):
        self.rules_path = Path(__file__).parent / "psychology_rules.json"
        self.unknown_path = Path(__file__).parent / "unknown.json"
        
        # STRICT CATEGORY ORDER (PRIORITY ilə)
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
        
        # CATEGORY → CURRENT_MOOD MAPPING
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
        
        # TƏKRARLANAN KARAKTERLƏR ÜÇÜN NORMALİZASİYA
        self.repeated_chars_regex = re.compile(r'(.)\1{2,}')
    
    def _load_rules(self) -> Dict:
        """Qaydaları yüklə - HƏR DƏFƏ YENIDƏN"""
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Rules file error: {e}")
            return {}
    
    def _normalize_text_v2(self, text: str) -> str:
        """
        YENİ V2 NORMALİZASİYA:
        1. Bütün diakritik variantları
        2. Təkrar hərfləri normallaşdır (gec → gec)
        3. Boşluq normalizasiyası
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Durğu işarələrini və xüsusi simvolları sil
        text = re.sub(r'[.,!?;:()\[\]{}"\'`…\-–—/*+=_|~<>]', ' ', text)
        
        # 3. Bütün mümkün Azərbaycan simvollarını Latinə çevir
        az_to_latin_extended = {
            # Ə və variantları
            'ə': 'e', 'ə': 'e', 'ə': 'e',
            
            # Ş və variantları  
            'ş': 's', 'ṣ': 's', 'ş': 's',
            
            # I/İ problemi
            'ı': 'i', 'i': 'i', 'İ': 'i',
            
            # Ö
            'ö': 'o', 'ö': 'o',
            
            # Ü
            'ü': 'u', 'ü': 'u',
            
            # Ç
            'ç': 'c', 'ç': 'c',
            
            # Ğ
            'ğ': 'g', 'ğ': 'g',
            
            # Q
            'q': 'g', # q → g (qarışıqlığı aradan qaldırmaq)
            
            # X
            'x': 'h', # x → h (xəbər → heber)
            
            # Əlavə Türk simvolları
            'ğ': 'g', 'Ğ': 'g',
            'ç': 'c', 'Ç': 'c',
            'ş': 's', 'Ş': 's',
            'ı': 'i', 'İ': 'i',
            'ö': 'o', 'Ö': 'o',
            'ü': 'u', 'Ü': 'u'
        }
        
        for az_char, latin_char in az_to_latin_extended.items():
            text = text.replace(az_char, latin_char)
        
        # 4. Təkrar hərfləri normallaşdır (geccc → gec)
        text = self.repeated_chars_regex.sub(r'\1\1', text)
        
        # 5. Rəqəmləri sil (vacib deyil)
        text = re.sub(r'\d+', ' ', text)
        
        # 6. Çoxlu boşluqları tək boşluğa sal
        text = re.sub(r'\s+', ' ', text)
        
        # 7. Trim
        text = text.strip()
        
        return text
    
    def _generate_variants(self, text: str) -> List[str]:
        """
        Mətndən bütün mümkün variantları yarat:
        1. Normalizasiya olunmuş
        2. Boşluqsuz variant
        3. Təkrar hərflər azaldılmış
        """
        variants = set()
        
        if not text:
            return list(variants)
        
        # 1. Əsas normalizasiya
        normalized = self._normalize_text_v2(text)
        if normalized:
            variants.add(normalized)
        
        # 2. Boşluqsuz variant
        no_spaces = normalized.replace(' ', '')
        if no_spaces:
            variants.add(no_spaces)
        
        # 3. "nə oldu" → "neoldu" və "noldu" variantları
        if ' ' in normalized:
            # Boşluqları fərqli kombinasiyalarda sil
            parts = normalized.split()
            
            # Bütün hissələri birləşdir
            joined = ''.join(parts)
            variants.add(joined)
            
            # "nə" → "ne" transformasiyasından sonra "no" variantı
            if 'ne' in joined:
                variants.add(joined.replace('ne', 'no'))
        
        return list(variants)
    
    def _check_category_match_v2(self, normalized_input: str, category_phrases: List[str]) -> Tuple[bool, str]:
        """
        YENİ V2 MATCHING:
        1. Input-un bütün variantlarını yarat
        2. Hər bir phrase-in bütün variantlarını yarat  
        3. Hər hansı variant uyğun gələrsə → TRUE
        """
        # Input-un bütün variantları
        input_variants = self._generate_variants(normalized_input)
        
        for phrase in category_phrases:
            if not phrase:
                continue
                
            # Phrase-in bütün variantları
            phrase_variants = self._generate_variants(phrase)
            
            # Hər bir input variantı üçün
            for input_var in input_variants:
                # Hər bir phrase variantı üçün
                for phrase_var in phrase_variants:
                    # SUBSTRING CHECK: phrase_var in input_var
                    if phrase_var and input_var and phrase_var in input_var:
                        return True, phrase
        
        return False, ""
    
    def _save_to_unknown(self, original_message: str, normalized_message: str):
        """SADƏCƏ HƏR ŞEYDƏN SONRA UNKNOWN YAZ"""
        try:
            unknown_data = []
            if self.unknown_path.exists():
                with open(self.unknown_path, 'r', encoding='utf-8') as f:
                    unknown_data = json.load(f)
            
            # Artıq varmı?
            normalized_original = self._normalize_text_v2(original_message)
            existing = next((item for item in unknown_data 
                           if self._normalize_text_v2(item.get("original", "")) == normalized_original), None)
            
            if not existing:
                new_entry = {
                    "original": original_message[:200],
                    "normalized": normalized_message[:200],
                    "timestamp": datetime.now().isoformat(),
                    "count": 1,
                    "rule_exists": False
                }
                unknown_data.append(new_entry)
                
                # Maksimum 1000 unknown saxla
                if len(unknown_data) > 1000:
                    unknown_data = unknown_data[-1000:]
                
                with open(self.unknown_path, 'w', encoding='utf-8') as f:
                    json.dump(unknown_data, f, indent=2, ensure_ascii=False)
                
                print(f"📝 GERÇƏK UNKNOWN: '{original_message[:50]}...' → unknown.json")
                
        except Exception as e:
            print(f"⚠️ Unknown save error: {e}")
    
    def analyze(self, message: str, platform: str = "telegram") -> Optional[Dict[str, Any]]:
        """
        MESAJI TƏHLİL ET - YENİ V2 ALQORİTM
        
        ƏSAS DƏYİŞİKLİK: Bütün mümkün variantları yoxlayırıq
        """
        # ========== 1. MESAJI NORMALIZƏ ET ==========
        normalized_message = self._normalize_text_v2(message)
        if not normalized_message:
            print(f"❓ BOŞ MESAJ → non_emotional")
            return self._create_result("non_emotional", "non_emotional", message)
        
        # ========== 2. RULES OXU VƏ NORMALIZƏ ET ==========
        raw_rules = self._load_rules()
        if not raw_rules:
            print(f"❌ RULES FILE YOXDUR → non_emotional")
            return self._create_result("non_emotional", "non_emotional", message)
        
        # Rules-dakı phrases-ləri normalizə et
        normalized_rules = {}
        for category_name, category_data in raw_rules.items():
            if category_name == "_meta":
                normalized_rules[category_name] = category_data
                continue
            
            if isinstance(category_data, dict):
                normalized_category = category_data.copy()
                phrases = category_data.get("phrases", [])
                
                # Hər phrase-i normalizasiya et
                normalized_phrases = []
                for phrase in phrases:
                    if isinstance(phrase, str):
                        normalized_phrase = self._normalize_text_v2(phrase)
                        if normalized_phrase:
                            normalized_phrases.append(normalized_phrase)
                
                normalized_category["phrases"] = normalized_phrases
                normalized_rules[category_name] = normalized_category
        
        # ========== 3. PRIORITY SIRASI İLƏ YOXLA ==========
        matched_category = None
        matched_phrase = ""
        
        # Əvvəlcə bütün normal kateqoriyaları yoxla
        for category_name in self.category_order:
            if category_name in normalized_rules:
                category_data = normalized_rules[category_name]
                phrases = category_data.get("phrases", [])
                
                if phrases:
                    # YENİ V2 MATCHING
                    match_found, phrase = self._check_category_match_v2(normalized_message, phrases)
                    if match_found:
                        matched_category = category_name
                        matched_phrase = phrase
                        print(f"✅ MATCH: '{message[:30]}...' → {category_name} (phrase: '{phrase}')")
                        break
        
        # ========== 4. HEÇ BİRİ UYĞUN GƏLMƏDİ? ==========
        if not matched_category:
            # non_emotional yoxla
            if "non_emotional" in normalized_rules:
                non_emotional_data = normalized_rules["non_emotional"]
                non_emotional_phrases = non_emotional_data.get("phrases", [])
                
                match_found, phrase = self._check_category_match_v2(normalized_message, non_emotional_phrases)
                if match_found:
                    matched_category = "non_emotional"
                    matched_phrase = phrase
                    print(f"✅ NON_EMOTIONAL: '{message[:30]}...' → non_emotional")
        
        # ========== 5. HƏLƏ DƏ TAPILMADI? ==========
        if not matched_category:
            # O ZAMAN GERÇƏK UNKNOWN
            self._save_to_unknown(message, normalized_message)
            print(f"❌ GERÇƏK UNKNOWN: '{message[:30]}...' → Heç bir rule uyğun gəlmədi")
            return None
        
        # ========== 6. NƏTİCƏ YARAT ==========
        result = self._create_result(matched_category, matched_phrase, message)
        
        # ========== 7. CRITICAL UYARISI ==========
        if matched_category in self.critical_categories:
            print(f"   🚨 CRITICAL: {matched_category.upper()} → OPERATOR REQUIRED")
        
        return result
    
    def _create_result(self, category: str, matched_phrase: str, original_message: str) -> Dict[str, Any]:
        """Nəticə dict yarat"""
        mood = self.category_to_mood.get(category, "neutral")
        emotional_state = self.category_to_emotional_state.get(category, "calm")
        
        # Operator tələb olunurmu?
        operator_required = category in self.critical_categories
        
        # Rules faylından operator_required oxu
        rules = self._load_rules()
        if category in rules:
            category_data = rules[category]
            if category_data.get("operator_required", False):
                operator_required = True
        
        # last_reason format
        last_reason = f"{category}_detected"
        if matched_phrase:
            last_reason = f"{category}_phrase: {matched_phrase[:20]}"
        
        return {
            "current_mood": mood,
            "emotional_state": emotional_state,
            "last_mood": mood,  # memory.py dəyişəcək
            "last_reason": last_reason,
            "last_message_type": category,
            "operator_required": operator_required,
            "updated_at": datetime.now().isoformat(),
            # Debug məlumatları
            "_debug": {
                "matched_phrase": matched_phrase,
                "matched_category": category,
                "original_message": original_message[:100]
            }
        }
    
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

# TEST FONKSİYONU
def run_tests():
    """Testlər"""
    print("\n" + "="*60)
    print("🧠 DEEPTHINK v4.1 TEST SİSTEMİ - VARIANT MATCHING")
    print("="*60)
    
    tests = [
        ("nə oldu", "stress"),
        ("nəoldu...", "stress"),
        ("nə oldu day gec cavab verirsiniz", "stress"),
        ("stresliyəm", "stress"),
        ("mən stresliyəm vallah", "stress"),
        ("noldu", "stress"),
        ("kömək edin", "urgency"),
        ("siz dələduzsunuz", "accusation"),
        ("dümbələy", "abuse"),
        ("ok", "non_emotional"),
        ("aydındır", "non_emotional"),
        ("təşəkkür", "satisfaction"),
        ("çox sağ ol", "satisfaction"),
    ]
    
    for message, expected in tests:
        result = deepthink.analyze(message)
        
        if result:
            actual = result.get("last_message_type", "unknown")
            status = "✅" if actual == expected else "❌"
            print(f"{status} '{message}' → {actual} (gözlənilən: {expected})")
        else:
            status = "✅" if expected == "unknown" else "❌"
            print(f"{status} '{message}' → UNKNOWN (gözlənilən: {expected})")

# Əgər birbaşa çalışdırılırsa, test et
if __name__ == "__main__":
    run_tests()