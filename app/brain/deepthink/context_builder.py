"""
DeepThink üçün kontekst qurur
❌ JSON yazmır
❌ Storage dəyişmir
✅ Yalnız memory-dən OXUYUR
"""
from typing import Dict, Any
from datetime import datetime, timedelta

class ContextBuilder:
    def __init__(self, memory_bridge):
        self.memory_bridge = memory_bridge
    
    def build_context(self, user_id: str, current_message: str) -> Dict[str, Any]:
        """
        DeepThink üçün analiz konteksti qurur
        
        Args:
            user_id: Telegram user ID
            current_message: Cari mesaj mətni
            
        Returns:
            dict: Analiz üçün kontekst
        """
        # 1. Memory-dən müştəri beyin fayllarını oxu
        customer_brain = self.memory_bridge.load_customer_brain(user_id)
        
        if not customer_brain:
            # Müştəri tapılmadı - yeni müştəri konteksti
            return self._build_new_customer_context(user_id, current_message)
        
        # 2. Operator statusunu yoxla
        operator_status = self.memory_bridge.get_operator_status(user_id)
        
        # 3. Son konversasiyaları yüklə
        recent_conversations = self.memory_bridge.get_recent_conversations(user_id, limit=5)
        
        # 4. Konteksti qur
        context = {
            # Müştəri məlumatları
            "customer": {
                "user_id": user_id,
                "identity": customer_brain.get("identity", {}),
                "behavior": customer_brain.get("behavior", {}),
                "psychology": customer_brain.get("psychology", {}),
                "intent": customer_brain.get("intent_interest", {}),
                "relationship": customer_brain.get("relationship", {}),
                "sales": customer_brain.get("sales", {})
            },
            
            # Cari vəziyyət
            "current": {
                "message": current_message,
                "message_length": len(current_message),
                "timestamp": datetime.now().isoformat(),
                "operator_active": operator_status.get("active", False)
            },
            
            # Analiz üçün signal-lar
            "signals": self._extract_signals(current_message, customer_brain),
            
            # Tarix
            "history": {
                "conversation_count": len(recent_conversations),
                "has_complaints": self._has_complaints(recent_conversations),
                "last_interaction": self._get_last_interaction(customer_brain)
            }
        }
        
        return context
    
    def _build_new_customer_context(self, user_id: str, message: str) -> Dict[str, Any]:
        """Yeni müştəri üçün kontekst qur"""
        return {
            "customer": {
                "user_id": user_id,
                "identity": {
                    "message_count": 0,
                    "trust_score": 50
                },
                "psychology": {
                    "current_mood": "neutral",
                    "emotional_state": {
                        "anger_level": 0,
                        "stress_level": 0,
                        "happiness_level": 0
                    }
                },
                "relationship": {
                    "relationship_level": 0,
                    "issues_reported": 0
                },
                "sales": {
                    "lead_score": 0,
                    "sales_stage": "cold"
                }
            },
            "current": {
                "message": message,
                "message_length": len(message),
                "timestamp": datetime.now().isoformat(),
                "operator_active": False,
                "is_first_message": True
            },
            "signals": self._extract_signals(message, {}),
            "history": {
                "conversation_count": 0,
                "has_complaints": False,
                "last_interaction": None
            }
        }
    
    def _extract_signals(self, message: str, customer_brain: Dict[str, Any]) -> Dict[str, Any]:
        """Mesajdan signal-ları çıxar"""
        message_lower = message.lower()
        
        signals = {
            "intent": {
                "is_question": "?" in message or any(word in message_lower for word in ["necə", "nə", "niyə", "harda", "nə vaxt"]),
                "is_complaint": any(word in message_lower for word in ["şikayət", "problem", "pis", "narahat", "kömək"]),
                "is_sales": any(word in message_lower for word in ["qiymət", "satın", "almaq", "məhsul", "endirim"]),
                "is_operator_request": any(word in message_lower for word in ["operator", "menecer", "insan", "canlı"]),
                "is_thanks": any(word in message_lower for word in ["sağ ol", "təşəkkür", "thanks"]),
                "is_greeting": any(word in message_lower for word in ["salam", "hello", "hi", "günaydın"])
            },
            "risk": {
                "has_anger_words": any(word in message_lower for word in ["pis", "axmaq", "idiot", "ləğv"]),
                "has_urgent_words": any(word in message_lower for word in ["təcili", "dərhal", "acil", "indi"]),
                "has_negative_words": any(word in message_lower for word in ["problem", "şikayət", "zarar", "itirdim"])
            },
            "sales": {
                "has_price_words": any(word in message_lower for word in ["qiymət", "bahalı", "ucuz", "endirim"]),
                "has_product_words": any(word in message_lower for word in ["məhsul", "ürün", "paket", "xidmət"]),
                "has_purchase_intent": any(word in message_lower for word in ["almaq", "satın", "sifariş", "bağla"])
            }
        }
        
        return signals
    
    def _has_complaints(self, conversations: list) -> bool:
        """Konversasiyalarda şikayət var?"""
        if not conversations:
            return False
        
        for conv in conversations[-3:]:  # Son 3 konversasiyaya bax
            if isinstance(conv, dict):
                message = conv.get("user_message", "").lower()
                if any(word in message for word in ["şikayət", "problem", "pis"]):
                    return True
        return False
    
    def _get_last_interaction(self, customer_brain: Dict[str, Any]) -> str:
        """Son qarşılıqlı əlaqəni tap"""
        identity = customer_brain.get("identity", {})
        return identity.get("last_seen", datetime.now().isoformat())