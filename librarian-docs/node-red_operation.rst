==================================
Node-Red Settings and How it Works
==================================

.. contents::

Image Librarian
===============

tail imagehub.log
-----------------
**Node-Red** is the primary background application monitoring the operation of **imagehub** events and the storage
of images.  The ``tail imagehub.log`` node monitors the log file for events (e.g. 'motion', 'still', 'temperature',
'humidity', etc.).

.. image:: images/nodered_tail_imagehub.log.jpg

Example of JSON data from the ``tail imagehub.log`` node::

   {
   "topic":"/data/imagehub_data/logs/imagehub.log",
   "payload":"2021-06-07 08:41:01,130 ~ Backporch RPiCam5|motion|still|BackDoor",
   "_msgid":"7cc4638b.decf1c"
   }

tail payload parser
-------------------
All the events are parsed by the ``tail payload parser`` and stored in the ``events`` table of the ``imagehub`` database.
Example of the output of this node::

  {
  "topic":"INSERT INTO events VALUES (:datetime, :hubEvent, :camera_id, :Event, :Value, :ROI_name)",
  "payload":{
      "datetime":"2021-06-07 08:45:03",
      "hubEvent":"2021-06-07 08:45:03,087 ~ StreetView RPiCam6",
      "camera_id":1,
      "Event":"motion",
      "Value":"moving",
      "ROI_name":"FrontDoor",
      "Viewname":"RPiCam6"
      },
  "_msgid":"a0812019.83aa"
  }

CUSTOM: Check ROI's for Objects
-------------------------------
If for example, an event occurs in a specified *Region of Interest* (ROI) a customized event can be triggered to notify you
of this event via email and/or text message.  The ``CUSTOM: Check ROI's for Objects`` node screens events for cameras
with the ``ROI_name`` field defined in the ``camera_nodes`` table.  The ``roi_name`` must be defined and ``log_roi_name: True``
in the ``imagenode.yaml`` file.  The ``Message`` field of the ``camera_nodes`` table is used to specify the message sent
via email or text.  This **Node-Red** configuration is setup to notify audibly a *object* + *Message* (e.g. 'A person is
at the Front Door').

The ``7 seconds`` delay is there to provide enough time for the image data to be examined for objects and the results
stored in the database. Example of the ``CUSTOM: Check ROI's for Objects`` and results from ``imagehub DB`` query::

   {
   "topic":
      "SELECT COUNT(object_id), object_id
      FROM image_objects
      WHERE image_id LIKE \"%RPiCam5%\"
      AND (datetime >= \"2021-06-07 09:24:40\" AND datetime < \"2021-06-07 09:25:00\")
      AND object_id IN (\"person\",\"dog\",\"cat\")
      GROUP BY object_id",
   "payload":[{"COUNT(object_id)":1,"object_id":"person"}],
   "_msgid":"24f44d11.9af8b2",
   "trigger_audio":true,
   "trigger_twilio":false,
   "ROI_Message":"is at the backdoor"
   }

CUSTOM: Check for twilio trigger and/or CUSTOM: Check for audio trigger
-----------------------------------------------------------------------
Depending on which flags are set ``trigger_audio`` and/or ``trigger_twilio`` as to which node(s) are triggered, either
``CUSTOM: Check for twilio trigger`` and/or ``CUSTOM: Check for audio trigger``.  Note: This application does not require
Twilio...It was used at one time, and the variables remain to confuse me and you.

watch /data/imagehub_data/images
--------------------------------
Any changes to the ``images`` folder will trigger a *watch* event similar to the following::

   {
   "payload":"/data/imagehub_data/images/2021-06-07/Backporch-RPiCam5-2021-06-07T10.07.07.063070.jpg",
   "topic":"/data/imagehub_data/images",
   "file":"Backporch-RPiCam5-2021-06-07T10.07.07.063070.jpg",
   "filename":"/data/imagehub_data/images/2021-06-07/Backporch-RPiCam5-2021-06-07T10.07.07.063070.jpg",
   "size":24576,
   "type":"file",
   "_msgid":"efc2c3a1.bd67"
   }

Adding images to the ``imagehub`` database and checking for objects.

.. image:: images/nodered_watch_images.jpg

add image name to DB
--------------------
This node monitors the *watch* node, and if certain parameters pass the test a SQL call is configured to insert the
image data into the ``images`` table::

   {
   "payload":
      {
      "datetime":"2021-06-07 10:17:49.558968",
      "image":"Driveway-RPiCam7-2021-06-07T10.17.49.558968.jpg",
      "camera_id":8,
      "ViewName":"RPiCam7",
      "size":57344
      },
   "topic":"INSERT IGNORE INTO images VALUES (:datetime, :image, :camera_id, :ViewName, :size)",
   "file":"Driveway-RPiCam7-2021-06-07T10.17.49.558968.jpg",
   "filename":"/data/imagehub_data/images/2021-06-07/Driveway-RPiCam7-2021-06-07T10.17.49.558968.jpg",
   "size":57344,
   "type":"file",
   "_msgid":"e15ff849.3423c8"
   }

