"""
Memory-dən OXUYAN köprü
❌ YAZMIR
✅ Yalnız OXUYUR
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class MemoryBridge:
    def __init__(self, base_path: str = "storage/data/telegram"):
        self.base_path = Path(base_path)
    
    def load_customer_brain(self, user_id: str) -> Dict[str, Any]:
        """
        Müştərinin 6 beyin faylını yükləyir
        
        Returns:
            dict: Beyin layları (identity, psychology, sales, ...)
        """
        customer_path = self.base_path / "customers" / str(user_id)
        
        if not customer_path.exists():
            return {}
        
        brain_layers = {}
        
        # 6 BEYİN FAYLI
        layers = [
            "identity", "behavior", "psychology",
            "intent_interest", "relationship", "sales"
        ]
        
        for layer in layers:
            file_path = customer_path / f"{layer}.json"
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        brain_layers[layer] = json.load(f)
                except:
                    brain_layers[layer] = {}
        
        return brain_layers
    
    def get_operator_status(self, user_id: str) -> Dict[str, Any]:
        """Operator handoff statusunu oxu"""
        control_file = self.base_path / "control" / "operator_handoff.json"
        
        if control_file.exists():
            try:
                with open(control_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(str(user_id), {"active": False})
            except:
                pass
        
        return {"active": False}
    
    def get_recent_conversations(self, user_id: str, limit: int = 5) -> list:
        """Son konversasiyaları al"""
        conv_path = self.base_path / "conversations" / str(user_id)
        
        if not conv_path.exists():
            return []
        
        # Son günün faylını tap
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = conv_path / f"{today}.json"
        
        conversations = []
        
        if today_file.exists():
            try:
                with open(today_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        conversations = data[-limit:]
            except:
                pass
        
        return conversations