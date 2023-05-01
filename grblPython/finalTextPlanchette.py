#final code that spells GPT responses from text input, only thing that is cooler is voice input
#COORDINATES ARE FOR THE PLANCHETTE ATTACHED, NOT JUST THE MAGNET!!

from chatgpt_wrapper import ChatGPT
import speech_recognition as sr
import pyttsx3

import time
import serial
import string
import re #pip install regex

coords = {
    "A": "G1 X465 Y120 F1300",
    "B": "G1 X424 Y100 F1300",
    "C": "G1 X393 Y87 F1300",
    "D": "G1 X372 Y75 F1300",
    "E": "G1 X333 Y70 F1300",
    "F": "G1 X290 Y65 F1300",
    "G": "G1 X267 Y65 F1300",
    "H": "G1 X220 Y64 F1300",
    "I": "G1 X185 Y64 F1300",
    "J": "G1 X173 Y73 F1300",
    "K": "G1 X130 Y75 F1300",
    "L": "G1 X95 Y92 F1300",
    "M": "G1 X50 Y115 F1300",
    "N": "G1 X490 Y190 F1300",
    "O": "G1 X450 Y170 F1300",
    "P": "G1 X425 Y155 F1300",
    "Q": "G1 X375 Y145 F1300",
    "R": "G1 X344 Y138 F1300",
    "S": "G1 X317 Y132 F1300",
    "T": "G1 X272 Y132 F1300",
    "U": "G1 X260 Y122 F1300",
    "V": "G1 X205 Y129 F1300",
    "W": "G1 X160 Y135 F1300",
    "X": "G1 X125 Y155 F1300",
    "Y": "G1 X95 Y170 F1300",
    "Z": "G1 X55 Y200 F1300"
}


port = "COM4"
ser = serial.Serial(port, 115200, timeout = 1) # open com port of hc-06 receiving, set to 9600 baud
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
    prompt = prompt + ". Respond in 3 words MAXIMIUM and prioritize humor over factual accuracy"
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

import string

def removePunctuation(string):
    # Define a set of all punctuation and symbols to remove
    punctuations = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    
    # Remove all punctuation and symbols
    cleaned_string = ''.join(c for c in string if c not in punctuations and not c.isdigit())
    
    # Concatenate all the characters together and convert to uppercase
    cleaned_string = cleaned_string.replace(' ', '').upper()
    
    return cleaned_string

def cncHome(): #homing function
    funnyString = "$H"
    ogString = "$H"
    funnyString = funnyString.strip() #strip all EOL chars for sending
    funnyString = funnyString + '\n'
    funnyString = bytes(funnyString, encoding='utf8')
    ser.write(funnyString)
    grbl_out = ser.readline().decode().strip()
    print(' Mr. GRBL: ' + grbl_out)

def prepString(string): #prepare a string for sending over serial
    string = removePunctuation(string)
    string.strip()
    string = string +'\n'
    string = bytes(string,encoding='utf8')
    return string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("homing...")
cncHome()

ouijaPrompt() #put chatgpt in Ouija mode
while(1): #wait for user to speak
    prompt = input("prompt: ")
    parsedHeard = prompt.lower()
    print("formatted: ", parsedHeard)
    gptResponse = askGPT(parsedHeard) #set gptResponse to chatGPT's final response
    gptResponse = removePunctuation(gptResponse) #prepare GPT response for formatting
    for char in gptResponse:
       gcode = coords[char] #grab coordinates of char from dict
       og = gcode
       gcode.strip()
       gcode = gcode + '\n'
       gcode = bytes(gcode,encoding='utf8')
       og = gcode #for printing GCODE not bytes so user know where machine going
       ser.write(gcode) #send gcode for character to machine
       #what print("GCODE SENT for: " + char + ": " + og)
       time.sleep(5)