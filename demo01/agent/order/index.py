from order_agent import MultiFunctionAgent

if __name__ == "__main__":
    my_agent = MultiFunctionAgent(session_id="order123")
    
    while True:
        user_input = input("用户: ")
        if user_input.lower() in ["退出", "quit", "exit"]:
            print("助手: 再见！")
            break
        
        response = my_agent.run(user_input)
        print(f"助手: {response}")