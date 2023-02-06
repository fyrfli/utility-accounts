from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import DateTimeField, StringField, TextAreaField, RadioField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from dotenv import load_dotenv, dotenv_values
from flask_login import LoginManager

from app import models

load_dotenv()
configs = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = configs['SECRET_KEY']

db = SQLAlchemy(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':

