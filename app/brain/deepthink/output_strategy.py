"""
DeepThink çıxışını formatlayır - BOT.PY üçün strategiya
❌ MESAJ YAZMIR
✅ Yalnız STRATEGİYA qaytarır
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BusinessStrategy:
    """
    Bot.py üçün strategiya obyekti
    Bu obyekt BOT-un NECƏ cavab verməli olduğunu deyir
    """
    tone: str  # "neutral", "friendly", "serious", "sales", "calm", "empathetic"
    length: str  # "short", "medium", "long"
    intent: str  # "support", "sales", "info", "operator", "deescalate"
    risk_level: str  # "low", "medium", "high", "critical"
    call_operator: bool
    sales_allowed: bool
    sales_approach: str  # "off", "soft", "normal", "aggressive", "closing"
    next_action: str
    confidence: float  # 0-1
    notes: str  # Bot üçün qısa izahat

class OutputStrategy:
    def format(self, decision, context, analyses) -> BusinessStrategy:
        """
        Qərarı bot üçün strategiya formatına çevirir
        
        Args:
            decision: BusinessDecision obyekti
            context: Kontekst məlumatları
            analyses: Bütün analiz nəticələri
            
        Returns:
            BusinessStrategy: Bot üçün strategiya
        """
        # Intent mapping
        intent_map = {
            "handoff_to_operator": "operator",
            "push_for_conversion": "sales",
            "provide_sales_info": "sales",
            "deescalate": "deescalate",
            "continue_support": "support",
            "provide_information": "info"
        }
        
        intent = intent_map.get(decision.next_action, "support")
        
        # Notes generation
        notes = self._generate_notes(decision, context, analyses)
        
        return BusinessStrategy(
            tone=decision.tone,
            length=decision.length,
            intent=intent,
            risk_level=analyses["risk"]["risk_level"],
            call_operator=decision.operator_required,
            sales_allowed=decision.sales_mode != "off",
            sales_approach=decision.sales_mode,
            next_action=decision.next_action,
            confidence=decision.confidence,
            notes=notes
        )
    
    def _generate_notes(self, decision, context, analyses) -> str:
        """Bot üçün izahat qeydləri"""
        notes = []
        
        # Operator qeydləri
        if decision.operator_required:
            notes.append(f"🚨 OPERATOR: {decision.reasoning.split('|')[0]}")
        
        # Risk qeydləri
        risk = analyses["risk"]
        if risk["risk_level"] in ["high", "critical"]:
            notes.append(f"⚠️ RİSK: {risk['risk_level']} ({risk['risk_score']})")
        
        # Satış qeydləri
        sales = analyses["sales"]
        if sales["sales_allowed"] and sales["sales_approach"] != "off":
            notes.append(f"💰 SATIŞ: {sales['sales_approach']}")
        else:
            notes.append("🚫 SATIŞ YOX")
        
        # Ünsiyyət qeydləri
        notes.append(f"🎭 TON: {decision.tone}")
        notes.append(f"📏 UZUNLUQ: {decision.length}")
        
        return " | ".join(notes)