import RPi.GPIO as GPIO
import time
import os
    
#python backend
    
#CONSTANTS
print("Initializing...")
PIRSensePin = 4
LED1Pin = 17
LED2Pin = 22
ButtonPin = 26
LOG_FILE_NAME = "/home/pi/Documents/motionDetectionProject/pictures/photo_logs.txt"



#SETUP
print("Removing log files...")
if (os.path.exists(LOG_FILE_NAME)):
    os.remove(LOG_FILE_NAME)
    print(">Log files removed")
else:
    print(">No old log files")

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1Pin, GPIO.OUT)
GPIO.setup(LED2Pin, GPIO.OUT)
GPIO.setup(ButtonPin, GPIO.IN)
GPIO.setup(PIRSensePin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
timeCount = 1

print(">Initalization complete")


    
def takePhoto():
    t = str(time.time())
    name = "fswebcam /home/pi/Documents/motionDetectionProject/pictures/" + t + ".jpg"
    os.system(name)
    with open(LOG_FILE_NAME, "a") as d:
        d.write(name)
        d.write("\n")
    return name
        
try:
    while (True):
        time.sleep(0.1)
        GPIO.output(LED2Pin, GPIO.HIGH)
        sensorState = GPIO.input(PIRSensePin)
        if (sensorState == 1):
            timeCount = timeCount + 1
        if (timeCount == 3):
            GPIO.output(LED1Pin, GPIO.HIGH)
            name = takePhoto()
            print(">photo taken")
            timeCount = 1
        else:
            GPIO.output(LED1Pin, GPIO.LOW)
        if(GPIO.input(ButtonPin) == 1):
            print("cleaning up GPIO")
            GPIO.cleanup()
            break
            
            
except (KeyboardInterrupt):
    print("cleaning up GPIO")
    GPIO.cleanup()
           
           
