#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMOTIONAL STATE ENGINE v3.0
🚨 STATELESS: Hər mesaj üçün SIFIRDAN hesablanır
🚨 NO DEFAULT: calm DEFAULT DEYİL
🚨 REAL-TIME: Yalnız message + mood + intent əsasında
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class EmotionalStateEngine:
    def __init__(self):
        self.rules_path = Path(__file__).parent / "emotional_state_rules.json"
        self.rules = self._load_rules()
        
        # 🚨 DEFAULT QADAĞASI: calm DEFAULT OLA BİLMƏZ
        # Hər halda konkret emotional state qaytarılmalıdır
        self.default_state = "neutral"  # calm deyil!
        
        # Emotional state kateqoriyaları
        self.state_categories = {
            "angry": ["əsəbi", "hirsli", "qəzəbli", "acıqlı", "kefim pis"],
            "dissatisfied": ["baha", "bahadır", "qiymət", "pahalı", "narazıyam"],
            "satisfied": ["yaxşı", "məmnunam", "təşəkkür", "sağ ol", "əla"],
            "inquiring": ["?", "necə", "niyə", "neçə", "nədir", "hardan"],
            "thinking": ["düşünürəm", "bilmirəm", "görüm", "baxaq"],
            "neutral": []  # Default deyil, sadəcə digərləri uyğun gəlmədikdə
        }

    def _load_rules(self) -> Dict:
        try:
            if self.rules_path.exists():
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Meta məlumatları sil
                    data.pop("_meta", None)
                    return data
        except Exception as e:
            print(f"⚠️ Emotional state rules yükləmə xətası: {e}")
        return {}

    def _normalize(self, text: str) -> str:
        """Mətni normalizasiya et"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^\w\sğüşıöçə]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _check_state_rules(self, message: str, mood: str, intent: str) -> Optional[str]:
        """
        JSON rules-dan emotional state tap
        Əgər rule tapılsa, onu qaytar
        """
        normalized_msg = self._normalize(message)
        
        if not self.rules:
            return None
        
        # Intent əsaslı axtarış
        if intent in self.rules:
            intent_rules = self.rules[intent]
            for rule in intent_rules:
                if isinstance(rule, dict):
                    keywords = rule.get("keywords", [])
                    conditions = rule.get("conditions", {})
                    
                    # Keywords yoxla
                    keyword_match = False
                    for kw in keywords:
                        if kw in normalized_msg:
                            keyword_match = True
                            break
                    
                    # Conditions yoxla
                    condition_match = True
                    if "mood" in conditions:
                        if mood not in conditions["mood"]:
                            condition_match = False
                    
                    if keyword_match and condition_match:
                        return rule.get("state", self.default_state)
        
        return None

    def derive_emotional_state(self, message: str, mood: str, intent: str) -> str:
        """
        🚨 KRİTİK FUNKSİYA: Emotional state SIFIRDAN hesablanır
        ❌ Keçmiş state OXUNMUR
        ❌ psychology.json OXUNMUR
        ❌ calm DEFAULT YOXDUR
        """
        
        normalized_msg = self._normalize(message)
        
        # 🚨 1. JSON RULES (əgər varsa)
        rule_based_state = self._check_state_rules(message, mood, intent)
        if rule_based_state:
            print(f"   🎯 EmotionalState JSON Rule: {rule_based_state}")
            return rule_based_state
        
        # 🚨 2. PRICE COMPLAINT → MƏCBURİ dissatisfied
        price_keywords = ["baha", "bahadır", "qiymət", "pahalı", "ucuz deyil"]
        if any(kw in normalized_msg for kw in price_keywords) and intent == "complaint":
            print(f"   🚨 EmotionalState: Price complaint → dissatisfied")
            return "dissatisfied"
        
        # 🚨 3. ANGRY MOOD + ANGRY KEYWORDS → angry
        angry_keywords = ["əsəbi", "hirsli", "qəzəbli", "acıqlı", "kefim pis", "sinirlendim"]
        if mood == "angry" and any(kw in normalized_msg for kw in angry_keywords):
            print(f"   🚨 EmotionalState: Angry mood + keywords → angry")
            return "angry"
        
        # 🚨 4. SUAL İŞARƏSİ → inquiring
        if "?" in message or any(q in normalized_msg for q in ["necə", "niyə", "neçə", "nədir", "hardan", "hara"]):
            print(f"   ❓ EmotionalState: Question → inquiring")
            return "inquiring"
        
        # 🚨 5. POSITIVE FEEDBACK → satisfied
        positive_keywords = ["yaxşı", "məmnunam", "təşəkkür", "sağ ol", "əla", "çox yaxşı"]
        if intent == "positive_feedback" or any(kw in normalized_msg for kw in positive_keywords):
            print(f"   👍 EmotionalState: Positive → satisfied")
            return "satisfied"
        
        # 🚨 6. COMPLAINT INTENT → dissatisfied (ümumi)
        if intent == "complaint":
            print(f"   ⚠️ EmotionalState: Complaint → dissatisfied")
            return "dissatisfied"
        
        # 🚨 7. MOOD-based emotional state
        mood_to_state = {
            "angry": "angry",
            "frustrated": "frustrated",
            "sad": "sad",
            "stressed": "tense",
            "happy": "joyful",
            "satisfied": "satisfied",
            "thinking": "thinking",
            "neutral": "neutral"
        }
        
        state = mood_to_state.get(mood, self.default_state)
        print(f"   🔄 EmotionalState: Mood-based → {state}")
        return state


# GLOBAL INSTANCE
emotional_state_engine = EmotionalStateEngine()