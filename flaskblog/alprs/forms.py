"""
alprs/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     BooleanField, FloatField, DateTimeField)
from wtforms.validators import DataRequired


class AlprEventsForm(FlaskForm):
    license_id = SelectField('license_id', validators=[DataRequired()], choices=[])
    datetime = DateTimeField('datetime', validators=[DataRequired()], render_kw={'readonly': True})
    image_id = StringField('image_id', validators=[DataRequired()], render_kw={'readonly': True})
    processing_time = FloatField('processing_time', validators=[DataRequired()])
    submit = SubmitField('Submit')


