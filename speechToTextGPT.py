from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer() #initialize speech recognition object
bot = ChatGPT() #initialize ChatGPT object that will retrieve answers
vosk = False #adjust based on which recognizer is being used


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def askGPT(prompt): #pass prompt to ChatGPT and print response
    response = bot.ask(prompt)
    split_response = response.split(':') #take big response with both replies and divide by colons
    finalResponse = split_response[2].strip() #take all information after the second colon as final response
    print(finalResponse) #print final response to console
    SpeakText(finalResponse) #DEBUG: speak final repsonse, this is placeholder for spelling on the board

def ouijaPrompt(): #pass Ouija jailbreak prompt to ChatGPT instance
  with open('ouijaPrompt.txt', 'r', encoding="utf8") as file:
    jailbreakPrompt = file.read().rstrip('\n') #store big character prompt in string
  response = bot.ask(jailbreakPrompt) #initialize "Ouija Mode" in ChatGPT by removing OpenAI restrictions
  print(response) #verify that Ouija Mode has successfully been activated with print to console
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ouijaPrompt()
while(1): #wait for user to speak

    try:

        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration = 0.2)
            audio2 = r.listen(source2)
            vtt = r.recognize_google(audio2) #can switch vosk to google, but only 50 calls/day
            vtt = vtt.lower()
            
            if vosk:
                parsedHeard = vtt.split('"')[3] #remove additional formatting when vosk recognition is used
            else:
                parsedHeard = vtt

            print("Unformatted: ", vtt)
            print("Formatted: ", parsedHeard) #print prompt that will be passed to ChatGPT


            askGPT(parsedHeard) 

    except sr.RequestError as e:
        print ("could not request resulst; [0]".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")