from langchain.memory import RedisChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict

# Redis连接配置
REDIS_URL = "redis://localhost:6379/0"  # 根据你的Redis配置修改

def get_redis_history(session_id: str) -> RedisChatMessageHistory: 
    """获取Redis聊天历史"""
    return RedisChatMessageHistory(
        url=REDIS_URL,
        session_id=session_id,  # 使用用户ID或会话ID作为session_id
        ttl=1200,  # 数据过期时间(秒)，设为None则永不过期
    )

def limit_history(messages: list, max_length: int = 10) -> list:
    return messages[-max_length:]