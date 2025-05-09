from text2sql_agent import Text2SQLAgent


agent = Text2SQLAgent()
sql = agent.generate_sql("查询员工信息", [])

print(sql)
