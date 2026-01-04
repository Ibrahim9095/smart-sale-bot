"""
Brain paketi - Memory və DeepThink sistemləri
"""
from .memory_bridge import MemoryBridge
from .deepthink import DeepThink

# Brain factory funksiyası
def create_brain_system(base_path: str = "storage/data/telegram"):
    """
    Tam brain sistemini yaradır
    Returns: (memory_bridge, deepthink)
    """
    memory_bridge = MemoryBridge(base_path)
    deepthink = DeepThink(memory_bridge)
    
    return memory_bridge, deepthink

__all__ = ['MemoryBridge', 'DeepThink', 'create_brain_system']