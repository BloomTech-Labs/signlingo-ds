import cv2
import os
import json
import numpy as np

# def extractFrames(pathIn, pathOut):
#     os.mkdir('images/')

# cap = cv2.VideoCapture("2020-05-14_14-55-47.mp4")
#
# count=0
# print(cap)
#
# while (cap.isOpened()):
#     ret, frame = cap.read()
#     #print(ret)
#     if ret:
#         print('Read %d frame: ' % count, ret)
#         cv2.imwrite(os.path.join('images/', 'frame{:d}.jpg'.format(count)), frame)
#         count += 1
#     else:
#         break
#
# cap.release()
# cv2.destroyAllWindows()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


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

# frames = splitter('2020-05-14_14-55-47.mp4')
#
# for frame in frames:
#     model.predict(frame)


#
# def main():
#     extractFrames()
#
# if __name__ == '__main__':
#     main()