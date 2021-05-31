#!/usr/bin/env python3
""" USAGE
 dashboard.py will display a Montage of camera images found in the 'latest_images.json'
 file located defined in the 'latest_images' variable below.

 python dashboard.py --montageW 2 --montageH 2 --imageW 420 --imageH 315
   OR
 python dashboard.py -mW 2 -mH 2 -iW 420 -iH 315

 modified version of server.py by Adrian Rosebrock
 Stephen B. Kirby March 6, 2021
"""

# import the necessary packages
from imutils import build_montages
import numpy as np
import time
import argparse
import imutils
import cv2
import json
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mW", "--montageW", required=False, type=int, help="montage frame width", default=2)
ap.add_argument("-mH", "--montageH", required=False, type=int, help="montage frame height", default=3)
ap.add_argument("-iW", "--imageW", required=False, type=int, help="image width", default=420)
ap.add_argument("-iH", "--imageH", required=False, type=int, help="image height", default=315)
args = vars(ap.parse_args())

# define Working Directory
work_dir = os.path.dirname( __file__ )

with open(os.path.join(work_dir, 'config.json')) as json_data_file:
    data = json.load(json_data_file)

# JSON data file location and name
latest_images = os.path.join(data["imagehub_data"], 'latest_images.json')
# Test Pattern image displayed if an error occurs while reading a file entry
test_pattern = os.path.join(work_dir, 'images', data["test_pattern"])

# display width & height of each video feed
display_width = args["imageW"]
display_height = args["imageH"]
# specify location of camera ID on screen
camID_width = int(display_width * 0.2)
camID_height = int(display_height * 0.07)

# assign montage width and height so we can view all incoming frames
# in a single "dashboard"
mW = args["montageW"]
mH = args["montageH"]
# initialize dictionary variables
tmp_boxes = {}
bounding_boxes = {}
# define total width and height of dashboard
tot_W = mW * display_width
tot_H = mH * display_height

# build bounding boxes for each of the images displayed
for i in reversed(range(mW)):
    for j in reversed(range(mH)):
        if j == 0:
            extra = 0
        else:
            extra = 1
        tmpW = tot_W - display_width + extra
        tmpH = tot_H - display_height + extra
        tmp_boxes[j, i] = [tmpW, tmpH, tot_W, tot_H]
        tot_H = tot_H - display_height
    tot_W = tot_W - display_width
    tot_H = mH * display_height

# sort bounding_boxes by regions of dashboard (e.g. (0,0), (0,1), (1,0)...)
for i in sorted(tmp_boxes.keys()):
    bounding_boxes[i] = tmp_boxes[i]


# mouse click event for main window
def click_dashboard(event, x, y, flags, param):
    # grab references to the global variables
    global refPt

    refPt = ()
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = find_bounding_box(x, y)
        cam_name = ''
        if len(refPt) > 0:
            cam_name = camDict[refPt]
        frame = cv2.imdecode(np.fromfile(orgImgDict[cam_name], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if frame.shape[:2][0] > 1500:
            frame = cv2.resize(frame, (1024, 768))
        cv2.imshow(cam_name, frame)


# find the region or image clicked
def find_bounding_box(x, y):
    region = ()
    for i in reversed(range(mW)):
        for j in reversed(range(mH)):
            if ((x >= bounding_boxes[j, i][0]) and (x <= bounding_boxes[j, i][2]) and
                    (y >= bounding_boxes[j, i][1]) and (y <= bounding_boxes[j, i][3])):
                region = (j, i)
    return region


# initialize frame dictionary, camera dictionary, original image dictionary,
# key_list of dashboard regions and last_read
frameDict = {}
camDict = {}
orgImgDict = {}
key_list = list(bounding_boxes.keys())
last_read = 0

# start looping over all the frames
while True:
    # check last time file updated
    try:
        mtime = os.path.getmtime(latest_images)
        time.sleep(1)
    except OSError:
        print('OSError: reading ', latest_images)
        mtime = 0

    # check to see if the Modified Time of file is greater than last_read variable
    if mtime > last_read:
        # read file
        with open(latest_images, 'r') as myfile:
            data = myfile.read()

        # JSON parse file
        try:
            obj = json.loads(data)
        except:
            print('JSON Error: reading ', latest_images)
            continue
        # update last_read variable to last Modified Time
        last_read = mtime
        # loop thru entries in file
        for num, cam in enumerate(obj):
            image = cam['filename']
            rpiName = cam['nodename']
            # build dictionary of cameras and original images
            orgImgDict[rpiName] = image
            # build dictionary of dashboard image regions (bounding boxes) for each camera
            camDict[key_list[num]] = rpiName
            try:
                frame = cv2.imdecode(np.fromfile(image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            except Exception:
                # Load Test Pattern if file doesn't exist
                frame = cv2.imdecode(np.fromfile(test_pattern, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # resize the frame to have a maximum width of 400 pixels, then
            # grab the frame dimensions and construct a blob
            frame = imutils.resize(frame, width=display_width)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (display_width, display_height)), 0.007843,
                                         (display_width, display_height), 127.5)

            # draw the sending device name on the frame (x,y)
            cv2.putText(frame, rpiName, (display_width - camID_width, display_height - camID_height), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1)

            # update the new frame in the frame dictionary
            frameDict[rpiName] = frame

            # build a montage using images in the frame dictionary
            montages = build_montages(frameDict.values(), (w, h), (mW, mH))

            # display the montage(s) on the screen
            for (i, montage) in enumerate(montages):
                cv2.namedWindow("Home Monitor ({})".format(i), cv2.WINDOW_AUTOSIZE)
                cv2.imshow("Home Monitor ({})".format(i), montage)
                cv2.setMouseCallback("Home Monitor ({})".format(i), click_dashboard, montage)

    # if the `q` key or ESC key is pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
