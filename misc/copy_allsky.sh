#!/bin/sh
# copy_allsky.sh
# navigate to home directory, then to this directory, then execute python script, then back home
cd /home/ftpuser/
sudo cp -up /home/ftpuser/allsky/keograms/*.* /home/YOUR_HOME_DIRECTORY/volumes/nodered/data/imagehub_data/ftp/allsky/keograms/
sudo cp -up /home/ftpuser/allsky/startrails/*.* /home/YOUR_HOME_DIRECTORY/volumes/nodered/data/imagehub_data/ftp/allsky/startrails/
sudo cp -up /home/ftpuser/allsky/videos/*.* /home/YOUR_HOME_DIRECTORY/volumes/nodered/data/imagehub_data/ftp/allsky/videos/
cd /
