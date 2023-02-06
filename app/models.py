from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, TextAreaField, RadioField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class Users(FlaskForm):
    user_id Column(IntegerField, primary_key=True)
    user_name Column(StringField(64), InputRequired)
    user_email Column(EmailField(64), InputRequired)
    user_hash Column(StringField(128))
