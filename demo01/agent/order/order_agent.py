from langchain_community.chat_message_histories import RedisChatMessageHistory
from helper import (
    create_workflow
)


class MultiFunctionAgent:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.message_history = RedisChatMessageHistory(
            url="redis://:123456@localhost:6379/0",
            session_id=session_id,
            ttl=1200
        )
        self.workflow = create_workflow()
    
    def run(self, user_input: str) -> str:
        try:
            # 初始化状态
            initial_state = {
                "input": user_input,
                "chat_history": self.message_history.messages,
                "intermediate_steps": [],
                "agent_outcome": None
            }
            
            # 执行工作流
            result = self.workflow.invoke(initial_state)
            
            # 保存对话历史
            self.message_history.add_user_message(user_input)
            self.message_history.add_ai_message(result["agent_outcome"])
            
            return result["agent_outcome"]
        except Exception as e:
            raise e
            # return f"发生错误: {str(e)}"