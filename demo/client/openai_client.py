from langchain_openai import ChatOpenAI, OpenAI
from pydantic import SecretStr
from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy import false


class OpenaiClient:
    def __init__(self, model_name: str = "deepseek-r1:1.5b", temperature: float = 0.3):
        # 使用本地部署的大模型
        
        # 聊天模型
        self.chat_model = ChatOpenAI(
            base_url="http://ollama:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
            model=model_name,  # 你的 Ollama 模型名
            api_key=SecretStr("sk-ollama"),  # 任意字符串（Ollama 不需要真实 key） ，注意：不能传汉字
            verbose=False,
        )
        
        self.llm = OpenAI(
            base_url="http://ollama:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
            model=model_name,  # 你的 Ollama 模型名
            api_key=SecretStr("sk-ollama"),  # 任意字符串（Ollama 不需要真实 key） ，注意：不能传汉字
            verbose=False,
        )
        return
    
    def say_hello(self):
        # 调用模型
        messages = [HumanMessage(content="你好！")]
        response = self.chat_model.invoke(messages)
        print(response.content)
        return