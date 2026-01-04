"""
Müştəri niyyətini analiz edir
"""
from typing import Dict, Any

class IntentRouter:
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Müştəri niyyətini təhlil edir
        
        Returns:
            dict: Niyyət analizi nəticələri
        """
        signals = context.get("signals", {})
        intent_signals = signals.get("intent", {})
        customer = context.get("customer", {})
        psychology = customer.get("psychology", {})
        
        # Primary intent müəyyənləşdir
        if intent_signals.get("is_operator_request", False):
            primary_intent = "operator_request"
            confidence = 0.95
        elif intent_signals.get("is_complaint", False):
            primary_intent = "complaint"
            confidence = 0.90
        elif intent_signals.get("is_sales", False):
            primary_intent = "sales_inquiry"
            confidence = 0.85
        elif intent_signals.get("is_question", False):
            primary_intent = "information"
            confidence = 0.80
        elif intent_signals.get("is_thanks", False):
            primary_intent = "gratitude"
            confidence = 0.95
        elif intent_signals.get("is_greeting", False):
            primary_intent = "greeting"
            confidence = 0.98
        else:
            primary_intent = "general_support"
            confidence = 0.60
        
        # Secondary intent (əlavə niyyətlər)
        secondary_intents = []
        current_message = context.get("current", {}).get("message", "").lower()
        
        if "qiymət" in current_message and primary_intent != "sales_inquiry":
            secondary_intents.append("price_check")
        
        if "vaxt" in current_message or "nə vaxt" in current_message:
            secondary_intents.append("timing_inquiry")
        
        if "harada" in current_message or "harda" in current_message:
            secondary_intents.append("location_inquiry")
        
        # Təciliyyət səviyyəsi
        if intent_signals.get("is_operator_request", False) or intent_signals.get("is_complaint", False):
            urgency = "high"
        elif "təcili" in current_message or "dərhal" in current_message:
            urgency = "high"
        else:
            urgency = "normal"
        
        # Psixoloji niyyət əlavəsi
        mood = psychology.get("current_mood", "neutral")
        if mood == "angry" and primary_intent != "complaint":
            secondary_intents.append("emotional_outburst")
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": secondary_intents,
            "urgency": urgency,
            "confidence": confidence,
            "requires_human_judgment": primary_intent in ["complaint", "operator_request"],
            "needs_immediate_response": urgency == "high"
        }