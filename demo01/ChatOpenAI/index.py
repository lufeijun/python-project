from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 指向本地 Ollama 的 API 端点
chat_model = ChatOpenAI(
    base_url="http://192.168.0.109:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
    model="qwen2:0.5b",  # 你的 Ollama 模型名
    api_key="ollama",  # 任意字符串（Ollama 不需要真实 key）
)

# 调用模型
messages = [HumanMessage(content="你好！")]
response = chat_model.invoke(messages)
print(response.content)