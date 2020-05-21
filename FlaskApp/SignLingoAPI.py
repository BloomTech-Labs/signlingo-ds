from flask import Flask, request, render_template, flash, redirect, Response
from werkzeug.utils import secure_filename
from flask import jsonify
import os, time

from HelperFunctions import splitter, clear_temp, allowed_file
from ModelFunctions import main as img_detector


app = Flask(__name__, template_folder='templates')
if not os.path.isdir('TEMPPICS'):
    os.mkdir('TEMPPICS')
if not os.path.isdir('TEMPVID'):
    os.mkdir('TEMPVID')


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def api():
    start_time = time.time()
    if request.method == 'POST':
        # Checks to make sure a file was actually received with the key 'video'
        if 'video' not in request.files:
            flash('No file part')
            return redirect(request.url)
        video = request.files['video']

        # Checks to make sure the video has a filename.
        if video.filename == '':
            flash('No Selected File')
            return redirect(request.url)


        if video and allowed_file(video.filename): # If a video exists and it's of an appropriate type
            filename = secure_filename(video.filename) # Apparently a good method to use to make sure no one can do silly things with filenames.
            video.save(os.path.join('TEMPVID','test_' + filename)) #Saves our video file to the TEMPVID folder.
            print('Video saved.\n')

        for vid in os.listdir('TEMPVID'):
            splitter(vid, frameskip=30) #Frameskip allows us to designate that we only save frames with a count % frameskip. 1 saves every frame.

        print("Files in temporary folder:")
        print("Temp Video folder contents:", os.listdir('TEMPVID'))
        print("Number of files in TEMPPICS:", len(os.listdir('TEMPPICS')), '\n')

        #Actual DS magic happens here.
        predict_list = [('a', 0.443), ('a', 0.852), ('s',0.241), ('m', 0.159)] #Clear this out before actually making predictions. Data here is for testing.
        # for img in os.listdir('TEMPPICS'):
        #     predict_list.append(model.predict(img)) #Or however we want to predict the result.
        classes, confidences = img_detector()
        print("TYPES - ", type(classes), type(confidences))
        x = list(zip(classes, confidences))
        print(x)
        clear_temp() # Helper function that clears both of the temporary folders.

        print("Temp folders cleared.")
        print("Temp Video folder contents:", os.listdir('TEMPVID'))
        print("Number of files in TEMPPICS:", len(os.listdir('TEMPPICS')), '\n')

        end_time = time.time()
        print("TOTAL RUN TIME = ", (end_time - start_time))
        return str(x)
        #return jsonify(predict_list) # Or some variant thereof


import random

@app.route('/test_api', methods=['POST'])
def test_api():
    video = request.files['video']
    random_bit = random.getrandbits(1)
    random_boolean = [bool(random_bit)]
    return jsonify(random_boolean)