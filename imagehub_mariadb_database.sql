-- Adminer 4.8.0 MySQL 5.5.5-10.4.19-MariaDB-1:10.4.19+maria~bionic-log dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `imagehub` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `imagehub`;

CREATE TABLE `alpr_events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `license_id` int(11) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `image_id` varchar(75) COLLATE utf8mb4_unicode_ci NOT NULL,
  `processing_time` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `image_id` (`image_id`),
  KEY `license_id` (`license_id`),
  CONSTRAINT `alpr_events_ibfk_2` FOREIGN KEY (`image_id`) REFERENCES `images` (`image`),
  CONSTRAINT `alpr_events_ibfk_3` FOREIGN KEY (`license_id`) REFERENCES `license_plates` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `camera_nodes` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `NodeName` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ViewName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `CameraType` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Display` tinyint(4) unsigned zerofill NOT NULL,
  `Chk_Objects` tinyint(4) unsigned zerofill NOT NULL,
  `ALPR` tinyint(4) unsigned zerofill NOT NULL,
  `ROI_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Message` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Twilio_Enabled` tinyint(4) unsigned zerofill NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `camera_nodes` (`ID`, `NodeName`, `ViewName`, `CameraType`, `Display`, `Chk_Objects`, `ALPR`, `ROI_name`, `Message`, `Twilio_Enabled`) VALUES
(1,	'Imagehub',	'Imagehub',	'None',	0000,	0000,	0000,	'',	'',	0000);

CREATE TABLE `events` (
  `datetime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE current_timestamp(),
  `hubEvent` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `camera_id` int(10) unsigned NOT NULL,
  `Event` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Value` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ROI_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`hubEvent`),
  KEY `camera_id` (`camera_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`camera_id`) REFERENCES `camera_nodes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `images` (
  `datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `image` varchar(75) COLLATE utf8mb4_unicode_ci NOT NULL,
  `camera_id` int(10) unsigned NOT NULL,
  `ViewName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`image`),
  KEY `camera_id` (`camera_id`),
  CONSTRAINT `images_ibfk_1` FOREIGN KEY (`camera_id`) REFERENCES `camera_nodes` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `image_objects` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp(),
  `image_id` varchar(75) COLLATE utf8mb4_unicode_ci NOT NULL,
  `object_id` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `image_object_index` (`image_id`,`object_id`),
  KEY `object_id` (`object_id`),
  CONSTRAINT `image_objects_ibfk_3` FOREIGN KEY (`image_id`) REFERENCES `images` (`image`),
  CONSTRAINT `image_objects_ibfk_4` FOREIGN KEY (`object_id`) REFERENCES `objects` (`ObjectName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `license_plates` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `license` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `identified` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `license` (`license`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `objects` (
  `ID` int(11) NOT NULL,
  `ObjectName` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ObjectName` (`ObjectName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `objects` (`ID`, `ObjectName`) VALUES
(6,	'bicycle'),
(1,	'bird'),
(7,	'bus'),
(5,	'car'),
(3,	'cat'),
(2,	'dog'),
(8,	'motorbike'),
(4,	'person'),
(9,	'truck');

CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_posted` datetime NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_file` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 2021-05-28 13:50:21
