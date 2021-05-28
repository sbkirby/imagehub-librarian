"""
images/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField,
                     DateTimeField, SelectField)
from wtforms.validators import DataRequired


class ImagesSelectForm(FlaskForm):
    datetime = DateTimeField('datetime', render_kw={'readonly': True})
    image = StringField('image', validators=[DataRequired()], render_kw={'readonly': True})
    camera_id = SelectField('camera_id', validators=[DataRequired()], choices=[])
    ViewName = StringField('ViewName', validators=[DataRequired()])
    size = IntegerField('size', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ImagesForm(FlaskForm):
    datetime = DateTimeField('datetime')
    image = StringField('image', validators=[DataRequired()])
    camera_id = IntegerField('camera_id', validators=[DataRequired()])
    ViewName = StringField('ViewName', validators=[DataRequired()])
    size = IntegerField('size', validators=[DataRequired()])
    submit = SubmitField('Submit')

