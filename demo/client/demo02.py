from demo.client.openai_client import OpenaiClient
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,HumanMessagePromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate



# 提示词模版
# 1、字符串提示词模板 PromptTemplate
# 2、聊天提示词模板 ChatPromptTemplate
# 3、少量示例 FewShotPromptTemplate

client = OpenaiClient().chat_model


# 1、字符串提示词模板
def demo01():
    
    # 创建模板
    template = "请用简洁的语言解释{concept}，就像给{audience}讲解一样。"
    prompt = PromptTemplate(
        input_variables=["concept", "audience"],
        template=template
    )

    # 使用模板
    filled_prompt = prompt.format(concept="量子计算", audience="")
    print("=========提示词============")
    print(filled_prompt)
    
    
    result = client.invoke( prompt.invoke({"concept":"量子计算","audience":"小学生"}) )
    print("=========结果============")
    print( result )
        
    return

# 2、聊天提示词模板 
def demo02():
    
    # 创建聊天模板
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一位专业的{role}。请用{style}风格回答。"),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    # 使用模板
    messages = chat_template.format_messages(
        role="物理学家",
        style="幽默风趣",
        question="什么是相对论？"
    )
    
    # 使用模板
    print("=========提示词============")
    print(messages)
    
    
    result = client.invoke( messages )
    print("=========结果============")
    print( result )
    
    return


# 3、少量示例
def demo03():

    examples = [
        {"word": "开心", "antonym": "难过"},
        {"word": "高", "antonym": "矮"}
    ]

    # 单个示例的模板
    example_prompt = PromptTemplate(
        template="词语: {word}\n反义词: {antonym}",
        input_variables=["word", "antonym"],
    )

    # 创建FewShot模板
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples, # 示例
        example_prompt=example_prompt,
        prefix="给出以下词语的反义词",
        suffix="词语: {input}\n反义词:",
        input_variables=["input"]
    )

    # 使用
    messages = few_shot_prompt.format(input="快")
    
    # 使用模板
    print("=========提示词============")
    print(messages)
    
    
    result = client.invoke( messages )
    print("=========结果============")
    print( result )
    
    
    return