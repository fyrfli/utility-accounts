from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, TextAreaField, RadioField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class Users(FlaskForm):
    user_id 
