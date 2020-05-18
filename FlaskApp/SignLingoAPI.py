from flask import Flask, request, send_file, render_template
from flask import jsonify
import json, codecs

from HelperFunctions import NumpyEncoder
import cv2

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def api():
    video = request.files['video']
    video = "2020-05-14_14-55-47.mp4"
    frames = splitter(video)


    json_dump = json.dumps(frames[0], cls=NumpyEncoder)
    print(json_dump)
    #video = video['video'].read()
    #video = request.form['video']
    # video2 = request.files['video']
    #print(video)

    return json_dump
    #return render_template("display.html", video=video)
    #return send_file(video)

def splitter(video):
    cap = cv2.VideoCapture(video)

    count = 0
    frame_list = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        # print(ret)

        if ret:
            #print('Read %d frame: ' % count, ret)
            frame_list.append(frame)
            count += 1
        else:
            break

    return frame_list