#!/bin/bash
# Start python scripts concurrently at docker opencv startup
cd /home/your_username/IOTstack
# Start MQTT Client script
python3 mqtt_client.py &
# Start imagehub with path to imagehub.yaml
python3 /home/your_username/IOTstack/imagehub/imagehub/imagehub.py -p /home/your_username/IOTstack/imagehub
