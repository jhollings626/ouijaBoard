#final code that spells GPT responses from text input, only thing that is cooler is voice input
#WON'T WORK UNTIL ALL LETTERS HAVE COORDINATES!!!!!

from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
import pyttsx3

import time
import serial
import string
import re #pip install regex

coords = {
  "C": "G1 X300 Y0 F1000",
  "O": "G1 X150 Y50 F1000",
  "K": "G1 X500 Y200 F1000"
}


port = "COM4"
ser = serial.Serial(port, 115200, timeout = 1) #open com port of hc-06 receiving, set to 9600 baud
print("serial opened")
unicode = "\r\n\r\n"
unicode = unicode.encode()
ser.write(unicode)
time.sleep(5)
ser.flushInput()
r = sr.Recognizer() #initialize speech recognition object
bot = ChatGPT() #initialize ChatGPT object that will retrieve answers
vosk = True #adjust based on which recognizer is being used


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def askGPT(prompt): #pass prompt to ChatGPT and print response
    prompt = prompt + ". 3 words MAXIMIUM and prioritize humor"
    #print("Asked: ", prompt)
    response = bot.ask(prompt)
    split_response = response.split(':') #take big response with both replies and divide by colons
    finalResponse = split_response[2].strip() #take all information after the second colon as final response
    print("OuijaGPT: ", finalResponse) #print final response to console
    return finalResponse
    #SpeakText(finalResponse) #DEBUG: speak final repsonse, this is placeholder for spelling on the board

def ouijaPrompt(): #pass Ouija jailbreak prompt to ChatGPT instance
  with open('ouijaPrompt.txt', 'r', encoding="utf8") as file:
    jailbreakPrompt = file.read().rstrip('\n') #store big character prompt in string
  response = bot.ask(jailbreakPrompt) #initialize "Ouija Mode" in ChatGPT by removing OpenAI restrictions
  #print(response) #verify that Ouija Mode has successfully been activated with print to console
  print("Ouija mode activated. Ready for questions...")

  def prepString(string): #prepare for sending over serial
    string = removePunctuation(string)
    string.strip()
    string = string +'\n'
    string = bytes(string,encoding='utf8')
    return string

def removePunctuation(string):
    string = string.translate(str.maketrans("", "", string.punctuation))
    string = string.upper()
    string = "".join(string.split())
    return string

def cncHome(): #homing function
    funnyString = "$H"
    ogString = "$H"
    funnyString = funnyString.strip() #strip all EOL chars for sending
    funnyString = funnyString + '\n'
    funnyString = bytes(funnyString, encoding='utf8')
    ser.write(funnyString)
    grbl_out = ser.readline().decode().strip()
    print(' Mr. GRBL: ' + grbl_out)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("homing...")
cncHome()



ouijaPrompt()
while(1): #wait for user to speak
    prompt = input("prompt: ")
    parsedHeard = prompt.lower()
    print("formatted: ", parsedHeard)
    gptResponse = askGPT(parsedHeard) #set gptResponse to chatGPT's final response
    gptResponse = removePunctuation(gptResponse) #prepare GPT response for formatting
    for char in gptResponse:
       gcode = coords[char] #grab coordinates of char from dict
       og = gcode #for printing GCODE not bytes so user know where machine going
       gcode = prepString(gcode)
       ser.write(gcode) #send gcode for character to machine
       print("GCODE SENT for: " + char + ": " + og)