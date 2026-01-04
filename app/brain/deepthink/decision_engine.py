"""
Bütün analizləri birləşdirir, yekun qərarı verir
"""
from typing import Dict, Any
import json
from pathlib import Path

class DecisionEngine:
    def __init__(self, rules_path: str = "app/brain/rules"):
        self.rules = self._load_rules(rules_path)
    
    def _load_rules(self, rules_path: str) -> Dict[str, Any]:
        """Biznes qaydalarını yüklə"""
        rules = {}
        path = Path(rules_path)
        
        rule_files = {
            "psychology": "psychology_rules.json",
            "sales": "sales_rules.json",
            "operator": "operator_rules.json"
        }
        
        for rule_type, filename in rule_files.items():
            file_path = path / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    rules[rule_type] = json.load(f)
            else:
                rules[rule_type] = self._get_default_rules(rule_type)
        
        return rules
    
    def _get_default_rules(self, rule_type: str) -> Dict[str, Any]:
        """Default qaydalar"""
        if rule_type == "psychology":
            return {
                "anger_threshold": 5,
                "stress_threshold": 6,
                "mood_mapping": {
                    "angry": {"tone": "calm", "action": "deescalate"},
                    "stressed": {"tone": "empathetic", "action": "comfort"},
                    "positive": {"tone": "friendly", "action": "engage"}
                }
            }
        elif rule_type == "sales":
            return {
                "lead_thresholds": {
                    "cold": 30,
                    "warm": 60,
                    "hot": 80
                },
                "approach_mapping": {
                    "cold": {"mode": "soft", "focus": "awareness"},
                    "warm": {"mode": "normal", "focus": "interest"},
                    "hot": {"mode": "aggressive", "focus": "conversion"}
                }
            }
        else:  # operator
            return {
                "handoff_conditions": [
                    {"risk_level": "critical", "immediate": True},
                    {"risk_level": "high", "urgent": True},
                    {"complaints": 2, "within_hours": 24},
                    {"explicit_request": True}
                ]
            }
    
    def decide(self, 
               context: Dict[str, Any],
               risk_analysis: Dict[str, Any],
               intent_analysis: Dict[str, Any],
               sales_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Yekun qərarı verir
        Returns: {
            "core_decision": {...},
            "reasoning": {...},
            "applied_rules": [...]
        }
        """
        applied_rules = []
        
        # 1. Operator qərarı
        operator_decision = self._decide_operator(
            context, risk_analysis, intent_analysis, applied_rules
        )
        
        # 2. Ton qərarı
        tone_decision = self._decide_tone(
            context, risk_analysis, applied_rules
        )
        
        # 3. Uzunluq qərarı
        length_decision = self._decide_length(
            context, intent_analysis, applied_rules
        )
        
        # 4. Satış qərarı
        sales_decision = self._decide_sales(
            context, sales_analysis, risk_analysis, applied_rules
        )
        
        # 5. Növbəti hərəkət
        next_action = self._decide_next_action(
            operator_decision, risk_analysis, intent_analysis
        )
        
        return {
            "core_decision": {
                "operator_required": operator_decision["required"],
                "tone": tone_decision["tone"],
                "length": length_decision["length"],
                "sales_mode": sales_decision["mode"],
                "priority": risk_analysis["risk_level"],
                "next_action": next_action
            },
            "reasoning": {
                "operator_reason": operator_decision["reason"],
                "tone_reason": tone_decision["reason"],
                "sales_reason": sales_decision["reason"],
                "risk_summary": {
                    "level": risk_analysis["risk_level"],
                    "score": risk_analysis["risk_score"],
                    "primary": risk_analysis["primary_risk"]
                }
            },
            "applied_rules": applied_rules,
            "confidence": self._calculate_overall_confidence(
                risk_analysis, intent_analysis, sales_analysis
            )
        }
    
    def _decide_operator(self, context: Dict[str, Any], 
                        risk_analysis: Dict[str, Any],
                        intent_analysis: Dict[str, Any],
                        applied_rules: list) -> Dict[str, Any]:
        """Operator lazımdır?"""
        reasons = []
        required = False
        
        # 1. Risk əsasında
        if risk_analysis["risk_level"] in ["critical", "high"]:
            required = True
            reasons.append(f"Yüksək risk: {risk_analysis['risk_level']}")
            applied_rules.append("operator_risk_threshold")
        
        # 2. Niyyət əsasında
        if intent_analysis.get("requires_human", False):
            required = True
            reasons.append(f"Operator tələb edən niyyət: {intent_analysis['primary_intent']}")
            applied_rules.append("operator_intent_requirement")
        
        # 3. Psixoloji vəziyyət
        psycho = context.get("psychological_state", {})
        if psycho.get("anger", 0) > self.rules["psychology"]["anger_threshold"]:
            required = True
            reasons.append(f"Yüksək qəzəb səviyyəsi: {psycho.get('anger')}")
            applied_rules.append("operator_anger_threshold")
        
        # 4. Açıq sorğu
        message = context.get("current_situation", {}).get("message", "").lower()
        if any(word in message for word in ["operator", "menecer", "insan", "canlı"]):
            required = True
            reasons.append("Müştəri operator sorğusu")
            applied_rules.append("operator_explicit_request")
        
        return {
            "required": required,
            "reason": "; ".join(reasons) if reasons else "Operator tələb olunmur"
        }
    
    def _decide_tone(self, context: Dict[str, Any],
                    risk_analysis: Dict[str, Any],
                    applied_rules: list) -> Dict[str, Any]:
        """Cavab tonunu müəyyənləşdir"""
        psycho = context.get("psychological_state", {})
        mood = psycho.get("mood", "neutral")
        risk_level = risk_analysis["risk_level"]
        
        # Risk əsasında ton
        if risk_level in ["critical", "high"]:
            tone = "calm"
            reason = "Yüksək risk vəziyyəti"
            applied_rules.append("tone_high_risk")
        elif mood in self.rules["psychology"]["mood_mapping"]:
            tone = self.rules["psychology"]["mood_mapping"][mood]["tone"]
            reason = f"Müştəri əhvali: {mood}"
            applied_rules.append(f"tone_mood_{mood}")
        else:
            tone = "professional"
            reason = "Standart peşəkar ünsiyyət"
        
        return {"tone": tone, "reason": reason}
    
    def _decide_length(self, context: Dict[str, Any],
                      intent_analysis: Dict[str, Any],
                      applied_rules: list) -> Dict[str, Any]:
        """Cavab uzunluğunu müəyyənləşdir"""
        intent = intent_analysis["primary_intent"]
        urgency = intent_analysis["urgency"]
        
        if urgency == "high":
            length = "short"
            reason = "Təcili vəziyyət"
            applied_rules.append("length_urgent")
        elif intent in ["greeting", "gratitude"]:
            length = "short"
            reason = "Sadə sosial qarşılıq"
            applied_rules.append("length_social")
        elif intent in ["info", "sales"]:
            length = "medium"
            reason = "İnformativ cavab tələb olunur"
            applied_rules.append("length_informative")
        elif intent == "complaint":
            length = "long"
            reason = "Ətraflı izahat və empatiya tələb olunur"
            applied_rules.append("length_complaint")
        else:
            length = "medium"
            reason = "Standart cavab uzunluğu"
        
        return {"length": length, "reason": reason}
    
    def _decide_sales(self, context: Dict[str, Any],
                     sales_analysis: Dict[str, Any],
                     risk_analysis: Dict[str, Any],
                     applied_rules: list) -> Dict[str, Any]:
        """Satış rejimini müəyyənləşdir"""
        if not sales_analysis["sales_allowed"]:
            return {
                "mode": "off",
                "reason": sales_analysis.get("reason", "Satış üçün uyğun deyil")
            }
        
        # Risk yüksəkdirsə, satış yox
        if risk_analysis["risk_level"] in ["critical", "high"]:
            applied_rules.append("sales_risk_block")
            return {
                "mode": "off",
                "reason": "Risk səviyyəsi satışa mane olur"
            }
        
        approach = sales_analysis["sales_approach"]
        
        if approach == "closing":
            reason = "Sıcak lead, bağlama mərhələsi"
            applied_rules.append("sales_closing")
        elif approach == "aggressive":
            reason = "İsti lead, aktiv satış"
            applied_rules.append("sales_aggressive")
        elif approach == "normal":
            reason = "Standart satış yanaşması"
            applied_rules.append("sales_normal")
        elif approach == "soft":
            reason = "Soyuq lead, yumşaq yanaşma"
            applied_rules.append("sales_soft")
        else:
            reason = "Satış rejimi deaktiv"
            applied_rules.append("sales_off")
        
        return {"mode": approach, "reason": reason}
    
    def _decide_next_action(self,
                           operator_decision: Dict[str, Any],
                           risk_analysis: Dict[str, Any],
                           intent_analysis: Dict[str, Any]) -> str:
        """Növbəti hərəkəti müəyyənləşdir"""
        if operator_decision["required"]:
            return "handoff_to_operator"
        
        if risk_analysis["immediate_action"] != "continue":
            return risk_analysis["immediate_action"]
        
        if intent_analysis["primary_intent"] == "sales":
            return "continue_sales_conversation"
        
        return "continue_support"
    
    def _calculate_overall_confidence(self,
                                    risk_analysis: Dict[str, Any],
                                    intent_analysis: Dict[str, Any],
                                    sales_analysis: Dict[str, Any]) -> float:
        """Ümumi etibarlılıq səviyyəsi"""
        scores = []
        
        # Risk analizi etibarlılığı
        risk_score = risk_analysis.get("risk_score", 0)
        if risk_score > 7:
            scores.append(0.9)  # Yüksək risk aydındır
        elif risk_score > 4:
            scores.append(0.7)
        else:
            scores.append(0.5)
        
        # Niyyət analizi etibarlılığı
        scores.append(intent_analysis.get("confidence", 0.5))
        
        # Satış analizi etibarlılığı
        scores.append(sales_analysis.get("confidence", 0.5))
        
        # Ortalama
        return sum(scores) / len(scores)