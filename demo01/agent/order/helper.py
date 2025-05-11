from datetime import datetime
from langchain.tools import tool
from typing import Union
from langgraph.graph import END, StateGraph
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import HumanMessage, AIMessage
import operator

@tool
def calculate(expression: str) -> Union[float, int, str]:
    """执行数学计算(加、减、乘、除)，输入应为数学表达式如'3+5'或'10/2'"""
    try:
        # 安全评估数学表达式
        allowed_chars = set("0123456789+-*/. ()")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含非法字符"
        
        result = eval(expression)
        return float(result) if not result.is_integer() else int(result)
    except Exception as e:
        return f"计算错误: {str(e)}"

# 模拟订单数据库
ORDERS_DB = {
    "1001": {"customer": "张三", "items": ["笔记本电脑", "鼠标"], "total": 5999.00, "status": "已发货"},
    "1002": {"customer": "李四", "items": ["手机", "耳机"], "total": 3999.00, "status": "处理中"},
    "1003": {"customer": "王五", "items": ["平板电脑"], "total": 2599.00, "status": "已送达"}
}

@tool
def search_order(order_id: str) -> dict:
    """根据订单ID查询订单信息"""
    order = ORDERS_DB.get(order_id)
    if order:
        return order
    return {"error": f"未找到订单 {order_id}"}

@tool
def current_time(order_id: str) -> dict:
    """获取当前时间"""
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


chat_model = ChatOpenAI(
    base_url="http://ollama:11434/v1",
    model="qwen3:1.7b",
    api_key="ollama",
)

# 定义状态结构
class AgentState(TypedDict):
    input: str
    chat_history: List[Union[HumanMessage, AIMessage]]
    intermediate_steps: Annotated[List[tuple], operator.add]
    agent_outcome: Union[str, None]


# 创建基础Agent
def create_base_agent():
    tools = [calculate, search_order,current_time]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个多功能助手，可以帮助用户进行数学计算、获取当前时间、查询订单信息。
        请严格按照以下规则操作：
        1. 计算时确保表达式安全
        2. 查询订单需要完整的订单ID
        3. 用中文回答"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    agent = create_openai_tools_agent(chat_model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)


# 节点函数
def call_agent(state: AgentState):
    
    agent_executor = create_base_agent()
   
    result = agent_executor.invoke({
        "input": state["input"],
        "chat_history": state["chat_history"]
    })
    
    return {
        "agent_outcome": result["output"], 
        "intermediate_steps": result.get("intermediate_steps", [])
    }

def execute_tools(state: AgentState):
    # 这里简化处理，实际应根据agent_outcome决定执行哪个工具
    # 在完整实现中，需要解析agent_outcome获取工具调用信息
    return {"intermediate_steps": state["intermediate_steps"]}

# 条件判断函数
def should_continue(state: AgentState):
    if state["agent_outcome"] and "需要更多信息" in state["agent_outcome"]:
        return "continue"
    return "end"

# 初始化工作流
def create_workflow():
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("agent", call_agent)
    workflow.add_node("action", execute_tools)
    
    # 设置边
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END
        }
    )
    workflow.add_edge("action", "agent")
    
    return workflow.compile()
