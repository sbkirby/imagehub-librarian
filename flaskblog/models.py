"""
models.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class CameraNodes(db.Model):
    __tablename__ = 'camera_nodes'
    ID = db.Column(db.Integer, primary_key=True)
    NodeName = db.Column(db.String(50), nullable=False)
    ViewName = db.Column(db.String(100), nullable=False)
    CameraType = db.Column(db.String(120), nullable=False)
    Display = db.Column(db.Boolean, nullable=False)
    Chk_Objects = db.Column(db.Boolean, nullable=False)
    ALPR = db.Column(db.Boolean, nullable=False)
    ROI_name = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Text_Enabled = db.Column(db.Boolean, nullable=False)
    images = db.relationship('Images', backref='camera', lazy=True)
    events = db.relationship('Events', backref='event', lazy=True)

    def __repr__(self):
        return f"CameraNodes('{self.NodeName}', '{self.ViewName}')"


class Events(db.Model):
    __tablename__ = 'events'
    datetime = db.Column(db.DateTime)
    hubEvent = db.Column(db.String(120), nullable=False, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera_nodes.ID'), nullable=False)
    Event = db.Column(db.String(120), nullable=False)
    Value = db.Column(db.String(120), nullable=False)
    ROI_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Events('{self.datetime}', '{self.hubEvent}', '{self.camera_id}')"


class LicensePlates(db.Model):
    __tablename__ = 'license_plates'
    ID = db.Column(db.Integer, primary_key=True)
    license = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    identified = db.Column(db.String(120), nullable=False)
    alprevent = db.relationship('AlprEvents', backref='licenseplates', lazy=True)

    def __repr__(self):
        return f"LicensePlates('{self.license}', '{self.color}', '{self.type}')"


class Objects(db.Model):
    __tablename__ = 'objects'
    ID = db.Column(db.Integer, primary_key=True)
    ObjectName = db.Column(db.String(120), nullable=False)
    imageobjects = db.relationship('ImageObjects', backref='objects', lazy=True)

    def __repr__(self):
        return f"Objects('{self.ObjectName}')"


class Images(db.Model):
    __tablename__ = 'images'
    datetime = db.Column(db.DateTime)
    image = db.Column(db.String(75), nullable=False, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera_nodes.ID'),nullable=False)
    ViewName = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    alprevent = db.relationship('AlprEvents', backref='images_alpr', lazy=True)
    imageobject = db.relationship('ImageObjects', backref='images_obj', lazy=True)

    def __repr__(self):
        return f"Images('{self.image}', '{self.ViewName}')"


class ImageObjects(db.Model):
    __tablename__ = 'image_objects'
    ID = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    image_id = db.Column(db.String(75), db.ForeignKey('images.image'), nullable=False)
    object_id = db.Column(db.String(120), db.ForeignKey('objects.ID'), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ImageObjects('{self.image_id}', '{self.object_id}', '{self.datetime}')"


class AlprEvents(db.Model):
    __tablename__ = 'alpr_events'
    ID = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(db.Integer, db.ForeignKey('license_plates.ID'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    image_id = db.Column(db.String(75), db.ForeignKey('images.image'), nullable=False)
    processing_time = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"AlprEvents('{self.license_id}', '{self.image_id}', '{self.datetime}')"
        
