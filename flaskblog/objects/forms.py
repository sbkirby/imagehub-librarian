"""
objects/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField,
                     BooleanField, FloatField, DateTimeField,
                     SelectField)
from wtforms.validators import DataRequired


class ObjectsForm(FlaskForm):
    ID = IntegerField('ID', validators=[DataRequired()])
    ObjectName = StringField('ObjectName', validators=[DataRequired()])
    submit = SubmitField('Submit')
