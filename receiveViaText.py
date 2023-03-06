from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer() #initialize speech recognition object
bot = ChatGPT() #initialize ChatGPT object that will retrieve answers
vosk = True #adjust based on which recognizer is being used


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def askGPT(prompt): #pass prompt to ChatGPT and print response
    prompt = prompt + ". 10 words maximum and maximize humor"
    #print("Asked: ", prompt)
    response = bot.ask(prompt)
    split_response = response.split(':') #take big response with both replies and divide by colons
    finalResponse = split_response[2].strip() #take all information after the second colon as final response
    print("OuijaGPT: ", finalResponse) #print final response to console
    SpeakText(finalResponse) #DEBUG: speak final repsonse, this is placeholder for spelling on the board

def ouijaPrompt(): #pass Ouija jailbreak prompt to ChatGPT instance
  with open('ouijaPrompt.txt', 'r', encoding="utf8") as file:
    jailbreakPrompt = file.read().rstrip('\n') #store big character prompt in string
  response = bot.ask(jailbreakPrompt) #initialize "Ouija Mode" in ChatGPT by removing OpenAI restrictions
  #print(response) #verify that Ouija Mode has successfully been activated with print to console
  print("Ouija mode activated. Ready for questions...")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ouijaPrompt()
while(1): #wait for user to speak
    prompt = input("prompt: ")
    parsedHeard = prompt.lower()
    print("formatted: ", parsedHeard)
    askGPT(parsedHeard) 