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
the ``Imagehub`` camera (DO NOT DELETE).  This "camera" is the Camera Node that all system events are associated with
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

.. image:: images/flask_new_camera.jpg

Camera Event Logs
=================
Events for select Camera
------------------------

.. image:: images/flask_events_for_select_camera.jpg

Latest event for all active Cameras
-----------------------------------

.. image:: images/flask_latest_events_for_each_camera.jpg

License Plates
==============
Images for a License Plate
--------------------------
.. image:: images/flask_images_for_a_license_plate.jpg

.. image:: images/flask_images_for_a_license_plate_UNKNOWN.jpg

ALPR Images/Update
------------------
.. image:: images/flask_alpr_events.jpg

Update License Plate
--------------------
.. image:: images/flask_update_delete_license_plate.jpg
.. image:: images/flask_update_license_plate.jpg

Add License Plate
-----------------
.. image:: images/flask_add_license_plate.jpg

Objects
=======
Images for select Objects
-------------------------
.. image:: images/flask_select_object.jpg
.. image:: images/flask_images_for_select_objects.jpg
Images for all Objects
----------------------
.. image:: images/flask_all_image_objects.jpg
Update Object
-------------
.. image:: images/flask_update_delete_object.jpg
.. image:: images/flask_update_object.jpg
Add Object
----------
.. image:: images/flask_add_object.jpg
