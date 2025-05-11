
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from openai_client import MyOpenaiClient


# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = ""

# demo01
def demo01():
    
    # 1、初始化聊天客户端
    # client = MyOpenaiClient(model_name="qwen3:1.7b").chat_model
    client = MyOpenaiClient().chat_model

    # 2、处理消息
    message = [
        SystemMessage(content="讲一下语句从中文翻译为英语，不需要思考"),
        HumanMessage(content="你好，欢迎来到张家界"),
    ]

    # 3、格式化输出
    parse = StrOutputParser()


    # 4、链式调用
    # result = client.chat_model.invoke(message)
    chain = client | parse
    result = chain.invoke(message)

    print(result)
    return

# demo02=带模版
def demo02():

    # 1、初始化聊天客户端
    client = MyOpenaiClient().chat_model

    # 2、模版消息
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "将一下语句翻译为{language}"), 
            ("user", "{text}")
        ]
    )
    
    print("模版信息")
    print(prompt_template.invoke({"language": "英语", "text": "你好，欢迎来到张家界。"}))

    # 3、格式化输出
    parse = StrOutputParser()


    # 4、链式调用
    # result = client.chat_model.invoke(message)
    chain = prompt_template | client | parse
    result = chain.invoke({"language":"英语","text":"今天我为你介绍了在线计算广告的另外一个高级话题：受众扩展。"})

    print(result)
    return


demo02()
