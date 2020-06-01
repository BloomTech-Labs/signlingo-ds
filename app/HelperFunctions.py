import cv2
import os
import json
import numpy as np


def splitter(video, frameskip=1):
    """
    Accepts a video file as first param.
    frameskip must be an integer, only frames with a count % frameskip == 0 will be saved.
    frameskip == 1 keeps all frames. frameskip == 2 drops every other frame, etc.
    Outputs selected frames into TEMPPICS folder.
    """

    cap = cv2.VideoCapture(os.path.join('TEMPVID', video))

    count = 0
    frame_list = []
    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            if count % frameskip == 0:
                cv2.imwrite(os.path.join('TEMPPICS', 'frame{:d}.jpg'.format(count)), frame)
            count += 1
        else:
            break

    return frame_list


def allowed_file(filename):
    """
    Returns true the file is of an appropriate type and has an appropriate name, otherwise returns false.
    """
    # Change if using videos of type other than mp4
    allowed_extensions = {'mp4'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def clear_temp():
    """
    Clears the entire contents of the TEMPVID and TEMPPICS folders.
    """
    for file in os.listdir('TEMPVID'):
        os.remove(os.path.join('TEMPVID', file))

    for file in os.listdir('TEMPPICS'):
        os.remove(os.path.join('TEMPPICS', file))
