#!/usr/bin/env python3
""" USAGE
 dashboard_jpg.py will display a Montage of streaming cameras.

 python dashboard_jpg.py --montageW 2 --montageH 2 --imageW 420 --imageH 315 --port 5558
   OR
 python dashboard_jpg.py -mW 2 -mH 2 -iW 420 -iH 315 -p 5558

 modified version of server.py by Adrian Rosebrock
 Stephen B. Kirby March 6, 2021
"""

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import logging
import logging.handlers
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
import sys
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mW", "--montageW", required=False, type=int, help="montage frame width", default=1)
ap.add_argument("-mH", "--montageH", required=False, type=int, help="montage frame height", default=1)
ap.add_argument("-iW", "--imageW", required=False, type=int, help="image width", default=1024)
ap.add_argument("-iH", "--imageH", required=False, type=int, help="image height", default=768)
ap.add_argument("-p", "--port", required=False, type=int, help="listening port - default 5558", default=5558)
ap.add_argument("-lf", "--logfile", required=False, help="path and name of logfile",
                default=os.path.join(os.path.expanduser("~"),"IOTstack","dashboard_jpg.log"))
args = vars(ap.parse_args())

# define imageHub prior to executing
imageHub = None
# define the log file location and name
log_file = args["logfile"]

# display width & height of each video feed
display_width = args["imageW"]
display_height = args["imageH"]


def main():
    # initialize the ImageHub object
    port = args["port"]
    imageHub = imagezmq.ImageHub(open_port='tcp://*:{}'.format(port))
    print('[INFO] Listening on Port {}'.format(port))
    # assign logfile attribute to class imageHub in order to use logging
    imageHub.logfile = log_file
    log = start_logging(imageHub)
    log.info('Starting dashboard_jpg.py')

    # initialize the frame  dictionary
    frameDict = {}

    # initialize the dictionary which will contain  information regarding
    # when a device was last active, then store the last time the check
    # was made was now
    lastActive = {}
    lastActiveCheck = datetime.now()

    # stores the estimated number of Pis, active checking period, and
    # calculates the duration seconds to wait before making a check to
    # see if a device was active
    ESTIMATED_NUM_PIS = 4
    ACTIVE_CHECK_PERIOD = 10
    ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

    # assign montage width and height so we can view all incoming frames
    # in a single "dashboard"
    mW = args["montageW"]
    mH = args["montageH"]

    # start looping over all the frames
    try:
        while True:
            # receive RPi name and frame from the RPi and acknowledge the receipt
            (msg, jpg_buffer) = imageHub.recv_jpg()  # sbk
            frame = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)  # sbk
            imageHub.send_reply(b'OK')
            # parse camera name
            rpiName = msg.split('|')[0]

            # skip tiny images
            (h1, w1) = frame.shape[:2]
            if ((h1, w1) == (2, 2) or (h1, w1) == (3, 3)):
                log.info("{} - {}".format(rpiName, msg))
                continue

            # if a device is not in the last active dictionary then it means
            # that its a newly connected device
            if rpiName not in lastActive.keys():
                log.info("Receiving data from {}...".format(rpiName))

            # record the last active time for the device from which we just
            # received a frame
            lastActive[rpiName] = datetime.now()

            # resize the frame to have a maximum width of 400 pixels, then
            # grab the frame dimensions and construct a blob
            frame = imutils.resize(frame, width=display_width, height=display_height)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (display_width, display_height)), 0.007843,
                                         (display_width, display_height), 127.5)

            # draw the sending device name on the frame
            cv2.putText(frame, rpiName, (display_width - 175, display_height - 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # update the new frame in the frame dictionary
            frameDict[rpiName] = frame

            try:
                # build a montage using images in the frame dictionary
                montages = build_montages(frameDict.values(), (w, h), (mW, mH))
            except Exception as ex:  # traceback will appear in log
                log.exception('Unanticipated error with no Exception handler.')

            # display the montage(s) on the screen
            for (i, montage) in enumerate(montages):
                cv2.imshow("Home Streaming ({})".format(i), montage)

            # if current time *minus* last time when the active device check
            # was made is greater than the threshold set then do a check
            if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
                # loop over all previously active devices
                for (rpiName, ts) in list(lastActive.items()):
                    # remove the RPi from the last active and frame
                    # dictionaries if the device hasn't been active recently
                    if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
                        log.info("Lost connection to {}".format(rpiName))
                        lastActive.pop(rpiName)
                        frameDict.pop(rpiName)

                # set the last active check time as current time
                lastActiveCheck = datetime.now()

            # if the `q` key or ESC key is pressed, break from the loop
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                log.info('Exiting via cv2.waitKey')
                break
    except (KeyboardInterrupt, SystemExit):
        log.warning('Ctrl-C was pressed or SIGTERM was received.')
    except Exception as ex:  # traceback will appear in log
        log.exception('Unanticipated error with no Exception handler.')
    finally:
        if 'hub' in locals():
            imageHub.close()
        log.info('Exiting dashboard_jpg.py')
        sys.exit()


def start_logging(hub):
    log = logging.getLogger()
    handler = logging.handlers.RotatingFileHandler(hub.logfile,
                                                   maxBytes=99000, backupCount=995)
    formatter = logging.Formatter('%(asctime)s ~ %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    hub.log = log
    return log


if __name__ == '__main__':
    main()
    if imageHub is not None:
        imageHub.close()
    # do a bit of cleanup
    cv2.destroyAllWindows()
