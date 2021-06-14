=================================
imagenode Installation Cheatsheet
=================================
The up to date instruction for **imagenode** are located at `https://github.com/jeffbass/imagenode <https://github.com/jeffbass/imagenode>`_.
Please check this site to verify these instructions are up to date.

.. contents::

Install Raspberry Pi OS
=======================
Download and install the latest version of `Raspberry Pi OS Lite <https://www.raspberrypi.org/software/operating-systems>`_.
I always use the instruction at `Overview | Raspberry Pi Zero Headless Quick Start <https://learn.adafruit.com/raspberry-pi-zero-creation?view=all>`_
to modify the SD cards for a quick and easy method of configuring and booting your RPis headlessly with WiFi.

raspi-config
============
Configure the Raspberry Pi (RPi) configuration as follows::

   sudo raspi-config

Perform the following changes within *raspi-config*.

- Modify ``System Options->Hostname`` to desired name
- Change ``System Options->Password``
- Enable ``Interface Options->Camera``
- Enable ``Interface Options->I2C`` (Optional)
- Enable ``Interface Options->SPI`` (Optional)
- Modify ``Localisation Options->Timezone`` to your Timezone
- Execute ``Advance Options->Expand Filesystem``
- Finish and Reboot

Update and Upgrade the RPi
==========================
Within the terminal::

    sudo apt-get update
    sudo apt-get upgrade

Git
===
Install Git::

   sudo apt-get install git

PIP
===
Install PIP::

   sudo apt-get install python3-pip

Virtual Environment
===================
Install and configure Virtual Environment::

    sudo pip3 install virtualenv virtualenvwrapper
    nano ~/.bashrc

At the end of the ``~/.bashrc`` file enter the following::

    # virtualenv and virtualenvwrapper
    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv
============
Exit the editor and execute the following::

    source ~/.bashrc
    mkvirtualenv cv -p python3

imagenode_requirements.txt
==========================
Making sure you are in the **cv** work environment, execute pip using the ``~/IOTstack/misc/imagenode_requirements.txt``
file::

   pip3 install -r imagenode_requirements.txt

Install Libraries
=================
The following libraries are needed for opencv-python version 4.4.0.46::

   sudo apt install libaec0 libaom0 libatk-bridge2.0-0 libatk1.0-0 libatlas3-base libatspi2.0-0 libavcodec58 libavformat58 libavutil56 libbluray2 libcairo-gobject2 libcairo2 libchromaprint1 libcodec2-0.8.1 libcroco3 libdatrie1 libdrm2 libepoxy0 libfontconfig1 libgdk-pixbuf2.0-0 libgfortran5 libgme0 libgraphite2-3 libgsm1 libgtk-3-0 libharfbuzz0b libhdf5-103 libilmbase23 libjbig0 libmp3lame0 libmpg123-0 libogg0 libopenexr23 libopenjp2-7 libopenmpt0 libopus0 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpixman-1-0 librsvg2-2 libshine3 libsnappy1v5 libsoxr0 libspeex1 libssh-gcrypt-4 libswresample3 libswscale5 libsz2 libthai0 libtheora0 libtiff5 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau1 libvorbis0a libvorbisenc2 libvorbisfile3 libvpx5 libwavpack1 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwebp6 libwebpmux3 libx264-155 libx265-165 libxcb-render0 libxcb-shm0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxinerama1 libxkbcommon0 libxrandr2 libxrender1 libxvidcore4 libzvbi0

Install imagenode
=================
Change Directory and Install **imagenode**::

    cd ~
    git clone https://github.com/jeffbass/imagenode.git

Configure imagenode
===================
Configure the service and YAML files::

    cd imagenode
    cp example.yaml ~/IOTstack/imagenode.yaml

Edit the imagenode.service file::

   nano imagenode.service

Modify the ``ExecStart=/home/pi/.virtualenvs/py3cv3/bin/python -u /home/pi/imagenode/imagenode/imagenode.py`` to match your
installation.  Replace the ``py3cv3`` with ``cv``.  Save and Exit and move the file::

    sudo cp imagenode.service /etc/systemd/system
    sudo systemctl enable imagenode.service

Edit the ``imagenode.yaml`` file to match your setup.  Instructions for configuring these files are located at
`imagenode Settings and the imagenode.yaml file <https://github.com/jeffbass/imagenode/blob/master/docs/settings-yaml.rst>`_.
Numerous examples of ``imagenode.yaml`` files are located at `YAML-rama <https://github.com/jeffbass/imagenode/tree/master/yaml>`_::

  cd ~/IOTstack
  nano imagenode.yaml

Once the ``imagenode.yaml`` has be modified to meet your needs::

  sudo systemctl start imagenode.service

The installation is complete

