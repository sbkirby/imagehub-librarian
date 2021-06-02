"""
detect_objects_cv2.py - Object Detection module for mqtt_client.py

files needed:
coco.names, ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt and frozen_inference_graph.pb

Detection Model Source:
http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v3_large_coco_2020_01_14.tar.gz

Adapted from Adrian Rosebrock code
Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
import cv2
import numpy as np
import os


score_threshold = 0.45  # score threshold to detect object
nms_threshold = 0.2  # A threshold used in non maximum suppression
confThreshold = 0.55  # A threshold used to filter boxes by confidences (0.5f default)
debug = True  # Set to True to view in Portainer log view of opencv docker file
# define Working Directory
wrk_dir = os.path.dirname(os.path.realpath(__file__))

classNames = []
classFile = os.path.join(wrk_dir, 'coco.names')
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

considerNames = ["bird", "dog", "cat", "person", "car", "bicycle", "bus", "motorbike", "truck"]

configPath = os.path.join(wrk_dir, 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
weightsPath = os.path.join(wrk_dir, 'frozen_inference_graph.pb')

if debug:
    print("[INFO] loading model...")

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

if debug:
    print("[INFO] detecting: {}...".format(",".join(obj for obj in considerNames)))


# detect objects in image frames
def detectObject(image):
    frame = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    classIds, confidences, bbox = net.detect(frame, confThreshold=confThreshold)
    bbox = list(bbox)
    confidences = list(np.array(confidences).reshape(1, -1)[0])
    confidences = list(map(float, confidences))
    objCount = {obj: 0 for obj in considerNames}

    # Performs non maximum suppression (NMS) given boxes and corresponding scores
    indices = cv2.dnn.NMSBoxes(bbox, confidences, score_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        if len(classIds) != 0:
            if classNames[classIds[i][0]-1] in considerNames:
                # increment the count of the particular object
                objCount[classNames[classIds[i][0]-1]] += 1

    return objCount


def main():
    print(detectObject(os.path.join(wrk_dir, 'objects_test_image_1.jpg')))
    # print(detectObject(os.path.join(wrk_dir, 'objects_test_image_2.jpg')))


if __name__ == '__main__':
    main()
