#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEEPTHINK - RULE-BASED EMOTION ENGINE v4.2
🚨 PSYCHOLOGY FIX: Price Complaint → Mood RESET
🚨 STATELESS: Keçmiş mood SAXLANMIR
🚨 REAL HUMAN: Hər mesaj üçün SIFIRDAN hesablanır
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class DeepThink:
    def __init__(self):
        self.rules_path = Path(__file__).parent / "psychology_rules.json"
        self.unknown_path = Path(__file__).parent / "unknown.json"

        # ❌ QADAĞA: Angry heç vaxt Price Complaint üçün qalmamalı
        # 🚨 PRICE COMPLAINT RESET: "baha" → mood=neutral
        self.price_reset_keywords = [
            "baha", "bahadır", "çox baha", "qiymət", "pahalı", "ucuz deyil",
            "puluna dəyməz", "qiymət çox yüksəkdir"
        ]

        self.category_order = [
            "abuse",
            "threat", 
            "blackmail",
            "accusation",
            "harassment",
            "urgency",
            "anger",
            "frustration",
            "sadness",
            "stress",
            "joy",
            "satisfaction",
            "thinking_state",
            "non_emotional"
        ]

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

        self.critical_categories = [
            "abuse", "threat", "blackmail", "accusation", "harassment", "urgency"
        ]

        self.repeated_chars_regex = re.compile(r'(.)\1{2,}')

    def _load_rules(self) -> Dict:
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _normalize_text_v2(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\sğüşıöçə]', ' ', text)
        text = self.repeated_chars_regex.sub(r'\1\1', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _is_price_complaint(self, normalized_text: str) -> bool:
        """🚨 PRICE COMPLAINT DETECTION: Angry-ni RESET edir"""
        for keyword in self.price_reset_keywords:
            if keyword in normalized_text:
                return True
        return False

    def analyze(self, message: str, platform: str = "telegram") -> Optional[Dict[str, Any]]:
        """
        🚨 PSYCHOLOGY FIX: 
        - Hər mesaj SIFIRDAN analiz edilir
        - Price complaint varsa → mood=neutral (angry YOX)
        - Keçmiş mood YOXDUR
        """
        
        normalized = self._normalize_text_v2(message)
        if not normalized:
            return self._create_result("non_emotional", "", message)

        # 🚨 1. ƏVVƏL PRICE COMPLAINT CHECK (MƏCBURİ RESET)
        if self._is_price_complaint(normalized):
            print(f"   🚨 PSYCHOLOGY RESET: Price complaint → mood=neutral")
            return self._create_result("price_complaint", "price_reset", message)

        # 2. NORMAL RULE MATCHING
        rules = self._load_rules()
        matched_category = None
        matched_phrase = ""

        for category in self.category_order:
            if category in rules:
                for phrase in rules[category].get("phrases", []):
                    if phrase and phrase in normalized:
                        matched_category = category
                        matched_phrase = phrase
                        break
            if matched_category:
                break

        if not matched_category:
            return None

        # 3. ANGRY DETECT EDİLİBSƏ, amma price complaint-dən SONRA?
        # Burada onsuz da price complaint yoxdursa, normal qaydada davam edirik
        return self._create_result(matched_category, matched_phrase, message)

    def _create_result(self, category: str, phrase: str, message: str) -> Dict[str, Any]:
        """🚨 QEYD: emotional_state-i burada YOX, EmotionalStateEngine hesablayır"""
        
        # Price complaint üçün xüsusi işləmə
        if category == "price_complaint":
            return {
                "current_mood": "neutral",  # 🚨 MƏCBURİ RESET
                "emotional_state": "calm",  # EmotionalStateEngine override edəcək
                "last_message_type": "price_complaint",
                "last_reason": f"price_complaint_reset:{phrase}",
                "operator_required": False,
                "updated_at": datetime.now().isoformat()
            }
        
        return {
            "current_mood": self.category_to_mood.get(category, "neutral"),
            "emotional_state": self.category_to_emotional_state.get(category, "calm"),
            "last_message_type": category,
            "last_reason": f"{category}_phrase:{phrase}",
            "operator_required": category in self.critical_categories,
            "updated_at": datetime.now().isoformat()
        }


# GLOBAL INSTANCE
deepthink = DeepThink()


def analyze_psychology(message: str, intent: str) -> Dict[str, Any]:
    """
    🚨 ORKESTRATOR FUNCTION (memory.py üçün)
    - mood → deepthink (STATELESS)
    - emotional_state → EmotionalStateEngine (STATELESS)
    """
    # 1. Mood-u tap (keçmiş YOX)
    mood_result = deepthink.analyze(message)
    
    if not mood_result:
        current_mood = "neutral"
        last_message_type = "unknown"
        operator_required = False
        last_reason = "unknown_phrase"
    else:
        current_mood = mood_result.get("current_mood", "neutral")
        last_message_type = mood_result.get("last_message_type", "unknown")
        operator_required = mood_result.get("operator_required", False)
        last_reason = mood_result.get("last_reason", "")
    
    # 2. Emotional State-i hesabla (keçmiş YOX)
    # Sadə emotional state məntiqi - JSON rules yoxdursa
    emotional_state = _derive_simple_emotional_state(message, current_mood, intent)
    
    # 3. Nəticəni qaytar
    return {
        "current_mood": current_mood,
        "emotional_state": emotional_state,
        "last_message_type": last_message_type,
        "last_reason": last_reason,
        "operator_required": operator_required,
        "updated_at": datetime.now().isoformat()
    }


def _derive_simple_emotional_state(message: str, mood: str, intent: str) -> str:
    """
    Sadə emotional state məntiqi
    JSON rules yoxdursa, bu funksiya işləyəcək
    """
    message_lower = message.lower()
    
    # 🚨 PRICE COMPLAINT → MƏCBURİ dissatisfied
    price_keywords = ["baha", "bahadır", "qiymət", "pahalı", "ucuz deyil"]
    if any(kw in message_lower for kw in price_keywords) and intent == "complaint":
        return "dissatisfied"
    
    # 🚨 ANGRY MOOD + ANGRY KEYWORDS → angry
    angry_keywords = ["əsəbi", "hirsli", "qəzəbli", "acıqlı", "kefim pis", "sinirlendim"]
    if mood == "angry" and any(kw in message_lower for kw in angry_keywords):
        return "angry"
    
    # 🚨 SUAL İŞARƏSİ → inquiring
    if "?" in message or any(q in message_lower for q in ["necə", "niyə", "neçə", "nədir", "hardan", "hara"]):
        return "inquiring"
    
    # 🚨 POSITIVE FEEDBACK → satisfied
    positive_keywords = ["yaxşı", "məmnunam", "təşəkkür", "sağ ol", "əla", "çox yaxşı"]
    if intent == "positive_feedback" or any(kw in message_lower for kw in positive_keywords):
        return "satisfied"
    
    # 🚨 COMPLAINT INTENT → dissatisfied (ümumi)
    if intent == "complaint":
        return "dissatisfied"
    
    # 🚨 MOOD-based emotional state
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
    
    return mood_to_state.get(mood, "neutral")