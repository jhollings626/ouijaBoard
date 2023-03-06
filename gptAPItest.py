import openai
import os

openai.api_key="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"
messages = []
system_message = input("What type of chatbot you want me to be?")
messages.append({"role":"system","content":system_message})

print("Alright! I am ready to be your friendly chatbot" + "\n" + "You can now type your messages.")
message = input("")
messages.append({"role":"user","content": message})

response=openai.Completion.create(
  model="gpt-3.5-turbo",
  messages=message
)

reply = response["choices"][0]["message"]["content"]
print(reply)