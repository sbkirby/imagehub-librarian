================================================================================================
imagehub-librarian: An Application for Receiving, Saving and Managing Images from Raspberry Pi's
================================================================================================

Introduction
============

The **imagehub-librarian** is a Docker based application using
Node-Red, MQTT, MariaDB and OpenCV containers along with the `imagehub <https://github.com/jeffbass/imagehub>`_
package from Jeff Bass to receive, save and manage images received
from Raspberry Pi's (RPi's). Containers of Grafana and
Flask are integrated into this application to monitor statistics, and
manage the hardware and images.

Here are a couple of images of the **imagehub-librarian** dashboards for viewing and managing the cameras and images
captured by **imagehub**:

.. image:: librarian-docs/images/Flask_View.jpg
    :width: 600px
    :height: 452px
    :align: center
    :alt: Example of Flask webpage
.. image:: librarian-docs/images/image_of_dashboard.png
    :width: 600px
    :height: 340px
    :align: center
    :alt: Example of Dashboard View

Additionally, this application is capable of detecting the objects of captured images.  If a 'car' is detected, this
application is capable of performing Automatic License Plate Recognition (ALPR) on the captured image.  All of the
object dection and ALPR data is stored in a relational database, and can be monitored in Grafana and the Flask
sections of **imagehub-librarian**.

.. contents::

Overview
========

Jeff Bass's **imagehub** application is the backbone of this application.  It is the "receive and store" part of a
distributed computer vision pipeline that is run on multiple computers. Multiple Raspberry Pi (and other) computers
run **imagenode** to capture images, detect motion, light, temperature values, etc. **Imagenode** then sends event
messages and selected images to **imagehub**, which files the events and images for later analysis.  Typically,
**imagehub** can manage up to 8 to 12 sending computers.

By design, **imagehub** is a very simple program. It does 2 things:

1. It receives images and stores them.
2. It receives event messages and logs them.

It does this from multiple sources simultaneously. The sources are typically a bunch of Raspberry Pi computers with
PiCameras and temperature sensors. Keeping **imagehub** simple allows it to be fast enough to reliably store data from
multiple sources. Analysis of images and responses to queries are handled by other programs. See `Using imagenode in
distributed computer vision projects <https://github.com/jeffbass/imagenode/blob/master/docs/imagenode-uses.rst>`_
for a more detailed explanation of the overall project design.

The **imagehub-librarian** provides a means of viewing and monitoring the log files and images saved
by **imagehub**.  Plus, it adds a means of object detection and ALPR for selected cameras.

imagehub-librarian Features
===========================

- Records the images and sensor events saved by **imagehub** in a database.
- Inspects the images for objects and records the results.
- Triggered events based on detected objects. For example, if a 'car' or 'truck' is detected, the image might be analyzed for a License Plate via ALPR.

Dependencies and Installation
=============================

**imagehub-librarian** has been tested with:

- ubuntu 20.04 LTS running on a BMAX Mini PC with Intel Celeron J4125, 8GB DDR4 and 500GB NVMe Internal SSD
- `imagehub <https://github.com/jeffbass/imagehub>`_ Version 0.2.0 - 2021-01-17
- `IOTstack <https://github.com/SensorsIot/IOTstack>`_ - on 2021-06-04

The **IOTstack** package provides the docker framework for the **imagehub-librarian**.  The librarian
builds two additional docker images, and provides the configuration files and instructions for
the **IOTstack** installed docker images.  To install **IOTstack**::

    sudo apt install -y curl git net-tools openssh-server htop apt-utils
    curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash

After executing the above lines. Change directory to IOTstack and execute the menu.sh shell file::

    cd ~/IOTstack
    ./menu.sh

This will install PIP and docker, and require a reboot.  Log in again and change directory to IOTstack
and execute the menu.sh again and select "Build Stack"::

    cd ~/IOTstack
    ./menu.sh
    Select "Build Stack"

Select the following images to build the stack::

    adminer
    mariadb
    mosquitto
    nodered
    portainer-ce

After the stack has been built, and the menu has been exited DO NOT START Docker.  There are a few task
to complete before Docker is started.  To insure your Docker has not started::

    cd ~/IOTstack
    docker-compose down

