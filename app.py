from flask import Flask, current_app, url_for, request
import os
from werkzeug.utils import secure_filename
from markupsafe import escape
import cv2


UPLOAD_FOLDER = 'videos'
IMAGES_FOLDER = 'images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return "index page"


@app.post('/video')
def getVideo():
    f = request.files[0]
    print(f)
    return 'video received'


@app.route("/upload", methods=['post'])
def form():
    videoFile = request.files.get('file')
    # file.fileName = ther person's name (passed from client)
    filename = secure_filename(videoFile.filename)
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.webm')
    videoFile.save(filePath)

    imagesFolderName = IMAGES_FOLDER + '/' + filename
    if not os.path.exists(imagesFolderName):
        os.makedirs(imagesFolderName)

    capture = cv2.VideoCapture(filePath)
    frameNr = 0
    imagePath = os.getcwd() + f'/images/{filename}'
    print(imagePath)

    while (True):
        success, frame = capture.read()
        print(frameName)
        if success and frameNr % 5 == 0:
            cv2.imwrite(f'{imagesFolderName}/frame_{frameNr}.jpg', frame)
        else:
            break
        frameNr = frameNr+1
    print(imagePath)
    capture.release()
    return "file received"


@app.get("/home")
def home():
    return current_app.send_static_file("index.html")


@app.get('/users/<string:name>')
def user_hello(name):
    return f"Hello {escape(name)}"


@app.route('/path/<path:subpath>', methods=["GET"])
def show_subpath(subpath):
    return f"Subpath = {escape(subpath)}"
