#basic spelling of words using a limited number of hardcoded coordinates, meant for testing without Ouija top of machine

import time
import serial
import string
import re #pip install regex

coords = {
    "A": "G1 X490 Y130 F1300",
    "B": "G1 X440 Y120 F1300",
    "C": "G1 X410 Y96 F1300",
    "D": "G1 X375 Y88 F1300",
    "E": "G1 X340 Y80 F1300",
    "F": "G1 X305 Y76 F1300",
    "G": "G1 X275 Y72 F1300",
    "H": "G1 X236 Y74 F1300",
    "I": "G1 X205 Y74 F1300",
    "J": "G1 X170 Y79 F1300",
    "K": "G1 X140 Y88 F1300",
    "L": "G1 X110 Y96 F1300",
    "M": "G1 X59 Y123 F1300",
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
ser = serial.Serial(port, 115200, timeout = 1) #open com port of hc-06 receiving, set to 9600 baud
print("serial opened")
unicode = "\r\n\r\n"
unicode = unicode.encode()
ser.write(unicode)
time.sleep(5)
ser.flushInput()

def prepString(string): #prepare for sending over serial
    #string = removePunctuation(string)
    string.strip()
    string = string +'\n'
    string = bytes(string,encoding='utf8')
    return string

#def removePunctuation(string):
 #   string = string.translate(str.maketrans("", "", string.punctuation))
  #  string = string.upper()
   # string = "".join(string.split())
    #return string

def cncHome(): #homing function
    funnyString = "$H"
    ogString = "$H"
    funnyString = funnyString.strip() #strip all EOL chars for sending
    funnyString = funnyString + '\n'
    funnyString = bytes(funnyString, encoding='utf8')
    ser.write(funnyString)
    grbl_out = ser.readline().decode().strip()
    print(' Mr. GRBL: ' + grbl_out)

print("homing...")
cncHome() #home CNC on startup


while(True):
    funnyString = input("WORD TO SPELL: ")
    #funnyString = removePunctuation(funnyString)
    for char in funnyString:
        gcode = coords[char] #grab coordinates of char from dict
        og = gcode #for printing GCODE not bytes so user know where machine going
        gcode = prepString(gcode)
        ser.write(gcode) #send gcode for character to machine
        print("GCODE SENT for: " + char + ": " + og)
