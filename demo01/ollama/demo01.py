from langchain_ollama import OllamaLLM # ollama
from langchain_core.prompts import ChatPromptTemplate # 提示词
from langchain_core.output_parsers import StrOutputParser # 输出解析器



# prompt = ChatPromptTemplate.from_template("《三国演义》{topic}介绍")
prompt = ChatPromptTemplate.from_template("讲一个关于 {topic} 的笑话")

model = OllamaLLM(
    base_url="http://192.168.0.109:11434",
    # model="deepseek-r1:1.5b"
    model="qwen2:0.5b"
)

output_parser = StrOutputParser()

chain = prompt | model | output_parser

print( chain.invoke({"topic":"三国"}) )
