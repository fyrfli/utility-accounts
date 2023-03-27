from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField, URLField, DateField, DecimalField, TelField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')
    submit = SubmitField('login')


class Utils(FlaskForm):
    util_name = StringField('name')
    util_site = URLField('website')
    util_acct = StringField('account')
    util_main = TelField('main telephone')
    util_alt = TelField('alt. telephone')
    util_hours = StringField('hours')
    util_amt = DecimalField('amount')
    util_bdate = StringField('bill date')
    util_ddate = StringField('due date')
    util_autopay = BooleanField('autopay?')
    submit = SubmitField('submit')
