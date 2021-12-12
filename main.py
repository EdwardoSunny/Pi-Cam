import RPi.GPIO as GPIO
import time
import os
import face_recognition
import os
import cv2


KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
TOLERENCE = 0.45;
FRAME_THICKNESS = 3;
FONT_THICKNESSS = 2;
MODEL = "hog" #cnn if gpu

print("Initializing...")
PIRSensePin = 4
LED1Pin = 17
LED2Pin = 22
ButtonPin = 26
LOG_FILE_NAME = "/home/pi/Documents/motionDetectionProject/photo_logs.txt"

print("loading known faces")
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0] #first face it finds
        known_names.append(name)
        known_faces.append(encoding)
        print(filename)
        
print("processing unknown faces")


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
    name = "fswebcam /home/pi/Documents/motionDetectionProject/unknown_faces/" + t + ".jpg"
    os.system(name)
    with open(LOG_FILE_NAME, "a") as d:
        d.write(name)
        d.write("\n")
    return name

processTimeCount = 0
try:
    while (True):
        time.sleep(0.1)
        #on indicator
        GPIO.output(LED2Pin, GPIO.HIGH)
        sensorState = GPIO.input(PIRSensePin)
        print(sensorState)
        if (sensorState == 1):
            timeCount = timeCount + 1
        if (timeCount == 5):
            GPIO.output(LED1Pin, GPIO.HIGH)
            name = takePhoto()
            print(">photo taken")
            timeCount = 1
            
        else:
            GPIO.output(LED1Pin, GPIO.LOW)
        if (processTimeCount >= 10):
            processTimeCount = 0
            print("processing unknown faces")

            for filename in os.listdir(UNKNOWN_FACES_DIR):
                print(filename)
                image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
                locations = face_recognition.face_locations(image,model=MODEL)
                encodings = face_recognition.face_encodings(image,locations) #where are locations we want to encode
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #BGR is open cv use
    
                for face_encodings, face_location in zip(encodings, locations):
                    results = face_recognition.compare_faces(known_faces, face_encodings, TOLERENCE) #compare current encoding to everyface, and returns list of booleans
                    match = None
                    if (True in results):
                        match = known_names[results.index(True)]
                        print(f"Match found: {match}")
        if(GPIO.input(ButtonPin) == 1):
            print("wiping pictures memory")
            delCMD = "rm -v /home/pi/Documents/motionDetectionProject/unknown_faces/*"
            os.system(delCMD)
            print("cleaning up GPIO")
            GPIO.cleanup()
            break
        processTimeCount= processTimeCount + 1
            
            
except (KeyboardInterrupt):
    print("cleaning up GPIO")
    GPIO.cleanup()
           
           

