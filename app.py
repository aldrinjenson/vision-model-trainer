from flask import Flask, current_app, url_for, request
import os
from werkzeug.utils import secure_filename
from markupsafe import escape
import cv2
from trainer import train
import threading


UPLOAD_FOLDER = 'videos'
IMAGES_FOLDER = 'images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.get("/")
def home():
    return current_app.send_static_file("index.html")


@app.route("/upload", methods=['post'])
def upload():
    videoFile = request.files.get('file')
    # file.fileName = ther person's name (passed from client)
    filename = secure_filename(videoFile.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.webm')
    videoFile.save(filePath)

    imagesFolderName = IMAGES_FOLDER + '/' + filename
    frameNr = 0
    if os.path.exists(imagesFolderName):
        numFiles = len(os.listdir(imagesFolderName))
        frameNr = numFiles
    else:
        os.makedirs(imagesFolderName)

    capture = cv2.VideoCapture(filePath)
    imagePath = os.getcwd() + f'/images/{filename}'

    success = True
    while (success):
        success, frame = capture.read()
        if success and frameNr % 2 == 0:
            cv2.imwrite(f'{imagesFolderName}/frame_{frameNr}.jpg', frame)
        frameNr = frameNr+1
    capture.release()
    print("going to train")
    threading.Thread(target=train).start()
    return "file received and splitted successfully"
