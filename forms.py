from flask_wtf import FlaskForm

from wtforms import StringField, DateField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserForm(FlaskForm):
    username = StringField('User Name')
    password = StringField('Password')
    submit = SubmitField('Create User')