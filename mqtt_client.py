#!/usr/bin/env python3
"""
mqtt_client.py - detect objects in images and preform ALPR on car images via Plate Recognizer account at
https://platerecognizer.com/

Edit JSON config.json file in work_dir defined below

Date: October 1, 2020
By: Stephen B. Kirby
"""

import sys
import os
import time
import paho.mqtt.client as mqtt
import json
import requests
import tools.detect_objects_cv2 as detect_objects

# client name
client_name = 'ObjDector'
transmit = True
current_status = True
# set DEBUG=True to print debug statements in Docker log file of openalpr container
DEBUG = True
# init client object
client = None
# define Home Directory
work_dir = os.path.join(os.path.dirname( __file__ ), os.pardir)
# ALPR regions for Plate Recognizer
regions = ['us-tx']
API_TOKEN = '****INSERT YOUR API TOKEN****'


# read data from config file. json only
def load_config():
    with open(os.path.join(work_dir, 'config.json')) as json_data_file:
        return json.load(json_data_file)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, *extra_params):
    global DEBUG
    if DEBUG:
        print('Connected with result code ' + str(rc))
    client.subscribe('image/#')  # SUB to all image messages


# PUBLISH data to server
def publish_message(topic, objs):
    global client
    if transmit:
        if topic == 'image/id_objects/count':
            client.publish(topic, objs, 1)
        if topic == 'image/alpr/results':
            client.publish(topic, objs, 1)
        time.sleep(0.01)


# Decode JSON data in payload
def decode_msg(msg):
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    return json.loads(m_decode)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global current_status, DEBUG
    if DEBUG:
        print("on_message payload: ", msg.payload)
    if msg.topic == 'image/id_objects/get_objects':
        if current_status:
            head, filename = os.path.split(msg.payload)  # separate filename from path
            if os.path.isfile(msg.payload):
                tmp = detect_objects.detectObject(msg.payload)
                tmp["filename"] = filename.decode('utf-8')  # filename key field
                tmp["isfile"] = True  # file exists
                objs = json.dumps(tmp, separators=(',', ':'))
                if DEBUG:
                    print('get_objects objs: ', objs)
                publish_message('image/id_objects/count', objs)
            else:
                # if file doesn't exist store result in image database
                tmp = {"filename": filename.decode('utf-8'), "isfile": False}
                objs = json.dumps(tmp, separators=(',', ':'))
                publish_message('image/id_objects/count', objs)
    if msg.topic == 'image/alpr/get_license':
        if current_status:
            # loop thru list of two images to read for license
            cnt = 0
            payload = json.loads(msg.payload)
            for img in payload['filename']:
                cnt += 1  # counter for test - publish & quit after second image
                # check to see file exist
                if DEBUG:
                    print('get_license cnt: ', cnt)
                if os.path.isfile(img):
                    # open file
                    with open(img, 'rb') as fp:
                        try:
                            # POST the image to Plate Recognizer website - 2500/month
                            response = requests.post(
                                'https://api.platerecognizer.com/v1/plate-reader/',
                                data=dict(regions=regions),  # Optional
                                files=dict(upload=fp),
                                headers={'Authorization': 'Token ' + API_TOKEN})
                        except NewConnectionError as err:
                            print('get_license Error: Failed to establish a new connection')
                            time.sleep(1)
                            break
                        if DEBUG:
                            print('get_license response.json: ', response.json())
                        results_str = json.dumps(response.json(), separators=(',', ':'))
                        # if results aren't empty publish data or second image
                        if (response.json()["results"] != []) or (cnt == 2):
                            publish_message('image/alpr/results', results_str)
                            break
                        time.sleep(1)
    if msg.topic == 'image/information':
        msg_data = decode_msg(msg)
        if DEBUG:
            print('image/information: ', msg_data)


# Logging
def on_log(client, userdata, level, buf):
    global DEBUG
    if DEBUG:
        print("on_log: ", buf)


# save the data, cleanup GPIO (if used) and exit
def clean_and_exit():
    time.sleep(0.1)
    sys.exit()  # exit python to system


def main():
    global client
    # wait 15 seconds for network to start
    if DEBUG:
        print("[INFO] Standby 10 seconds for things to start.")
    time.sleep(10)
    data = load_config()
    # mqtt connect
    client = mqtt.Client(client_name)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log
    client.username_pw_set(data['MQTT_USER'], password=data['MQTT_PW'])
    client.connect(data['OIP_HOST'], data['MQTT_PORT'], 60)
    time.sleep(0.5)
    try:
        client.loop_forever()
    except Exception as ex:
        if DEBUG:
            print('main(): Unanticipated error with no Exception handler.', ex)
        client.disconnect()
        clean_and_exit()


if __name__ == "__main__":
    main()
