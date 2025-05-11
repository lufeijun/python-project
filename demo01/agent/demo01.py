from langchain_openai import ChatOpenAI 
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from openai import api_key

# 官网的 dmeo
memory = MemorySaver()

model = ChatOpenAI(
            base_url="http://ollama:11434/v1",
            model="qwen3:1.7b",
            api_key="ollama",
        )

search = TavilySearchResults(
        max_results=2,
        tavily_api_key=""
    )
tools = [search]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# 使用 agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="你好，我是赵四，生活在黑龙江")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="今天的天气怎么样?")]}, config
):
    print(chunk)
    print("----")