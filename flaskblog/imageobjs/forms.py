"""
imageobjs/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField,
                     BooleanField, FloatField, DateTimeField,
                     SelectField)
from wtforms.validators import DataRequired


class ImageObjectsSelectForm(FlaskForm):
    ID = IntegerField('ID', validators=[DataRequired()])
    datetime = DateTimeField('datetime', validators=[DataRequired()], render_kw={'readonly': True})
    image_id = StringField('image_id', validators=[DataRequired()], render_kw={'readonly': True})
    object_id = SelectField('object_id', validators=[DataRequired()], choices=[])
    count = IntegerField('count', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ImageObjectsForm(FlaskForm):
    ID = IntegerField('ID', validators=[DataRequired()])
    datetime = DateTimeField('datetime', validators=[DataRequired()], render_kw={'readonly': True})
    image_id = StringField('image_id', validators=[DataRequired()], render_kw={'readonly': True})
    object_id = StringField('object_id', validators=[DataRequired()])
    count = IntegerField('count', validators=[DataRequired()])
    submit = SubmitField('Submit')
