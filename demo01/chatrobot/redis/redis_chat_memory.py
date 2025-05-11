from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any

class LimitedRedisChatMemory(ConversationBufferMemory):
    """限制只保留最近N条消息的记忆类"""
    max_history: int = 10
    
    def __init__(self, max_history: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.max_history = max_history
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """加载记忆变量，只返回最近N条消息"""
        history = super().load_memory_variables(inputs)
        if isinstance(history[self.memory_key], list):
            history[self.memory_key] = history[self.memory_key][-self.max_history:]
        return history    