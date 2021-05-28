"""
plates/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField)
from wtforms.validators import DataRequired


class LicensePlatesForm(FlaskForm):
    license = StringField('license', validators=[DataRequired()])
    color = StringField('color', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
    identified = StringField('identified', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LicensePlatesLookupForm(FlaskForm):
    license = SelectField('license', validators=[DataRequired()], choices=[])
    submit = SubmitField('Submit')

