from ollama_client import MyOllamaClient
from openai_client import MyOpenaiClient
import asyncio

# client = MyOllamaClient()
# client.say_hello()

client = MyOpenaiClient()
# client.say_hello()

# 异步流式
asyncio.run(client.stream_demo_asc("你好"))
asyncio.run(client.stream_demo_asc("西游释厄传"))