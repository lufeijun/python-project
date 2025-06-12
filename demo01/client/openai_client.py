import string
from langchain_openai import ChatOpenAI , OpenAI
from langchain_core.messages import HumanMessage
from pydantic import SecretStr

class MyOpenaiClient:
    def __init__(self, model_name: str = "deepseek-r1:1.5b", temperature: float = 0.3):
        # 使用本地部署的大模型
        self.chat_model = ChatOpenAI(
            base_url="http://ollama:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
            model=model_name,  # 你的 Ollama 模型名
            api_key=SecretStr("sk-ollama"),  # 任意字符串（Ollama 不需要真实 key） ，注意：不能传汉字
        )
        
        self.llm = OpenAI(
            base_url="http://ollama:11434/v1",  # Ollama 的兼容 OpenAI 的 API 地址
            model=model_name,  # 你的 Ollama 模型名
            api_key=SecretStr("sk-ollama"),  # 任意字符串（Ollama 不需要真实 key） ，注意：不能传汉字
        )
        return
    
    def say_hello(self):
        # 调用模型
        messages = [HumanMessage(content="你好！")]
        response = self.chat_model.invoke(messages)
        print(response.content)
        return
    def stream_demo(self): # 同步的 stream
        chucks = []
        for chuck in self.chat_model.stream("西游释厄传"): 
            chucks.append(chuck)
            # content='内容' additional_kwargs={} response_metadata={} id='run--3aa93e48-fc2c-4831-9909-03a4c514fc3a'
            # print(chuck)
            print( chuck.content, end="==" , flush=True )
        return
    async def stream_demo_asc(self,input:str = "西游释厄传"): # 异步的 stream ，需要 asyncio.run(client.stream_demo_asc()) 调用
        chucks = []
        async for chuck in self.chat_model.astream(input): 
            chucks.append(chuck)
            # content='内容' additional_kwargs={} response_metadata={} id='run--3aa93e48-fc2c-4831-9909-03a4c514fc3a'
            # print(chuck)
            print( chuck.content, end="" , flush=True )
        return