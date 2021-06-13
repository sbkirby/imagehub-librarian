================================================
Automated License Plate Reader (ALPR) Operations
================================================
The implementation of ALPR is accomplished with `PLATE RECOGNIZER <https://platerecognizer.com/>`_ software.  This
is currently a free product as long as you don't exceed 2,500 API calls in one month.  I live on a street that isn't
very busy, and I average between 35 - 70 entries per day in the ``alpr_events`` TABLE.

.. contents::

Installation
============
You will be required to ``Sign Up`` with ``PLATE RECOGNIZER`` in order to obtain an Account and ``API Token``.  The FREE
Account gives you access to their **Cloud API Plan**, which is what my application utilizes.  Once you're registered,
copy the ``API Token`` and put it into the "ALPR_API_TOKEN" field of ``config.json`` file located in the ``~/IOTstack`` folder.
Replace the "ALPR_regions" field in the file with your areas Region Code.  Refer to these codes in the
`Countries - ALPR API Documentation <https://docs.platerecognizer.com/#countries>`_::

   {
    "OIP_HOST": "mosquitto",
    "MQTT_USER": "admin",
    "MQTT_PW": "admin",
    "MQTT_PORT": 1883,
    "latest_images": "latest_images.json",
    "test_pattern": "RCA_Indian_Head_Test_Pattern_Dark.jpg",
    "imagehub_data": "/home/YOUR_HOME_DIRECTORY/IOTstack/volumes/nodered/data/imagehub_data",
    "ALPR_regions": ["us-tx", "us-la", "us-ca", "us-ok"],
    "ALPR_API_TOKEN": "your_ALPR_token",
    "purge_folders": "purge_folders.json",
    "SECRET_KEY": "5791628bb0b13ce0c676dfde280ba245",
    "SQLALCHEMY_DATABASE_URI": "mariadb+mariadbconnector://mariadbuser:IOtSt4ckmariaDbPw@mariadb/imagehub",
    "MAIL_SERVER": "smtp.someplace.net",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": true,
    "MAIL_USERNAME": "your_email_address@someplace.com",
    "MAIL_PASSWORD": "your_email_password"
    }

Cameras
=======
The location of the ALPR camera is critical. I recommend referring to `Camera Setup for Best ANPR <https://platerecognizer.com/camera-setup-for-best-anpr/>`_
for setting up your camera.

.. image:: images/RPi_4B_Case_with_HQ_Camera_Module.png

I am using the following equipment::

   Raspberry Pi 4 8GB
   Raspberry Pi HQ Camera Module
   35mm F1.6 APS-C Television TV Lens/CCTV Lens for 16mm C Mount Camera
   3D Printed Case - `Raspberry Pi 4B Case for HQ Camera Module <https://www.thingiverse.com/thing:4660741>`_
   `Adjustable Indoor/Outdoor Security Metal Wall Mount <https://www.amazon.com/gp/product/B06X6H8QDY>`_

I use the following ``imagenode.yaml`` settings for this camera::

    # Settings file imagenode.yaml -- example with lots of settings
    ---
    node:
      name: StreetView
      queuemax: 50
      patience: 30
      #heartbeat: 10
      send_type: jpg
      send_threading: True  # sends images in separate thread
      stall_watcher: False  # watches for stalled network or RPi power glitch
      print_settings: True
      REP_watcher: True
    hub_address:
      H1: tcp://10.0.0.100:5555
    cameras:
      P1:
        viewname: RPiCam4
        resolution: (1280,960)
        exposure_mode: sports
        shutter_speed: 1500
        framerate: 30
        threaded_read: False  # this is the new option; False selects PiCameraUnthreadedStream
        detectors:
          motion:
            ROI: (2,15),(98,95)
            #draw_roi: ((255,0,0),1)
            send_frames: detected event # continuous # or none or detected event
            send_count: 13
            delta_threshold: 7 # The minimum intensity difference between the current image and the weighted average of past images
            min_motion_frames: 9 # 9 -> 8 moving with send_count = 13
            min_still_frames: 6 # 7 -> 4 still
            min_area: 3  # minimum area of motion as percent of ROI
            blur_kernel_size: 21  # Guassian Blur kernel size - integer and odd
            send_test_images: False
            print_still_frames: False  # default = True
            draw_time: ((20,230,243),1)
            draw_time_org: (5,5)
            draw_time_fontScale: 1

I set the ``shutter_speed: 1500``, ``exposure_mode: sports`` and ``resolution: (1280, 960)`` to insure fast high resolution
images without blur.  The speed limit on street is 30 mph, and with these setting I get 7 - 8 images of each vehicle.  In
Texas vehicles 'usually' have a license plate on the front and rear of each vehicle.  As a vehicle approaches my camera
from the left I can see the license on the front of the car, but the license plate of vehicles approaching from the right
are not visible until 7th or 8th image.  Therefore, the application will send one image to the API, and if it fails it
will send another.  Currently, I send the 2nd and 7th image of a group of 8 images.  So far, I haven't exceeded my monthly
quota of API calls.  If my street were busier, I would need to rethink my strategy.

Flask ALPR Events
=================
Images for a License Plate
--------------------------
Select a License Plate of interest to see all the stored images for that plate.

.. image:: images/flask_images_for_a_license_plate.jpg

.. image:: images/flask_images_for_a_license_plate_UNKNOWN.jpg

ALPR Images/Update
------------------
Display all ALPR recorded events plus it provides a means of editing the ALPR event by clicking on the link below
each image.

.. image:: images/flask_alpr_events.jpg

Update License Plate
--------------------
This option provides a means of ``Updating`` and ``Deleting`` a License Plate in the database.  Great caution should
be taken in deleting entries in this Table since other Tables point to these entries.

.. image:: images/flask_update_delete_license_plate.jpg
.. image:: images/flask_update_license_plate.jpg

Add License Plate
-----------------
Add a License Plate.

.. image:: images/flask_add_license_plate.jpg

license
^^^^^^^
Enter the License Plate Number in Uppercase.

color
^^^^^
Enter the color of the vehicle.

type
^^^^
Enter the type of vehicle (e.g. car, suv, sedan, pickup truck, big truck, etc.).

identified
^^^^^^^^^^
Enter any identifying information in this field.

