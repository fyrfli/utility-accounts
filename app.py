from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, TextAreaField, RadioField, EmailField, PasswordField, SubmitField, HiddenField, URLField, DateField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from dotenv import load_dotenv, dotenv_values
from flask_login import LoginManager
from datetime import date, datetime
import hashlib

load_dotenv()
configs = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = configs['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + configs['DB_NAME']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# Define database models
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(64))
    user_pass = db.Column(db.String(128))
    user_name = db.Column(db.String(64))
    def is_active(self):
        return True
    def get_id(self):
        return self.user_name
    def is_anonymous(self):
        return False

class Utility(db.Model):
    __tablename__ = 'utility'
    util_id = db.Column(db.Integer, primary_key = True)
    util_name = db.Column(db.String(124))
    util_website = db.Column(db.String(248))
    util_accountno = db.Column(db.String(32))

class Bills(db.Model):
    __tablename__ = 'bills'
    util_id = db.Column(db.Integer, db.ForeignKey('utility.util_id'))
    bill_id = db.Column(db.Integer, primary_key = True)
    bill_date = db.Column(db.DateTime)
    bill_amount = db.Column(db.Float)

# forms
class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('login')

@app.before_first_request
def create_db():
    db.create_all()
    user = User.query.get(configs['ADMIN_USERNAME'].data)
    if user:
        return login()
    else:
        user.user_name = configs['ADMIN_USERNAME']
        user.user_email = configs['ADMIN_EMAIL']
        user.user_pass = hashlib.sha256(configs['ADMIN_PASSWORD'].encode()).hexdigest()
        db.session.add(user)
        db.session.commit()

#@app.user_loader
#def user_loader(user_id):
#    return User.query.get(user_id)

# global vaiablies
the_year = date.today().year
logged_in = False

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if hashlib.sha256(form.password.encode()).hexdigest() == user.user_pass:
                login_user(user, remember=True)
                logged_in = True
                return redirect(url_for("index"))
            else:
                flask.flash('Wrong password')
                return login()
        else:
            flask.flash('Wrong username')
            return login()
    return render_template('login.html', login_form=form, the_year=the_year)

@app.route("/logout", methods=["GET"])
def logout():
    user = current_user
    logout_user()
    logged_in = False
    return render_template("logout.html")

@app.route('/')
def index():
    if logged_in:
        return render_template('index.html', the_year=the_year)
    else:
        return login()

