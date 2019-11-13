#!/usr/bin/python

import spidev
import time
import os
import RPi.GPIO as GPIO     # Import the RPi Library for GPIO pin control

GPIO.setmode(GPIO.BOARD)    # the physical pin number scheme

# Open SPI bus

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=10000000

# GPIO pin numbers and pot channel
servcBtn=16         # starting/stop the service
resetBtn=18         # resetting values
modeBtn = 7
rLed = 13           # RED LED
gLed = 11           # Green LED
pot_channel = 2     # Define pot channel

startTime = time.time() # global start time

# Setting up the pins
GPIO.setup(resetBtn, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(servcBtn, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(modeBtn, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(rLed,GPIO.OUT)   # LED output pin
GPIO.setup(gLed,GPIO.OUT)   # LED output pin

flag = False                  # useful flag
flagMode = None
delay = 1                   # default sampling rate at 1 second

# combination code
secureCombocode = "R100L200R200L400"  # right 100ms, left 100ms, right 100ms, left 100ms
unsecureCombocode = "100200200400"
log = []                        # log of user input
dir = []                        # direction user input

# Function to read SPI data from MCP3008 chip
def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# Function to flash LED
def flshRed():
    for i in range(5):
        GPIO.output(rLed, GPIO.HIGH)
        time.sleep(.75)
        GPIO.output(rLed, GPIO.LOW)

def flshGreen():
    for i in range(5):
        GPIO.output(gLed, GPIO.HIGH)
        time.sleep(.75)
        GPIO.output(gLed, GPIO.LOW)

# Function Range to check range of values from pot and add direction symbols
def rangePot(val):
    if val >= 0 and val <= 550:
        return 0
    
    else:
        return 1

# Functiion to check the range of duration
def checkRange(curr_val, prev_val):
    now = time.time()
    if (now-startTime) >=0 and (now-startTime)<=1:
        return 100
    elif (now-startTime)>1 and (now-startTime)<=2:
        return 200
    elif (now-startTime)>2 and (now-startTime)<=3:
        return 300
    elif (now-startTime)>3 and (now-startTime)<=4:
        return 400
    elif (now-startTime)>4 and (now-startTime)<=5:
        return 500
    elif (now-startTime)>5 and (now-startTime)<=6:
        return 600
    elif (now-startTime)>6 and (now-startTime)<=7:
        return 700
    else:
        return 800



# Function converting dialed sequence
def convertSequence():
    global log
    global dir
    s = ""
    for i in range (len(log)):
        if dir[i] == 0:
            s += "L" + str(log[i])
        else:
            s += "R" + str(log[i])
    return s

def unsecureConvertSeq():
    global log
    s = ""
    for i in range (len(log)):
        s += str(log[i])

    return s


# Function to get data from the C_line (knob)
#def C_line()


# function to compare if two arrays have the same elements
def match(a,b):
    # set(a).intersection(b) performs faster comparison
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] == b[i]:
                return 1 # 1 for true
            else:
                return 0 # 0 for false

# function for L-Line output
#def L_line():
    
# function for reset
def setMode(channel):
    global flagMode
    if flagMode == None:
        flagMode = True
        
    elif flagMode == True:
        flagMode = False
        
    else:
        flagMode = True
        

def serviceCallback(channel):
    global flag
    global log
    global dir
    
    if flag == False:
        flag = True
    
    else:
        # reset the log and the dir arrays
        log = []
        dir = []
        clearing = os.system("clear") # command for cleaning the console, sets clearing = 0
        
        
def secureMode():
    global log
    global prev_val
    global val_count
    global count
    global startTime
    global flagMode
    
    
    while True:
        curr_val = ReadChannel(pot_channel)
        #print(curr_val)     # debug statement, delete later
        time.sleep(1)
    
        if (curr_val == prev_val) or (curr_val - prev_val) <= 5:
            print("symbol")
            count = count + 1 # increment the count of symbols
            print("count == ",count)
            val_count.append(curr_val)
            print("unfiddled time = ",time.time()-startTime)
            dur = checkRange(curr_val, prev_val)
            print("Duration = " ,dur)
            log.append(dur)
            direct = rangePot(curr_val)
            print("Direction = ",direct," #0-Left, 1-right")
            dir.append(direct)
            startTime = time.time()

            if count == 4:  # for this code, this ensures we check the code after recording 4 symbols
                print("======================")
                print("checking entered code.")
                print("======================")
            
                in_code = convertSequence()
                print(in_code) #to see how it converts it
                check = match(secureCombocode, in_code)
            
                if check == 1:
                    print("======================")
                    print("entered code succesfully")
                    flshGreen()
                
                else:
                    print("======================")
                    print("entered code unsuccesfully")
                    flshRed()
                    count = 0
                    break
            else:
                prev_val = curr_val
                
            
def unsecureMode():
    global log
    global prev_val
    global val_count
    global count
    global startTime
    global flagMode
    
    
    while True:
        curr_val = ReadChannel(pot_channel)
        #print(curr_val)     # debug statement, delete later
        time.sleep(1)
        
        if (curr_val == prev_val) or (curr_val - prev_val) <= 5:
            print("symbol")
            count = count + 1 # increment the count of symbols
            print("count == ",count)
            val_count.append(curr_val)
            print("unfiddled time = ",time.time()-startTime)
            dur = checkRange(curr_val, prev_val)
            print("Duration = " ,dur)
            log.append(dur)
            startTime = time.time()

            if count == 4:  # for this code, this ensures we check the code after recording 4 symbols
                print("======================")
                print("checking entered code.")
                print("======================")
            
                log.sort()
                in_code = unsecureConvertSeq()
                print(in_code) #to see how it converts it
                check = match(unsecureCombocode, in_code)
            
                if check == 1:
                    print("======================")
                    print("entered code succesfully")
                    flshGreen()
            
                else:
                    print("======================")
                    print("entered code unsuccesfully")
                    flshRed()
                    count = 0
                    break
            
            else:
                prev_val = curr_val

GPIO.add_event_detect(servcBtn, GPIO.FALLING, callback=serviceCallback, bouncetime=200) 
GPIO.add_event_detect(modeBtn, GPIO.FALLING, callback=setMode, bouncetime=200)


count = 0
val_count = []
prev_val = 0
try:
    while True:
        if flagMode:
            print("Press Service Button !")
            if flag:
                # secure mode
                print("Secure Mode")
                secureMode()
                flagMode = None
                flag = False
                
        elif flagMode == None:
            #print("Floating nje")
            continue
        
        else:
            # unsecure mode
            print("Unsecure Mode")
            unsecureMode()
            flagMode = None
        
            
except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()

GPIO.cleanup()      # on normal exit