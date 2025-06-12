from os import name

from pydantic import BaseModel, Field
from demo.client.openai_client import OpenaiClient
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser,PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException


def demo01():
    
    # 1、初始化聊天客户端
    # client = MyOpenaiClient(model_name="qwen3:1.7b").chat_model
    client = OpenaiClient().chat_model

    # 2、处理消息
    message = [
        SystemMessage(content="你是一个会讲笑话的助手，为用户提供正能量、高情绪价值的笑话，注意：直接回答问题，不要解释思考过程。只需给出最终答案。"),
        HumanMessage(content="给我讲一个笑话"),
    ]

    # 3、格式化输出
    parse = StrOutputParser()

    # 输出结果 这个结果包含 content(返回内容) 和 一些统计信息
    # result = client.invoke(message)
    # 4、链式调用
    chain = client | parse
    result = chain.invoke(message)

    print(result)
    return


# 流式输出
def demo02() :

    # client = OpenaiClient(model_name="llama3.2:1b").chat_model
    client = OpenaiClient().chat_model

    # 2、处理消息
    message = [
        SystemMessage(content="你是一个会讲笑话的助手，为用户提供正能量、高情绪价值的笑话，注意：直接回答问题，不要解释思考过程。只需给出最终答案。"),
        HumanMessage(content="给我讲一个笑话"),
    ]

    # 没有链
    # for chunk in client.stream("讲个笑话"):
    #     print(chunk.content, end="", flush=True)

    parse = StrOutputParser()
    chain = client | parse
    for chunk in chain.stream(message):
        print(chunk, end="", flush=True)

    return


# 将结果转唯 json，使用 JsonOutputParser
def response_json_one() :
    # 定义输出 JSON 的结构描述（告诉模型需要生成什么格式）
    json_schema = '''{
        "title": "Person",
        "description": "Identifying information about a person.",
        "type": "object",
        "properties": {
            "姓名": {"type": "string", "description": "The person's name"},
            "age": {"type": "integer", "description": "The person's age"},
            "hobbies": {
                "type": "array",
                "items": {"type": "string"},
                "description": "The person's hobbies"
            }
        },
        "required": ["姓名", "age"]
    }
    '''
    
    # 创建 JSON 解析器
    # parser = JsonOutputParser()
    parser = JsonOutputParser(pydantic_object=None, name=json_schema)

    # 构造提示词模板（注意包含指令和格式占位符）
    prompt = PromptTemplate(
        template="Answer the question as a valid JSON.\n{format_instructions}\nQuestion: {question}",
        input_variables=["question"],
        partial_variables={"format_instructions": parser.get_format_instructions()} # 注入 json 的格式
    )
    

    # 初始化模型链
    client = OpenaiClient(model_name="llama3.2:1b").chat_model
    # client = OpenaiClient(model_name="deepseek-r1:1.5b").chat_model # 如果模型开启了深度思考模式，那么返回的就不是完整的 json 字符串了，还有 think 部分

    chain = prompt | client | parser

    # 调用并获取 JSON 结果
    try:
        # result = chain.invoke({"question": "Tell me about a 25-year-old named John who loves hiking and coding"})
        result = chain.invoke({"question": "告诉我一个名叫张三的 25 岁年轻人的故事，他喜欢徒步旅行和编程"})
        print(result)
    except OutputParserException:
        print("模型返回了非 JSON 格式")
    
    return

# 将结果转唯 json，使用 PydanticOutputParser
def response_json_two():
    # 定义数据模型
    class Person(BaseModel):
        name: str = Field(description="人的姓名")
        age: int = Field(description="人的年龄")
        hobbies: list[str] = Field(description="爱好列表")

    
    
    prompt = PromptTemplate.from_template("""
    请提供关于{person}的信息，返回实际的JSON数据，不要返回schema定义。
    
    示例格式:
    {{
        "name": "姓名",
        "age": 年龄,
        "hobbies": ["爱好1", "爱好2"]
    }}
    
    要求格式:
    {format_instructions}
    
    请直接返回数据:
    """)
    
    
    # 使用 Pydantic 解析器
    pydantic_parser = PydanticOutputParser(pydantic_object=Person)
    client = OpenaiClient(model_name="llama3.2:1b").chat_model
    chain = prompt | client | pydantic_parser  # 自动验证字段类型    
    

    # 6. 调用链
    try:
        result = chain.invoke({
            "person": "告诉我一个名叫张三的 25 岁年轻人的故事，他喜欢徒步旅行和编程",
            "format_instructions": pydantic_parser.get_format_instructions()  # 自动注入 JSON 格式要求
        })
        print(result) 
    except OutputParserException as e:
        print(f"解析失败: {e}")
        
    return