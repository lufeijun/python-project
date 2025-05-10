import asyncio
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(
            base_url="http://ollama:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
            model="deepseek-r1:1.5b",  # 你的 Ollama 模型名
            api_key="ollama",  # 任意字符串（Ollama 不需要真实 key） ，注意：不能传汉字
            streaming=True,
        )

async def async_stream(input):
    async for chunk in chat.astream(input):
        print(chunk.content, end="", flush=True)

asyncio.run(async_stream("西游释厄传"))
asyncio.run(async_stream("你好"))


for i in range(1, 101):
    print(i)
