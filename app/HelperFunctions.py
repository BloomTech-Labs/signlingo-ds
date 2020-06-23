import cv2
import os
import random
import string
import ffmpeg


def splitter(video, uuid, frameskip=1):
    """
    This function splits a video file into a number of images, in order to feed the model more effectively.

    Accepts a video file as first param.

    frameskip is used for tweaking the response time of the model. Higher frame skip numbers will mean faster runtimes,
    but less predictions, which may make it harder to catch a correct prediction.
    frameskip must be an integer, only frames with a count % frameskip = 0 will be saved.
    frameskip = 1 keeps all frames. frameskip = 2 drops every other frame, etc.
    Outputs selected frames into TEMPPICS/VID_(uuid) folder.
    """
    cap = cv2.VideoCapture(os.path.join('TEMPVID', 'VID_' + uuid, video))
    os.mkdir(os.path.join('TEMPPICS', 'PICS_' + uuid))

    # Mobile devices take videos in landscape mode and embed metadata to encode the rotation, cv2 does not check this.
    # This ends up resulting in images from mobile devices being sideways.
    # The function below reads metadata for the correct rotation.
    rotate_code = check_rotation(os.path.join('TEMPVID', 'VID_' + uuid, video))

    count = 0
    frame_list = []
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            if rotate_code is not None:
                frame = cv2.rotate(frame, rotate_code)
            if count % frameskip == 0:
                cv2.imwrite(os.path.join('TEMPPICS', 'PICS_' + uuid, 'frame{:d}.jpg'.format(count)), frame)
            count += 1
        else:
            break

    return frame_list


def clear_temp(uuid):
    """
    Clears the entire contents of the TEMPVID/VID_(uuid) and TEMPPICS/PICS_(uuid) folders.
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
    # This function utilizes ffmpeg-python, which requires ffmpeg to be installed on the system.
    # https://www.ffmpeg.org

    meta_dict = ffmpeg.probe(path_video_file)
    rotate_code = None

    # The rotate tag is not in the same index every time, so we iterate over the indeces in order to find it.
    # The loop below will return a cv2 rotate code if the image needs rotated. Otherwise returns None
    for index in meta_dict['streams']:
        if 'rotate' in index['tags'].keys():
            if int(index['tags']['rotate']) == 90:
                rotate_code = cv2.ROTATE_90_CLOCKWISE
                print('ROTATED 90 CLOCKWISE')
            elif int(index['tags']['rotate']) == 180:
                rotate_code = cv2.ROTATE_180
                print('ROTATED 180')
            elif int(index['tags']['rotate']) == 270:
                rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE
                print('ROTATED 90 COUNTERCLOCKWISE')

    if rotate_code is None:
        print("NO ROTATION")

    return rotate_code