Install **imagehub** in the IOTstack folder. Note: Do not follow the **imagehub** installation instructions.  Imagehub will run from
a docker container. Therefore, the imagehub.service doesn't need to be configured and installed to run::

    cd ~/IOTstack
    git clone https://github.com/jeffbass/imagehub.git

Change the **imagehub** data_directory in the imagehub.yaml file to your Docker data location::

    nano imagehub/imagehub.yaml

Edit the data_directory field to match your installation. Change 'YOUR_HOME_DIRECTORY' to your username or folder name::

    data_directory: /home/YOUR_HOME_DIRECTORY/IOTstack/volumes/nodered/data/imagehub_data

At the time of this installation, Node-Red didn't allow for volumes outside of nodered/data path.  Hence,
the unusual imagehub_data location seen above.

Install the **imagehub-librarian** package.  The following will install these files into the IOTstack folder::

    cd ~
    git clone https://github.com/sbkirby/imagehub-librarian.git ~/IOTstack
    cd ~/IOTstack

Several task are required prior to starting Docker.  Edit the openalpr_script.sh and change
'YOUR_HOME_DIRECTORY' to the appropriate folder name::

    nano openalpr_script.sh

Make openalpr_script.sh executable::

    chmod +x openalpr_script.sh

Edit the 'config.json' file, and replace 'YOUR_HOME_DIRECTORY' to the appropriate folder name.  Configure
the email entries to match your email information ('MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_TLS', 'MAIL_USERNAME', 'MAIL_PASSWORD').
If a 'ALPR_API_TOKEN' is available from `Plate Recognizer <https://www.platerecognizer.com/>`_, enter it in the field::

    nano config.json

Build the OpenCV and Flask images::

    cd ~/IOTstack/docker
    docker build -f flask_Dockerfile -t flask:latest .
    docker build -f opencv_Dockerfile -t opencv:latest .

Rename the 'docker-compose.yml' file built by **IOTstack** and replace it with the file furnished by
**imagehub-librarian**::

    cd ~/IOTstack
    mv docker-compose.yml docker-compose_original.yml
    mv docker-compose_imagehub.yml docker-compose.yml

Edit the 'YOUR_HOME_DIRECTORY' folder locations for Flask and opencv in the NEW 'docker-compose.yml' file::

    nano docker-compose.yml

Tip: Pressing 'Ctrl + \\' in nano will allow for multiple finds and replaces.

Docker can be started::

    cd ~/IOTstack
    docker-compose up -d

All of the containers currently running can be seen via::

    docker ps -a

Configure Docker Images
-----------------------
Next, configure each of the docker containers with files furnished by **imagehub-librarian**.

MariaDB
^^^^^^^
Log into MariaDB via Adminer. Connect to `http://localhost:9080 <http://localhost:9080>`_ ::

    server: mariadb
    user: root
    password: IOtSt4ckToorMariaDb

Import database located in the 'misc' folder:
Import » "Choose Files" imagehub_mariadb_database.sql and "Execute"

.. image:: librarian-docs/images/mariadb_import_database.jpg

Setup privileges for user 'mariadbuser'
MySQL » mariadb » imagehub » Privileges » Create user::

	User: mariadbuser
	Password: IOtSt4ckmariaDbPw
	check 'All privileges'  `imagehub`.*

.. image:: librarian-docs/images/mariadb_privileges_create_user.jpg

Node-Red
^^^^^^^^
Log into Node-Red `http://localhost:1880 <http://localhost:1880>`_.  Go to the Menu->Manage palette->Install Tab->search modules, and install
modules 'node-red-contrib-stackhero-mysql' and 'node-red-node-email'.

.. image:: librarian-docs/images/nodered_manage_palette.jpg

Go to the Menu->Import->'select a file' to import the **imagehub-librarian** flow.
select file: ~/IOTstack/node-red/Image_Hub_Dashboard_flows.json

.. image:: librarian-docs/images/nodered_import_flow.jpg

Connect the data modules 'imagehub DB' nodes to MariaDB 'imagehub' Database::

    Host: mariadb
    Port: 3306
    User: mariadbuser
    Password: IOtSt4ckmariaDbPw
    Database: imagehub
    Name: imagehub

.. image:: librarian-docs/images/nodered_imagehub_DB_edit.jpg
.. image:: librarian-docs/images/nodered_imagehub_DB_Database_config.jpg

