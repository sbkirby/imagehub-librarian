"""
cameras/forms.py

Copyright (c) 2021 by Stephen B. Kirby.
License: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class CameraNodesForm(FlaskForm):
    NodeName = StringField('NodeName', validators=[DataRequired()])
    ViewName = StringField('ViewName', validators=[DataRequired()])
    CameraType = StringField('CameraType', validators=[DataRequired()])
    Display = BooleanField('Display')
    Chk_Objects = BooleanField('Check Objects')
    ALPR = BooleanField('ALPR')
    ROI_name = StringField('ROI_name')
    Message = StringField('Message')
    Text_Enabled = BooleanField('Text Enabled')
    submit = SubmitField('Submit')

