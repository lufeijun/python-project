from demo.client.openai_client import OpenaiClient
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser


# 聊天历史




client = OpenaiClient(model_name="qwen3:1.7b").chat_model



def demo01():
    
    client.invoke([HumanMessage(content="Hi! I'm Bob")])

    
    message = [
        # SystemMessage(content="你是一个会讲笑话的助手，为用户提供正能量、高情绪价值的笑话，注意：直接回答问题，不要解释思考过程。只需给出最终答案。"),
        HumanMessage(content="中国的首都是哪里"),
        AIMessage(content="中国的首都首都是北京。根据地理位置和城市面积排名，北京是中国东非边疆地区最大城市，拥有全国的现代化程度以及商业中心优势。尽管其他地区如上海、广州等也是大城市，但北京是全国最大的城市之一，因此首都通常是“第一大城市”的简称。"),
        HumanMessage(content="我之前的问题是什么"),
    ]


    print("======message==========")
    print(message)

    parse = StrOutputParser()
    chain = client | parse

    result = chain.invoke(message)
    print("======result==========")
    print( result )
    
    return
