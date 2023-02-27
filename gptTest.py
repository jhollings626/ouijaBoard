from chatgpt_wrapper import ChatGPT
bot = ChatGPT()

while True:
    prompt = input("prompt: ")
    response = bot.ask(prompt)
    print("")
    print("bot: " + response)
    print("")