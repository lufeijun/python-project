from chatbot import RedisChatBot

# 初始化聊天机器人
session_id = "user123"  # 可以使用用户ID或会话ID
bot = RedisChatBot(max_history=10)


# 模拟对话
while True:
    user_input = input("你: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("AI: 再见！")
        break
    
    # 获取AI回复
    response = bot.chat(input_text=user_input,session_id=session_id)
    print(f"AI: {response}")