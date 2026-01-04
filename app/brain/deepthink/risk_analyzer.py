"""
Risk analizi aparır
❌ Qərar vermir, yalnız riski qiymətləndirir
"""
from typing import Dict, Any

class RiskAnalyzer:
    def __init__(self, rules):
        self.rules = rules
    
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Risk analizi aparır
        
        Returns:
            dict: Risk analizi nəticələri
        """
        customer = context.get("customer", {})
        signals = context.get("signals", {})
        
        # Risk xallarını topla
        risk_score = 0
        risk_factors = []
        
        # 1. Psixoloji risklər
        psychology = customer.get("psychology", {})
        emotional_state = psychology.get("emotional_state", {})
        
        anger_level = emotional_state.get("anger_level", 0)
        stress_level = emotional_state.get("stress_level", 0)
        
        if anger_level > self.rules["psychology"]["anger_thresholds"]["high"]:
            risk_score += 8
            risk_factors.append("yüksək_qəzəb")
        elif anger_level > self.rules["psychology"]["anger_thresholds"]["medium"]:
            risk_score += 5
            risk_factors.append("orta_qəzəb")
        
        if stress_level > self.rules["psychology"]["stress_thresholds"]["high"]:
            risk_score += 6
            risk_factors.append("yüksək_stress")
        elif stress_level > self.rules["psychology"]["stress_thresholds"]["medium"]:
            risk_score += 3
            risk_factors.append("orta_stress")
        
        # 2. Münasibət riskləri
        relationship = customer.get("relationship", {})
        issues_reported = relationship.get("issues_reported", 0)
        
        if issues_reported >= 2:
            risk_score += 4
            risk_factors.append("çoxlu_problem")
        elif issues_reported >= 1:
            risk_score += 2
            risk_factors.append("problem_tarixi")
        
        # 3. Cari mesaj riskləri
        if signals.get("risk", {}).get("has_anger_words", False):
            risk_score += 7
            risk_factors.append("təhqirli_dil")
        
        if signals.get("risk", {}).get("has_urgent_words", False):
            risk_score += 3
            risk_factors.append("təcili_tələb")
        
        # 4. İstifadəçi etibarlılığı
        identity = customer.get("identity", {})
        trust_score = identity.get("trust_score", 50)
        
        if trust_score < 30:
            risk_score += 3
            risk_factors.append("aşağı_etibar")
        
        # Risk səviyyəsini müəyyənləşdir
        if risk_score >= 12:
            risk_level = "critical"
            action = "immediate_handoff"
            description = "Yüksək risk - Operator dərhal tələb olunur"
        elif risk_score >= 8:
            risk_level = "high"
            action = "urgent_handoff"
            description = "Risk yüksək - Operator köməyi tələb olunur"
        elif risk_score >= 5:
            risk_level = "medium"
            action = "monitor"
            description = "Orta risk - Diqqətlə monitorinq edilməlidir"
        elif risk_score >= 2:
            risk_level = "low"
            action = "continue"
            description = "Aşağı risk - Normal davam edilə bilər"
        else:
            risk_level = "none"
            action = "continue"
            description = "Risk yoxdur - Rahat davam edin"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(20, risk_score),  # Maksimum 20 xal
            "risk_factors": risk_factors,
            "recommended_action": action,
            "description": description,
            "details": {
                "anger_risk": anger_level,
                "stress_risk": stress_level,
                "trust_risk": 100 - trust_score,
                "issues_risk": issues_reported * 2
            }
        }