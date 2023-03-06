#basic sending of homing function via Python for testing serial communication
import time
import serial
import re #pip install regex

port = "COM4"

ser = serial.Serial(port, 115200, timeout = 1) #open com port of hc-06 receiving, set to 9600 baud
print("serial opened")
unicode = "\r\n\r\n"
unicode = unicode.encode()
ser.write(unicode)
time.sleep(2)
ser.flushInput()

funnyString = "$H"
ogString = "$H"
funnyString = funnyString.strip() #strip all EOL chars for sending
funnyString = funnyString + '\n'
funnyString = bytes(funnyString, encoding='utf8')
while(True):
    question = input("send coordinate? Y/N")
    if question  == "Y":
        print("sending: " + ogString)
        ser.write(funnyString)
        grbl_out = ser.readline().decode().strip()
        print(' Mr. GRBL: ' + grbl_out)


