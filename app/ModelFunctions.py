import numpy as np
import argparse, time, os, cv2
from PIL import Image, ImageOps

# from memory_profiler import profile

CONF_THRES = 0.0001  # Confidence Threshold for detection reporting.
NMS_THRES = 0.1  # Non-Maxima Suppression threshold, shouldn't need to be changed.
YOLO_PATH = "./"
LABELS = 'yolov3.names'
WEIGHTS = 'yolov3-tiny_custom_34000.weights'
CFG = 'yolov3-tiny_custom_test.cfg'


def get_labels(labels_path):
    """
    Loads the labels used by our YOLO model
    """
    lpath = os.path.sep.join(['./model', LABELS])
    labels = open(lpath).read().strip().split("\n")
    return labels


def get_colors(labels):
    """
    Initializes a list of colors to represent each possible class label.
    * This function may not be entirely necessary given how we get data back from the model.
    """
    np.random.seed(1337)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    return COLORS


def get_weights(weights_path):
    """
    Loads the weights used by the YOLO model.
    """
    weightsPath = os.path.sep.join(['./model', WEIGHTS])
    return weightsPath


def get_config(config_path):
    """
    Gets the config used by the YOLO model.
    """
    configPath = os.path.sep.join(['./model', CFG])
    return configPath


def load_model(config_path, weights_path):
    """
    Loads the model
    """
    print("[INFO] loading YOLO...")
    model_load_start_time = time.time()
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    model_load_end_time = time.time()
    print('[INFO] Model Loading time -', model_load_end_time - model_load_start_time, " seconds.")
    return net


# @profile
def get_prediction(image, net, LABEL, COLOR):
    """
    Gets prediction from the image
    """

    # Getting image height/width
    # prediction_start_time = time.time()
    (img_height, img_width) = image.shape[:2]

    # Determining output layer names
    output_layer_names = net.getLayerNames()
    output_layer_names = [output_layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Constructs a blob from the image input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)

    net.setInput(blob)

    # start = time.time()

    layer_outputs = net.forward(output_layer_names)

    # end = time.time()

    # Show timing info
    # print(f"[INFO] YOLO took {(end - start):.6f} seconds on net.forward step.")

    # Initializing our list of bounding boxes, confidences, and class ids.
    b_boxes = []
    confidences = []
    class_ids = []

    # loop over each of the layer outputs.
    for output in layer_outputs:
        # Loop over each detection
        for detection in output:
            # Extracting class id and confidence
            scores = detection[5:]
            # print(scores)

            class_id = np.argmax(scores)

            confidence = scores[class_id]

            if confidence > CONF_THRES:
                # If our confidence is greater than our confidence threshold, we'll draw some bounding boxes.

                # YOLO returns the coordinates of the center of the object it detected, and the box's width/height.
                # We'll scale the box's dimensions depending on the original image dimensions.
                box = detection[0:4] * np.array([img_width, img_height, img_width, img_height])
                (centerX, centerY, width, height) = box.astype("int")

                # Use the center coordinates to derive the top and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # Update our lists of bounding box coordinates, confidences, and class IDs
                b_boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Applying non-maxima suppression to suppress weak, overlapping bounding boxes.
    idxs = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRES, NMS_THRES)

    # Ensuring at least one detection exists
    if len(idxs) > 0:
        # Loop over the indexes we are keeping.
        for i in idxs.flatten():
            # Extracting bounding box coordinates.
            (x, y) = (b_boxes[i][0], b_boxes[i][1])
            (w, h) = (b_boxes[i][2], b_boxes[i][3])

            # draw a bounding box rectangle and label
            color = [int(c) for c in COLOR[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

            text = "{}: {:.4f}".format(LABEL[class_ids[i]], confidences[i])

            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    # prediction_end_time = time.time()
    # print(f"Image prediction time {(prediction_end_time - prediction_start_time):.2f} seconds")

    return image, class_ids, confidences


def main(uuid, rhanded):
    # main_start_time = time.time()

    # The below gets the labels, configuration, and weights, and then loads the model.
    # Note, a lot of the paths are hard coded into the functions after bug hunting and haven't been refactored back yet.
    labels_path = os.path.join('model', LABELS)
    cfg_path = os.path.join('model', CFG)
    weights_path = os.path.join('model', WEIGHTS)
    labels = get_labels(labels_path)
    config = get_config(cfg_path)
    weights = get_weights(weights_path)

    # Loading the model
    nets = load_model(config, weights)

    # Grabs the colors - Likely not necessary given how we return data.
    # The only thing it's used for is internal image display for debugging purposes.
    colors = get_colors(labels)

    # Initializing classes and confidences lists
    classes = []
    confids = []

    pic_path = os.path.join('TEMPPICS', 'PICS_' + uuid)
    for img in os.listdir(pic_path):
        print("Right handed = ", (True == rhanded))
        if not rhanded:
            # If the image is not right handed, mirror it.
            im = Image.open(os.path.join(pic_path, img))
            im = ImageOps.mirror(im)
            im.save(os.path.join(pic_path, 'mirrored.jpg'), quality=50)
            image = cv2.imread(os.path.join(pic_path, 'mirrored.jpg'))
        else:
            image = cv2.imread(os.path.join(pic_path, img))

        # Gets predictions on this image.
        # We really only care about class_ids and confidences, but result_img can be used for debugging
        result_img, class_ids, confidences = get_prediction(image, nets, labels, colors)
        classes.append(class_ids)
        confids.append(confidences)

        # print("Predicted class ids:", class_ids)
        # print("Predicted confidence levels", confidences)

        # Uncomment the two lines below to show an image popup of a prediction.
        # cv2.imshow("Image", result_img)
        # cv2.waitKey()

    # main_end_time = time.time()
    # print(f"Main loop finished in {(main_end_time - main_start_time):.2f} seconds")
    return classes, confids

# if __name__ == '__main__':
#     main()
