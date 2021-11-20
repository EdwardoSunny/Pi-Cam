from flask import Flask, redirect, url_for, render_template, jsonify, request
import os, test

CAMERA_FOLDER_PATH = "/home/pi/Documents/motionDetectionProject/pictures"
LOG_FILE_NAME = CAMERA_FOLDER_PATH + "/photo_logs.txt"
photoCount = 0
#front end

app = Flask(__name__, static_url_path=CAMERA_FOLDER_PATH, static_folder=CAMERA_FOLDER_PATH)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/controls")
def testing():
    return render_template('control.html')

@app.route("/deletePic/")
def delete():
    dir = "/home/pi/Documents/motionDetectionProject/pictures"
    for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
    return "Deletion Successful" + "\n" + "<a href='/'>Home</a>"
    
@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="Admin"))

@app.route("/check-movement")
def check_movement():
    message = "no movement"
    images = ""
    lineCount = 0
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME, "r") as f:
            for line in f:
                lineCount += 1
                temp = line.replace("fswebcam ", "")
                images += "<br/><br/>" + "<img src=\"" + temp + "\">"
        message = str(lineCount) + " photos taken due to movement <br/><br/>"
        print(images)
    return message + images

if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)