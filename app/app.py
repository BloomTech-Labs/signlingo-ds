from flask import Flask, request, render_template, flash, redirect, Response
from werkzeug.utils import secure_filename
# from memory_profiler import profile
from flask import jsonify
import os
import time
import random
import json


from HelperFunctions import splitter, clear_temp, allowed_file, create_uuid
from ModelFunctions import main as img_detector
from ModelFunctions import LABELS, WEIGHTS, CFG

app = Flask(__name__, template_folder='templates')

# Multiple users will conflict. Transition to a generator/temporary memory solution.
if not os.path.isdir('TEMPPICS'):
    os.mkdir('TEMPPICS')
if not os.path.isdir('TEMPVID'):
    os.mkdir('TEMPVID')

# Manually testing API endpoint
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def api():
    start_time = time.time()

    # Helper function to create a unique identifier for this process. UUID is necessary to prevent conflicts.
    uuid = create_uuid()
    
    # Checks to make sure a file was actually received with the key 'video'
    if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)

    #Pulls the video from the request
    video = request.files['video']

    #This is the letter that the front end is expecting
    letter = request.form.get('expected')
    letter = letter.upper()

    # This gets the handedness of the user, commented out for the time being and just assumes all photos are right handed.
    # rhanded = request.form.get('right-handed')
    # print(int(rhanded), int(rhanded) == 1)
    # rhanded = (int(rhanded) == 1)
    rhanded = True


    if video: # If a video exists
        filename = secure_filename(video.filename) # Apparently a good method to use to make sure no one can do silly things with filenames.
        vid_path = os.path.join('TEMPVID', 'VID_'+ uuid) #This will be the folder our temp vid lives in.
        os.mkdir(vid_path) # Creates the folder to be saved in.
        video.save(os.path.join(vid_path, 'test_' + filename)) #Saves our video file to the TEMPVID folder.
    else: #If the video does not exist, return.
        flash('File of incorrect type.')
        return redirect(request.url)

    splitter_start_time = time.time()
    for vid in os.listdir(vid_path):
        splitter(vid, uuid, frameskip=15) #Frameskip allows us to designate that we only save frames with a count % frameskip. 1 saves every frame. See splitter docstring for more info.
    splitter_end_time = time.time()
    #print(f"Total Splitter runtime - {(splitter_end_time - splitter_start_time):.2f} seconds")

    # Actual DS magic happens here.
    classes, confidences = img_detector(uuid, rhanded) #This is the function called 'main' in ModelFunctions.py
    predictions = list(zip(classes, confidences))
    clear_temp(uuid) # Helper function that clears both of the temporary folders.

    #Dictionary for comparing the results of the model to a letter, or converting an expected letter to a number.
    Dictionary = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
        'I': 8,
        'J': 9,
        'K': 10,
        'L': 11,
        'M': 12,
        'N': 13,
        'O': 14,
        'P': 15,
        'Q': 16,
        'R': 17,
        'S': 18,
        'T': 19,
        'U': 20,
        'V': 21,
        'W': 22,
        'X': 23,
        'Y': 24,
        'Z': 25,
    }
    inverse = {v:k for k, v in Dictionary.items()}


    testing_list = []
    print("Predictions-\n",predictions)

    #The below for loop is for processing the predictions into the format we want it to be in.
    for double in predictions:
        holding_array = []
        for individual in double:
            if len(individual) != 0:
                if individual[0] == int(individual[0]):
                    holding_array.append(inverse[individual[0]])
                else:
                    holding_array.append(float(individual[0]))
        testing_list.append(holding_array)


    # Check that predictions match expected
    is_match = False

    #Currently this API only looks to see if the expected letter was predicted at all. Sets is_match to true if it finds a matching letter.
    for pred in testing_list:
        if len(pred) != 0:
            if letter == pred[0]:
                is_match = True
                break

    end_time = time.time()
    runtime = end_time-start_time


    #Returned data looks like this when returned from the API.
    #{"Wanted_Letter": "B", "is_match": true, "runtime_seconds": 3.5063774585723877,
    #"full_predictions": [["B", 0.8875290751457214], ["B", 0.9751415252685547], ["B", 0.9301596283912659],
    #                     ["B", 0.9111566543579102], ["B", 0.7824452519416809]]}
    return_dict = {'Wanted_Letter': letter,
                   'is_match': is_match,
                   'runtime_seconds': runtime,
                   'full_predictions' : testing_list
                   }


    X = json.dumps(return_dict)

    return Response(X,  mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)