Grafana
^^^^^^^
Log into Grafana `http://localhost:3000 <http://localhost:3000>`_ ::

    username: admin
    password: admin
    change password if you wish or Skip

First, configure the database used by Grafana by going to menu Configuration -> Data Source::

    Data Service MySQL
    name: MySQL
    Host: mariadb
    Database: imagehub
    User: mariadbuser	Password: IOtSt4ckmariaDbPw
    save & test

.. image:: librarian-docs/images/grafana_database_config.jpg

Next, install a JSON configuration file, ALPR_Events-grafana.json located in the 'misc' folder, with charts and tables for the 'imagehub' database.
Go to menu Dashboards -> Manage::

    Import -> ALPR_Events-grafana.json
    Name: ALPR Events
    Folder: General
    MySQL: MySQL

.. image:: librarian-docs/images/grafana_import_dashboard.jpg

Flask
^^^^^
Before images are accessible from Flask, a link to the image folder must be created.  Change 'YOUR_HOME_DIRECTORY' to the
appropriate folder name::

    cd /home/YOUR_HOME_DIRECTORY/IOTstack/flaskblog/static
    ln -s /home/YOUR_HOME_DIRECTORY/IOTstack/volumes/nodered/data/imagehub_data imagehub_data

Log into Flask and create a user for yourself at `http://localhost:5000 <http://localhost:5000>`_.


Running imagehub-librarian
==========================

Docker
------

The Docker containers currently running can be monitored via the following command::

  docker ps -a

.. image:: librarian-docs/images/docker_ps_a.jpg

The Docker images created by IOTstack and imagehub-librarian can be seen via::

   docker images

.. image:: librarian-docs/images/docker_images.jpg

Additional documentation for **Docker** can be found at `Docker Reference documentation <https://docs.docker.com/reference/>`_.

Managing and controlling Docker is easily done with `Portainer-ce <http://localhost:9000/>`_.  Starting and Stopping
containers can conveniently be done with this application.

.. image:: librarian-docs/images/portainer.jpg

Imagehub
--------

The **imagehub** portion should be tested per the instructions at `imagehub - Running the Test <https://github.com/jeffbass/imagehub#running-the-tests>`_.
A typical **imagehub** installation and operation requires building a python enviroment and configuring and running
a service to run the application.  The **opencv** docker image contains the python enviroment, and runs the ``imagehub.py``
and ``mqtt_client.py`` within a container.  These two routines are required to operate **imagehub-librarian** properly.
Monitor the system resources and these routines via *htop*.

.. image:: librarian-docs/images/htop.jpg
    :width: 600px
    :height: 388px
    :align: center
    :alt: Make sure mqtt_client.py and imagehub.py are running

Monitoring the log files generated by **imagehub** will indicate most problems with this application::

    cat /home/YOUR_HOME_DIRECTORY/IOTstack/volumes/nodered/data/imagehub_data/logs/imagehub.log


Flask
-----

Flask is the web interface to the **imagehub-librarian**.  It provides a means of viewing images and monitoring the
sensor events of the network.


Running **imagehub-librarian** in production
==================================


Additional Documentation
========================
- `How imagehub works <docs/imagehub-details.rst>`_.
- `The imagehub Settings and the imagehub.yaml file <docs/settings-yaml.rst>`_.
- `Version History and Changelog <HISTORY.md>`_.
- `Research and Development Roadmap <docs/research-roadmap.rst>`_.
- `The imageZMQ classes that allow transfer of images <https://github.com/jeffbass/imagezmq>`_.
- `The imagenode program that captures and sends images <https://github.com/jeffbass/imagenode>`_.
- `The larger farm automation / computer vision project <https://github.com/jeffbass/yin-yang-ranch>`_.
  This project shows the overall system architecture. It also contains
  links to my **PyCon 2020** talk video and slides explaining the project.

Contributing
============


Acknowledgments
===============
- **ZeroMQ** is a great messaging library with great documentation
  at `ZeroMQ.org <http://zeromq.org/>`_.
- **PyZMQ** serialization examples provided a starting point for **imageZMQ**.
  See the
  `PyZMQ documentation <https://pyzmq.readthedocs.io/en/latest/index.html>`_.
