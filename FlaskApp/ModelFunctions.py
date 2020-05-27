import numpy as np
import argparse, time, os, cv2

CONF_THRES=0.0001 # Confidence Threshold for detection reporting.
NMS_THRES=0.1 # Non-Maxima Suppression threshold, shouldn't need to be changed.
YOLO_PATH="./"
LABELS = 'alphabet.names'
WEIGHTS = 'alphabet.weights'
CFG = 'alphabet.cfg'

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
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    return net

def get_prediction(image, net, LABELS, COLORS):
    """
    Gets prediction from the image
    """
    
    #Getting image height/width
    (img_height, img_width) = image.shape[:2]

    #Determining output layer names
    output_layer_names = net.getLayerNames()
    output_layer_names = [output_layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    #Constructs a blob from the image input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)

    net.setInput(blob)

    start = time.time()

    layer_outputs = net.forward(output_layer_names)

    #print("Layer Outputs:\n", layer_outputs)

    end = time.time()

    #Show timing info
    print("[INFO] YOLO took {:.6f} seconds.".format(end - start))

    #Initializing our list of bounding boxes, confidences, and class ids.
    b_boxes = []
    confidences = []
    class_ids = []

    #loop over each of the layer outputs.
    for output in layer_outputs:
        # Loop over each detection
        for detection in output:
            #Extracting class id and confidence
            scores = detection[5:]
            #print(scores)

            class_id = np.argmax(scores)

            confidence = scores[class_id]

            if confidence > CONF_THRES:
                #If our confidence is greater than our confidence threshold, we'll draw some bounding boxes.

                #YOLO actually returns the coordinates of the center of the object it detected, and the box's width/height.
                #We'll scale the box's dimensions depending on the original image dimensions.
                box = detection[0:4] * np.array([img_width, img_height, img_width, img_height])
                (centerX, centerY, width, height) = box.astype("int")

                #Use the center coordinates to derive the top and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                #Update our lists of bounding box coordinates, confidences, and class IDs
                b_boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Applying non-maxima suppression to suppress weak, overlapping bounding boxes.
    idxs = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRES, NMS_THRES)

    # Ensuring at least one detection exists
    if len(idxs) > 0:
        #Loop over the indexes we are keeping.
        for i in idxs.flatten():
            #Extracting bounding box coordinates.
            (x, y) = (b_boxes[i][0], b_boxes[i][1])
            (w, h) = (b_boxes[i][2], b_boxes[i][3])

            #draw a bounding box rectangle and label
            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])

            cv2.putText(image, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image, class_ids, confidences



def main():
    labels_path = os.path.join('model', LABELS)
    cfg_path = os.path.join('model', CFG)
    weights_path = os.path.join('model', WEIGHTS)

    labels = get_labels(labels_path)
    config = get_config(cfg_path)
    weights = get_weights(weights_path)

    nets = load_model(config, weights)

    colors = get_colors(labels)
    classes = []
    confids = []
    for img in os.listdir('TEMPPICS'):
        image = cv2.imread(os.path.join('TEMPPICS', img))

        result_img, class_ids, confidences = get_prediction(image, nets, labels, colors)
        classes.append(class_ids)
        confids.append(confidences)

        print("Predicted class ids:", class_ids)
        print("Predicted confidence levels", confidences)

        # cv2.imshow("Image", result_img)
        # cv2.waitKey()

    return classes, confids



if __name__ == '__main__':
    main()
