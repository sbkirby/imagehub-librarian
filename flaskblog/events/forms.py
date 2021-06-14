"""
events/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     BooleanField, FloatField, DateTimeField,
                     IntegerField)
from wtforms.validators import DataRequired


class EventsForm(FlaskForm):
    datetime = DateTimeField('datetime')
    hubEvent = StringField('hubEvent', validators=[DataRequired()])
    camera_id = IntegerField('camera_id', validators=[DataRequired()])
    Event = StringField('Event', validators=[DataRequired()])
    Value = StringField('Value', validators=[DataRequired()])
    ROI_name = StringField('ROI_name', validators=[DataRequired()])
    submit = SubmitField('Submit')

