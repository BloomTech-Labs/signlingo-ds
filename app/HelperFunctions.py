import cv2
import os
import random
import string
import ffmpeg




def splitter(video, uuid, frameskip=1):
    """
    Accepts a video file as first param.
    frameskip must be an integer, only frames with a count % frameskip == 0 will be saved.
    frameskip == 1 keeps all frames. frameskip == 2 drops every other frame, etc.
    Outputs selected frames into TEMPPICS folder.
    """
    cap = cv2.VideoCapture(os.path.join('TEMPVID','VID_' + uuid, video))
    os.mkdir(os.path.join('TEMPPICS', 'PICS_' + uuid))

    rotate_code = check_rotation(os.path.join('TEMPVID','VID_' + uuid, video))
    #rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE
    count = 0
    frame_list = []
    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            if rotate_code is not None:
                frame = cv2.rotate(frame, rotate_code)
            if count % frameskip == 0:
                cv2.imwrite(os.path.join('TEMPPICS','PICS_' + uuid, 'frame{:d}.jpg'.format(count)), frame)
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


def clear_temp(uuid):
    """
    Clears the entire contents of the TEMPVID and TEMPPICS folders.
    """
    vid_path = os.path.join('TEMPVID', 'VID_' + uuid)
    for file in os.listdir(vid_path):
        os.remove(os.path.join(vid_path, file))
    os.rmdir(vid_path)

    pic_path = os.path.join('TEMPPICS', 'PICS_' + uuid)
    for file in os.listdir(pic_path):
        os.remove(os.path.join(pic_path, file))
    os.rmdir(pic_path)

def create_uuid():
    """
    Generates a string of 10 characters to prevent concurrency conflicts.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))

def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    # print(path_video_file)
    # print('Exists? ',os.path.exists(path_video_file))


    meta_dict = ffmpeg.probe(path_video_file)
    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotateCode = None
    for index in meta_dict['streams']:
        if 'rotate' in index['tags'].keys():
            if int(index['tags']['rotate']) == 90:
                rotateCode = cv2.ROTATE_90_CLOCKWISE
                print('ROTATED 90 CLOCKWISE')
            elif int(index['tags']['rotate']) == 180:
                rotateCode = cv2.ROTATE_180
                print('ROTATED 180')
            elif int(index['tags']['rotate']) == 270:
                rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE
                print('ROTATED 90 COUNTERCLOCKWISE')

    return rotateCode

