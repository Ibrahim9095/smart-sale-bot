"""
Satış potensialını qiymətləndirir
"""
from typing import Dict, Any

class SalesJudger:
    def __init__(self, rules):
        self.rules = rules
    
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Satış potensialını analiz edir
        
        Returns:
            dict: Satış analizi nəticələsi
        """
        customer = context.get("customer", {})
        signals = context.get("signals", {})
        sales_data = customer.get("sales", {})
        psychology = customer.get("psychology", {})
        
        # Lead score və satış mərhələsi
        lead_score = sales_data.get("lead_score", 0)
        sales_stage = sales_data.get("sales_stage", "cold")
        price_sensitivity = sales_data.get("price_sensitivity", 5)
        
        # Satışa icazə olub-olmadığını yoxla
        sales_allowed = True
        sales_block_reasons = []
        
        # Bloklama şərtləri
        mood = psychology.get("current_mood", "neutral")
        if mood == "angry":
            sales_allowed = False
            sales_block_reasons.append("müştəri_qəzəbli")
        
        emotional_state = psychology.get("emotional_state", {})
        if emotional_state.get("anger_level", 0) > 5:
            sales_allowed = False
            sales_block_reasons.append("yüksək_qəzəb")
        
        if emotional_state.get("stress_level", 0) > 6:
            sales_allowed = False
            sales_block_reasons.append("yüksək_stress")
        
        # Satış mərhələsinə görə yanaşma
        if not sales_allowed:
            approach = "off"
            confidence = 0.1
        else:
            # Lead score əsasında yanaşma
            if lead_score > self.rules["sales"]["lead_score_thresholds"]["hot"]:
                approach = "closing"
                confidence = 0.85
            elif lead_score > self.rules["sales"]["lead_score_thresholds"]["warm"]:
                approach = "aggressive"
                confidence = 0.70
            elif lead_score > self.rules["sales"]["lead_score_thresholds"]["cold"]:
                approach = "normal"
                confidence = 0.60
            else:
                approach = "soft"
                confidence = 0.40
        
        # Qiymət həssaslığına görə strategiya
        if price_sensitivity > 7:
            pricing_strategy = "budget_focused"
            discount_mentions = "frequent"
        elif price_sensitivity > 4:
            pricing_strategy = "value_focused"
            discount_mentions = "occasional"
        else:
            pricing_strategy = "premium_focused"
            discount_mentions = "rare"
        
        # Cari mesajda satış siqnalı var?
        has_sales_signal = (
            signals.get("sales", {}).get("has_price_words", False) or
            signals.get("sales", {}).get("has_product_words", False) or
            signals.get("sales", {}).get("has_purchase_intent", False)
        )
        
        # Dönüşüm ehtimalı
        conversion_likelihood = self._calculate_conversion_likelihood(
            lead_score, sales_stage, psychology
        )
        
        return {
            "sales_allowed": sales_allowed,
            "sales_block_reasons": sales_block_reasons,
            "sales_approach": approach,
            "pricing_strategy": pricing_strategy,
            "discount_mentions": discount_mentions,
            "has_sales_signal": has_sales_signal,
            "conversion_likelihood": conversion_likelihood,
            "confidence": confidence,
            "recommended_action": self._get_recommended_action(approach, has_sales_signal)
        }
    
    def _calculate_conversion_likelihood(self, lead_score: int, sales_stage: str, psychology: Dict[str, Any]) -> int:
        """Dönüşüm ehtimalını hesabla"""
        base_score = lead_score
        
        # Psixoloji faktor
        mood = psychology.get("current_mood", "neutral")
        if mood == "positive":
            base_score += 20
        elif mood == "angry":
            base_score -= 30
        elif mood == "stressed":
            base_score -= 15
        
        # Satış mərhələsi
        stage_multipliers = {
            "cold": 0.5,
            "warm": 1.0,
            "hot": 1.5
        }
        multiplier = stage_multipliers.get(sales_stage, 1.0)
        final_score = base_score * multiplier
        
        return max(0, min(100, int(final_score)))
    
    def _get_recommended_action(self, approach: str, has_signal: bool) -> str:
        """Tövsiyə olunan hərəkəti müəyyənləşdir"""
        if approach == "off":
            return "avoid_sales"
        elif approach == "closing":
            return "push_for_conversion"
        elif approach == "aggressive":
            return "present_offer"
        elif approach == "normal":
            return "provide_information"
        elif approach == "soft":
            return "build_interest" if has_signal else "wait_for_signal"
        else:
            return "monitor"