from text2sql_agent import Text2SQLAgent

from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import Tool


if __name__ == "__main__":
    # 初始化agent
    agent = Text2SQLAgent()
    
    print("Text2SQL Agent 已启动(输入'quit'退出)")
    print("示例问题:")
    print("- 查询销售部所有员工姓名和工资")
    print("- 统计每个部门的平均工资")
    print("- 查找工资最高的10名员工\n")
    
    chat_history = []
    
    while True:
        user_input = input("\n请输入您的问题: ").encode('utf-8').decode('utf-8').strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input:
            continue
            
        # 生成SQL
        sql = agent.generate_sql(user_input, chat_history)
        
        # 更新对话历史
        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=sql)
        ])
        
        print("\n生成的SQL语句:")
        print(sql)