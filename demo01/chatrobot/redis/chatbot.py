from ast import List
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory


class RedisChatBot:
    def __init__(
            self,
            redis_url: str = "redis://localhost:6379/0",
            max_history: int = 10,
        ):
        self.redis_url = redis_url
        self.max_history = max_history
            
        # 创建基础链
        prompt = ChatPromptTemplate.from_messages([
            # SystemMessagePromptTemplate.from_template(
            #     "你是一个友好、乐于助人的AI助手。用简洁明了的方式回答用户问题。"
            # ),
            SystemMessage(content="你是一个提供情绪价值的 AI 聊天助手。用简洁明了的方式回答用户问题。"),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        # 大模型初始化
        self.chat_model = ChatOpenAI(
            base_url="http://ollama:11434/v1",
            model="qwen3:1.7b",
            api_key="ollama",
        )
        self.chain = prompt | self.chat_model

        # 创建一个带历史的聊天
        self.conversation = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.get_message_history(session_id),
            input_messages_key="input",
            history_messages_key="history"
        )

    def get_message_history(self, session_id: str) -> RedisChatMessageHistory:
        """获取Redis消息历史"""
        return RedisChatMessageHistory(
            url=self.redis_url,
            session_id=session_id
        )
    def limit_history(self, messages: List) -> List:
        """限制历史记录长度"""
        return messages[-self.max_history:]
    def chat(self, input_text: str, session_id: str) -> str:
        """执行聊天"""
        # 获取并限制历史记录
        history = self.get_message_history(session_id).messages
        history = self.limit_history(history)
        
        # 更新Redis中的历史记录
        self.get_message_history(session_id).clear()
        for msg in history:
            self.get_message_history(session_id).add_message(msg)
        
        # 获取回复
        response = self.conversation.invoke(
            {"input": input_text},
            config={"configurable": {"session_id": session_id}}
        )
        
        return response.content


# def create_chatbot(session_id: str):
#     """创建带Redis记忆的聊天机器人"""
    
#     # 1. 创建基础链
#     prompt = ChatPromptTemplate.from_messages([
#         # SystemMessagePromptTemplate.from_template(
#         #     "你是一个友好、乐于助人的AI助手。用简洁明了的方式回答用户问题。"
#         # ),
#         SystemMessage(content="你是一个提供情绪价值的 AI 聊天助手。用简洁明了的方式回答用户问题。"),
#         MessagesPlaceholder(variable_name="history"),
#         HumanMessagePromptTemplate.from_template("{input}")
#     ])
    
#     # 2. 初始化聊天模型
#     chat_model = ChatOpenAI(
#         base_url="http://ollama:11434/v1",
#         model="qwen3:1.7b",
#         api_key="ollama",
#     )
    
#     # 3. 定义链
#     chain = prompt | chat_model
    
#     # 4. 创建带历史记录的链
#     conversation = RunnableWithMessageHistory(
#         chain,
#         get_redis_history,
#         input_messages_key="input",
#         history_messages_key="history"
#     )
    
#     # 1. 获取Redis聊天历史
#     redis_history = get_redis_history(session_id)
    
#     # 2. 创建带限制的记忆系统
#     memory = LimitedRedisChatMemory(
#         max_history=10,
#         chat_memory=redis_history,
#         memory_key="history",
#         return_messages=True
#     )
    
#     # 5. 创建对话链
#     conversation = RunnableWithMessageHistory(
#         llm=chat_model,
#         memory=memory,
#         prompt=prompt,
#         verbose=False  # 设为True可查看详细交互过程
#     )
    
#     return conversation