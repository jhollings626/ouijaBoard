#basic spelling of words using a limited number of hardcoded coordinates, meant for testing without Ouija top of machine

import time
import serial
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

def prepString(string): #prepare for sending over serial
    string.strip()
    string = string +'\n'
    string = bytes(string,encoding='utf8')
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

print("homing...")
cncHome() #home CNC on startup


while(True):
    funnyString = input("WORD TO SPELL: ")
    for char in funnyString:
        gcode = coords[char] #grab coordinates of char from dict
        og = gcode #for printing not bytes
        gcode = prepString(gcode)
        ser.write(gcode) #send gcode for character to machine
        print("GCODE SENT: " + og)
