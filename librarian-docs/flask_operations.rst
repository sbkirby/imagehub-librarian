==============
Flask Overview
==============
A Flask interface to `imagehub <https://github.com/jeffbass/imagehub>`_ to assist the management of cameras and the
images saved and catalogued by this application. This application provides access to the Object Detection feature,
as well as an Automated license plate reader (ALPR) if you wish to activate this feature.

.. image:: images/flask_home_page.jpg

.. contents::

Cameras
=======
Images for select Camera
------------------------
Select the camera you wish to display images.

.. image:: images/flask_select_camera.jpg

This is an **example** screen of the Cameras for my home installation.  Every installation of **Image Librarian** will contain
the ``Imagehub`` camera (DO NOT DELETE).  This "camera" is the Camera Node that all "system events" are associated with
in the ``imagehub`` application.

A page will appear with all of the images for that camera in descending order.  The number of images currently stored
will appear in parenthesis next to camera name.  Image may be clicked to enlarge, plus once enlarged the images may be
examined in order by pressing the arrow keys on your keyboard or on the screen.

.. image:: images/flask_images_from_select_camera.jpg

Images from all Cameras
-----------------------
This will display the images from all the cameras in descending order.

.. image:: images/Flask_View.jpg

Update Camera
-------------
Select a camera and update the parameters.  If any field needs updating, click the ``Update`` button and edit the camera
data and ``Submit``.  Camera entries may also be ``Deleted`` if necessary.

.. image:: images/flask_update_camera.jpg

Add Camera
----------
The ``NodeName`` is a descriptive name for the camera.  I choose to concatenate the ``node.name`` from the
``imagenode.yaml`` file with the ``cameras.P1.viewname`` (e.g. 'BirdFeeder' and 'RPiCam3').  The ``ViewName`` field
should match the ``cameras.P1.viewname`` field in the ``imagenode.yaml`` file as seen below::

   # Settings for imagenode.py webcam motion detector testing---
    node:
      name: BirdFeeder #  <-------
      queuemax: 20
      patience: 30
      #heartbeat: 1
      send_type: jpg
      send_threading: True  # sends images in separate thread
      threaded_read: False  # this is the new option; False selects PiCameraUnthreadedStream
      stall_watcher: True  # watches for stalled network or RPi power glitch
      print_settings: True
    hub_address:
      H1: tcp://10.0.0.210:5555
    cameras:
      P1:
        viewname: RPiCam3 #  <-------
        resolution: (800,600)
        exposure_mode: sports
        framerate: 30
        detectors:
          motion:
            ROI: (5,25),(95,85)
            draw_roi: ((255,0,0),1)
            send_frames: detected event # continuous or none or detected event
            send_count: 4 # number of images to send when an event occurs
            delta_threshold: 5 # The minimum intensity difference between the current image and the weighted average of past images
            min_motion_frames: 7 # The minimum number of frames with detected motion to change the state to "moving"
            min_still_frames: 4 # The minimum number of frames with no detected motion to change the state to "still"
            min_area: 2  # minimum area of motion as percent of ROI
            blur_kernel_size: 17  # Guassian Blur kernel size - integer and odd
            send_test_images: False
            print_still_frames: False  # default = True
            draw_time: ((0,255,0),1)
            draw_time_org: (5,5)
            draw_time_fontScale: 0.6

.. image:: images/flask_new_camera.jpg

Camera Event Logs
=================
Events for select Camera
------------------------
This option provides a look at the latest events for selected camera.  

.. image:: images/flask_select_camera.jpg

.. image:: images/flask_events_for_select_camera.jpg

Latest event for all active Cameras
-----------------------------------
This option will display the last event to occur for each camera.  This is handy for monitoring the last activity for all
cameras at one time.

.. image:: images/flask_latest_events_for_each_camera.jpg

License Plates
==============
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

Objects
=======
Images for select Objects
-------------------------
Select an Object to view all images for this object.

.. image:: images/flask_select_object.jpg
.. image:: images/flask_images_for_select_objects.jpg

Images for all Objects
----------------------
View images and update Object data for images.  Click the object link below the image to update object data.

.. image:: images/flask_all_image_objects.jpg

Update Object
-------------
Depricated

.. image:: images/flask_update_delete_object.jpg
.. image:: images/flask_update_object.jpg

Add Object
----------
Depricated

.. image:: images/flask_add_object.jpg
