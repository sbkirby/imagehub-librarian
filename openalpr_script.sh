#!/bin/bash
# Start python scripts concurrently at docker opencv startup
cd /home/YOUR_HOME_DIRECTORY/IOTstack
# Start MQTT Client script
python3 mqtt_client.py &
# Start imagehub with path to imagehub.yaml
python3 /home/YOUR_HOME_DIRECTORY/IOTstack/imagehub/imagehub/imagehub.py -p /home/YOUR_HOME_DIRECTORY/IOTstack/imagehub
