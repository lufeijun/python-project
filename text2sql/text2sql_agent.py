from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, List
from langchain.tools import tool
from langchain_openai import ChatOpenAI


import json

from langchain_ollama import OllamaLLM


class DatabaseSchemaLoader:
    # 构造函数
    def __init__(self, schema_file: str):
        self.schema_file = schema_file
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict:
        with open(self.schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_schema_description(self) -> str:
        """获取格式化的数据库schema描述"""
        desc = f"数据库名称: {self.schema['database_name']}\n\n"
        
        # 表结构
        desc += "表结构:\n"
        for table in self.schema['tables']:
            desc += f"- {table['table_name']}: {table['description']}\n"
            for col in table['columns']:
                desc += f"  - {col['name']} ({col['type']}): {col['description']}\n"
        
        # 表关系
        if 'relationships' in self.schema:
            desc += "\n表关系:\n"
            for rel in self.schema['relationships']:
                desc += f"- {rel['table1']} ↔ {rel['table2']}: {rel['join_condition']}\n"
        
        return desc

# 初始化schema加载器
schema_loader = DatabaseSchemaLoader("./data/schema.json")

@tool
def get_database_schema() -> str:
    """返回数据库的结构信息，包括表、字段和关系"""
    return schema_loader.get_schema_description()

class Text2SQLAgent:
    def __init__(self, model_name: str = "qwen3:1.7b", temperature: float = 0.3):
        # 使用本地部署的大模型
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            base_url="http://192.168.0.109:11434/v1",  # 假设本地部署的API
            temperature=temperature,
            api_key="sk-oooxxx",
        )
        
        # 定义工具
        self.tools = [get_database_schema]
        
        # 系统提示词
        self.system_prompt = """你是一个专业的SQL专家，能够根据用户问题和数据库结构生成正确的SQL查询。
        
请遵循以下规则:
1. 首先生成SQL前，先查看数据库结构
2. 确保SQL语法正确
3. 使用合适的表连接
4. 只返回SQL语句，不要包含解释"""
        
        # 构建agent
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def generate_sql(self, user_query: str, chat_history: List = None) -> str:
        """生成SQL查询"""
        if chat_history is None:
            chat_history = []
        
        result = self.agent.invoke({
            "input": user_query,
            "chat_history": chat_history
        })
        
        return result["output"]
