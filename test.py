import face_recognition
import os
import cv2


KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
TOLERENCE = 0.45;
FRAME_THICKNESS = 3;
FONT_THICKNESSS = 2;
MODEL = "hog" #cnn if gpu

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
            #found match, use cv2 to draw square thingy
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0,255,0]
            
            #face rect
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
            
            #text rect
            t_top_left = (face_location[3], face_location[2])
            t_bottom_right = (face_location[1], face_location[2]+22)
            cv2.rectangle(image, t_top_left, t_bottom_right, color, cv2.FILLED)
            
            #text
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESSS)
    cv2.imshow(filename,image)
    cv2.waitKey(1000)
