
from moviepy.editor import *
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


@app.get("/createMovie/<folder_name>")
def createMovie(folder_name: str):
    folder = f"images/{folder_name}/"
    image_files = [
        folder + f for f in os.listdir(folder) if f.endswith(".jpg")]

    img_clips = [ImageClip(f).set_duration(2) for f in image_files]
    video = concatenate_videoclips(img_clips)

    music = AudioFileClip("bgSong.mp3")
    audio = afx.audio_loop(music, duration=video.duration)
    video = video.set_audio(audio)

    video.write_videofile("output.mp4", fps=60)
    return "Done"


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
            # cv2.imwrite(f'{imagesFolderName}/frame_{frameNr}.jpg', frame)
            cv2.imwrite(f'{imagesFolderName}/frame_{frameNr//2}.jpg', frame)
        frameNr = frameNr+1
    capture.release()
    print("going to train")
    threading.Thread(target=train).start()
    return "file received and splitted successfully"
