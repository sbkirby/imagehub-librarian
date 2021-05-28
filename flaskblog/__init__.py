#!/usr/bin/env python3
"""
__init__.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    from flaskblog.cameras.routes import cameras
    from flaskblog.alprs.routes import alprs
    from flaskblog.images.routes import images
    from flaskblog.plates.routes import plates
    from flaskblog.objects.routes import objects
    from flaskblog.imageobjs.routes import imageobjs
    from flaskblog.events.routes import events
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(cameras)
    app.register_blueprint(alprs)
    app.register_blueprint(images)
    app.register_blueprint(plates)
    app.register_blueprint(objects)
    app.register_blueprint(imageobjs)
    app.register_blueprint(events)
    return app
