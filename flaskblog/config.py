"""
config.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
import os
import json


# read data from config file. json only
def load_config():
	# define Working Directory
	wrk_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
	with open(os.path.join(wrk_dir, 'config.json')) as json_data_file:
		return json.load(json_data_file)


# Read config.json file for settings
data = load_config()


class Config:
	SECRET_KEY = data["SECRET_KEY"]
	SQLALCHEMY_DATABASE_URI = data["SQLALCHEMY_DATABASE_URI"]
	SQLALCHEMY_POOL_RECYCLE = 550
	SQLALCHEMY_ECHO = True
	MAIL_SERVER = data["MAIL_SERVER"]
	MAIL_PORT = data["MAIL_PORT"]
	MAIL_USE_TLS = data["MAIL_USE_TLS"]
	MAIL_USERNAME = data["MAIL_USERNAME"]
	MAIL_PASSWORD = data["MAIL_PASSWORD"]
