
from openai_client import MyOpenaiClient
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.config import RunnableConfig


# model 客户端
# client = MyOpenaiClient(model_name="qwen3:1.7b").chat_model
client = MyOpenaiClient(model_name="llama3.2:1b").chat_model
store = {}




def demo01():
    
    msg = client.invoke(
        [
            SystemMessage(content="关闭思考模式，no think"),
            # SystemMessage(content="你是一个聊天机器人，叫小蜜一号，能为人提供情绪价值"),
            # HumanMessage(content="你好，我叫赵四"),
            # AIMessage(content="你好赵四，请问有什么我可以帮助你的吗？"),
            # HumanMessage(content="我是谁"),
            HumanMessage(content="你好，我叫王武"),
            AIMessage(content="我能帮你做什么呢"),
            HumanMessage(content="我的名字叫啥"),
        ]
    )
    print(msg)
    return

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def demo02():
    # 在内存中保存聊天消息
    with_message_history = RunnableWithMessageHistory(client, get_session_history)
    
    config = RunnableConfig(
        metadata={"configurable": {"session_id": "1234"}}
    )
    
    response = with_message_history.invoke(
        [HumanMessage(content="你好，我叫王武，很高兴认识你")],
        config=config,
    )
    print(response)
    
    print("==================================")
    
    response = with_message_history.invoke(
        [HumanMessage(content="我叫什么名字")],
        config=config,
    )
    print(response)
    
    
    return










demo02()