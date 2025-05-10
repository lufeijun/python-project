from langchain_ollama import OllamaLLM , ChatOllama # ollama
from langchain_core.prompts import ChatPromptTemplate # 提示词
from langchain_core.output_parsers import StrOutputParser # 输出解析器



class MyOllamaClient:
    def __init__(self, model_name: str = "deepseek-r1:1.5b", temperature: float = 0.3):
        # 使用本地部署的大模型
        self.llm = OllamaLLM(
            base_url="http://ollama:11434",
            model=model_name
        )
        
        self.chat_model = ChatOllama(
            base_url="http://ollama:11434",
            model=model_name
        )
        
        return
    def say_hello(self):
        prompt = ChatPromptTemplate.from_template("讲一个关于 {topic} 的笑话")
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser
        print( chain.invoke({"topic":"三国"}) )
    
        return    
    