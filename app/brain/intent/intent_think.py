"""
INTENT ANALIZ SISTEMI v1.0
✅ Müştərinin niyə belə hiss etdiyini tapır
✅ Include məntiqi ilə işləyir
✅ Normalizasiya eyni qayda ilə
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

class IntentThink:
    def __init__(self):
        self.rules_path = Path(__file__).parent / "intent_rules.json"
        
        # INTENT KATEQORİYALARI
        self.intent_categories = [
            "slow_response",      # Cavab gecikir
            "accusation",         # İtiham, şübhə
            "request_help",       # Kömək istəyi
            "request_info",       # Məlumat istəyi
            "complaint",          # Şikayət
            "price_question",     # Qiymət sualı
            "comparison",         # Müqayisə
            "greeting",           # Salamlama
            "thanks",             # Təşəkkür
            "confusion"           # Qarışıqlıq
        ]
    
    def _load_rules(self) -> Dict:
        """Intent qaydalarını yüklə"""
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Intent rules file error: {e}")
            return {}
    
    def _normalize_text(self, text: str) -> str:
        """
        MƏTNİ NORMALİZASİYA ET - DEEPTHINK İLƏ EYNİ
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Durğu işarələrini sil
        text = re.sub(r'[.,!?;:()\[\]{}"\'`…\-–—/*+=_|~<>]', ' ', text)
        
        # 3. AZ → LATIN çevir (DEEPTHINK İLƏ EYNİ)
        az_to_latin = {
            'ə': 'e',
            'ş': 's',
            'ı': 'i',
            'ö': 'o',
            'ü': 'u',
            'ç': 'c',
            'ğ': 'g',
            'Ə': 'e',
            'Ş': 's',
            'İ': 'i',
            'I': 'i',
            'Ö': 'o',
            'Ü': 'u',
            'Ç': 'c',
            'Ğ': 'g'
        }
        
        for az_char, latin_char in az_to_latin.items():
            text = text.replace(az_char, latin_char)
        
        # 4. Çoxlu boşluqları tək boşluğa sal
        text = re.sub(r'\s+', ' ', text)
        
        # 5. Trim
        text = text.strip()
        
        return text
    
    def _generate_variants(self, text: str) -> List[str]:
        """
        Mətndən bütün mümkün variantları yarat
        """
        variants = set()
        
        if not text:
            return list(variants)
        
        # 1. Əsas normalizasiya
        normalized = self._normalize_text(text)
        if normalized:
            variants.add(normalized)
        
        # 2. Boşluqsuz variant
        no_spaces = normalized.replace(' ', '')
        if no_spaces:
            variants.add(no_spaces)
        
        # 3. "nə oldu" → "neoldu" və "noldu" variantları
        if ' ' in normalized:
            parts = normalized.split()
            joined = ''.join(parts)
            variants.add(joined)
            
            # "nə" → "ne" transformasiyasından sonra "no" variantı
            if 'ne' in joined:
                variants.add(joined.replace('ne', 'no'))
        
        return list(variants)
    
    def _check_intent_match(self, normalized_input: str, intent_phrases: List[str]) -> Tuple[bool, str]:
        """
        INTENT MATCHING - include (contains) məntiqi
        """
        # Input-un bütün variantları
        input_variants = self._generate_variants(normalized_input)
        
        for phrase in intent_phrases:
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
    
    def analyze(self, message: str, psychology_category: str = None) -> Optional[Dict[str, Any]]:
        """
        MESADAN INTENT TAP
        
        Args:
            message: İstifadəçi mesajı
            psychology_category: Psixoloji kateqoriya (məsələn, "stress")
            
        Returns:
            Dict və ya None (heç bir intent tapılmasa)
        """
        # 1. Mesajı normalizə et
        normalized_message = self._normalize_text(message)
        if not normalized_message:
            return None
        
        # 2. Intent qaydalarını yüklə
        rules = self._load_rules()
        if not rules:
            return None
        
        # 3. Bütün intent kateqoriyalarını yoxla
        matched_intent = None
        matched_phrase = ""
        
        for intent_name in self.intent_categories:
            if intent_name in rules:
                intent_data = rules[intent_name]
                phrases = intent_data.get("phrases", [])
                
                if phrases:
                    match_found, phrase = self._check_intent_match(normalized_message, phrases)
                    if match_found:
                        matched_intent = intent_name
                        matched_phrase = phrase
                        break
        
        # 4. Heç bir intent tapılmadısa
        if not matched_intent:
            return None
        
        # 5. Nəticə yarat
        intent_data = rules[matched_intent]
        
        return {
            "intent": matched_intent,
            "matched_phrase": matched_phrase,
            "description": intent_data.get("description", ""),
            "priority": intent_data.get("priority", 999),
            "confidence": 1.0,  # Tam uyğun olduğu üçün
            "updated_at": datetime.now().isoformat()
        }


# Global instance
intent_think = IntentThink()

# TEST FONKSİYONU
def run_intent_tests():
    """Intent testləri"""
    print("\n" + "="*60)
    print("🧠 INTENT TEST SİSTEMİ")
    print("="*60)
    
    tests = [
        ("nə oldu day gec cavab verirsiniz", "slow_response"),
        ("niyə gec cavab verirsiniz?", "slow_response"),
        ("siz dələduzsunuz", "accusation"),
        ("kömək edin", "request_help"),
        ("qiymət necədir", "price_question"),
        ("hansı daha yaxşıdır", "comparison"),
        ("salam", "greeting"),
        ("təşəkkür", "thanks"),
        ("başa düşmürəm", "confusion"),
    ]
    
    for message, expected in tests:
        result = intent_think.analyze(message)
        
        if result:
            actual = result["intent"]
            status = "✅" if actual == expected else "❌"
            print(f"{status} '{message}' → {actual} (gözlənilən: {expected})")
        else:
            status = "✅" if expected is None else "❌"
            print(f"{status} '{message}' → NO INTENT (gözlənilən: {expected})")

if __name__ == "__main__":
    run_intent_tests()