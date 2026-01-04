"""
DeepThink - AI Business Brain
❌ MESAJ YAZMIR
❌ JSON YAZMIR
✅ Yalnız QƏRAR VERİR
"""
import json
from pathlib import Path
from typing import Dict, Any

from .context_builder import ContextBuilder
from .risk_analyzer import RiskAnalyzer
from .intent_router import IntentRouter
from .sales_judger import SalesJudger
from .decision_engine import DecisionEngine
from .output_strategy import OutputStrategy

class DeepThink:
    """AI Business Brain - Qərarverici sistem"""
    
    def __init__(self, memory_bridge):
        self.memory_bridge = memory_bridge
        self.rules = self._load_rules()
        
        # Komponentləri yüklə
        self.context_builder = ContextBuilder(memory_bridge)
        self.risk_analyzer = RiskAnalyzer(self.rules)
        self.intent_router = IntentRouter()
        self.sales_judger = SalesJudger(self.rules)
        self.decision_engine = DecisionEngine(self.rules)
        self.output_strategy = OutputStrategy()
    
    def _load_rules(self) -> Dict[str, Any]:
        """Biznes qaydalarını yüklə"""
        rules_path = Path(__file__).parent.parent / "rules"
        rules = {}
        
        rule_files = {
            "psychology": "psychology_rules.json",
            "sales": "sales_rules.json",
            "operator": "operator_rules.json"
        }
        
        for rule_type, filename in rule_files.items():
            file_path = rules_path / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    rules[rule_type] = json.load(f)
            else:
                # Default qaydalar
                rules[rule_type] = self._get_default_rules(rule_type)
        
        return rules
    
    def _get_default_rules(self, rule_type: str) -> Dict[str, Any]:
        """Default qaydalar"""
        if rule_type == "psychology":
            return {
                "mood_mapping": {
                    "angry": {"tone": "calm", "action": "deescalate"},
                    "stressed": {"tone": "empathetic", "action": "comfort"},
                    "positive": {"tone": "friendly", "action": "engage"},
                    "neutral": {"tone": "professional", "action": "continue"}
                },
                "stress_thresholds": {"low": 3, "medium": 6, "high": 8},
                "anger_thresholds": {"low": 2, "medium": 5, "high": 7}
            }
        elif rule_type == "sales":
            return {
                "lead_score_thresholds": {"cold": 30, "warm": 60, "hot": 80},
                "sales_approach_mapping": {
                    "cold": {"approach": "soft", "focus": "awareness"},
                    "warm": {"approach": "normal", "focus": "interest"},
                    "hot": {"approach": "aggressive", "focus": "conversion"}
                }
            }
        else:  # operator
            return {
                "handoff_conditions": [
                    {"condition": "risk_level", "threshold": "high", "reason": "Risk yüksək"},
                    {"condition": "explicit_request", "keywords": ["operator"], "reason": "Operator sorğusu"}
                ]
            }
    
    def analyze(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Əsas analiz funksiyası
        
        Args:
            user_id: Telegram user ID
            message: İstifadəçi mesajı
            
        Returns:
            dict: Bot üçün strategiya
        """
        try:
            # 1. Kontekst qur
            context = self.context_builder.build_context(user_id, message)
            
            # 2. Paralel analizlər
            risk_analysis = self.risk_analyzer.analyze(context)
            intent_analysis = self.intent_router.analyze(context)
            sales_analysis = self.sales_judger.analyze(context)
            
            # 3. Qərar ver
            decision = self.decision_engine.decide(
                context, risk_analysis, intent_analysis, sales_analysis
            )
            
            # 4. Strategiya formatla
            strategy = self.output_strategy.format(
                decision, context, 
                {"risk": risk_analysis, "intent": intent_analysis, "sales": sales_analysis}
            )
            
            # 5. Nəticəni qaytar
            return {
                "success": True,
                "strategy": {
                    "tone": strategy.tone,
                    "length": strategy.length,
                    "intent": strategy.intent,
                    "risk_level": strategy.risk_level,
                    "call_operator": strategy.call_operator,
                    "sales_allowed": strategy.sales_allowed,
                    "sales_approach": strategy.sales_approach,
                    "next_action": strategy.next_action,
                    "confidence": strategy.confidence,
                    "notes": strategy.notes
                },
                "analysis": {
                    "risk": risk_analysis,
                    "intent": intent_analysis,
                    "sales": sales_analysis
                },
                "context_summary": {
                    "user_id": user_id,
                    "message_preview": message[:100],
                    "customer_exists": bool(context.get("customer", {}).get("identity"))
                }
            }
            
        except Exception as e:
            # Xəta halında default strategiya
            return {
                "success": False,
                "error": str(e),
                "strategy": {
                    "tone": "neutral",
                    "length": "medium",
                    "intent": "support",
                    "risk_level": "medium",
                    "call_operator": False,
                    "sales_allowed": False,
                    "sales_approach": "off",
                    "next_action": "continue_support",
                    "confidence": 0.3,
                    "notes": f"Xəta: {str(e)[:50]}"
                }
            }