from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import DateTimeField, StringField, TextAreaField, RadioField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from dotenv import load_dotenv, dotenv_values
from flask_login import LoginManager
from datetime import date, datetime

load_dotenv()
configs = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = configs['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/' + configs['DB_NAME']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

the_year = date.today().year

@app.route('/')
def index():
    return render_template('index.html', the_year=the_year)

