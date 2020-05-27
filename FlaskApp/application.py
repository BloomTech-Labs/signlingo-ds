from flask import Flask, request, render_template, flash, redirect, Response
from werkzeug.utils import secure_filename
from flask import jsonify
import os, time
import random

from HelperFunctions import splitter, clear_temp, allowed_file
from ModelFunctions import main as img_detector

application = Flask(__name__, template_folder='templates')

# Multiple users will conflict. Transition to a generator/temporary memory solution.
if not os.path.isdir('TEMPPICS'):
    os.mkdir('TEMPPICS')
if not os.path.isdir('TEMPVID'):
    os.mkdir('TEMPVID')


@application.route('/')
def home():
    return render_template("index.html")


@application.route('/test_api', methods=['POST'])
def test_api():
    video = request.files['video']
    random_bit = random.getrandbits(1)
    random_boolean = bool(random_bit)
    return jsonify({'Random Test Boolean':random_boolean})


@application.route('/api', methods=['POST'])
def api():
    start_time = time.time()
    
    # Checks to make sure a file was actually received with the key 'video'
    if 'video' not in request.files:
        flash('No file part')
        return reThedirect(request.url)
    video = request.files['video']

    # Checks to make sure the video has a filename.
    if video.filename == '':
        flash('No Selected File')
        return redirect(request.url)

    if video and allowed_file(video.filename): # If a video exists and it's of an appropriate type
        filename = secure_filename(video.filename) # Apparently a good method to use to make sure no one can do silly things with filenames.
        video.save(os.path.join('TEMPVID','test_' + filename)) #Saves our video file to the TEMPVID folder.

    for vid in os.listdir('TEMPVID'):
        splitter(vid, frameskip=30) #Frameskip allows us to designate that we only save frames with a count % frameskip. 1 saves every frame.

    # Actual DS magic happens here.
    classes, confidences = img_detector()
    x = list(zip(classes, confidences))
    clear_temp() # Helper function that clears both of the temporary folders.
    end_time = time.time()
    
    return str(x)
