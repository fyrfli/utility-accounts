from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime
import hashlib
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField, URLField, DateField, DecimalField, TelField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo

db = SQLAlchemy()
login = LoginManager()

class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')
    submit = SubmitField('login')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(128), unique = True)
    user_email = db.Column(db.String(128), unique = True)
    user_pass = db.Column(db.String())
    def set_password(self,password):
        self.user_pass = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.user_pass, password)
    def is_active(self):
        return True
    def is_authenticated(self):
        return self.authenticated
    def get_id(self):
        return self.user_id
    def is_anonymous(self):
        return False

class Utility(db.Model):
    __tablename__ = 'utilities'
    util_id = db.Column(db.Integer, primary_key = True)
    util_name = db.Column(db.String(124))
    util_site = db.Column(db.String(124))
    util_acct = db.Column(db.String(32))
    util_main = db.Column(db.String)
    util_alt = db.Column(db.String)
    util_hours = db.Column(db.String)
    util_amt = db.Column(db.Float)
    util_bdate = db.Column(db.String)
    util_ddate = db.Column(db.String)
    util_autopay = db.Column(db.Boolean)

class Utils(FlaskForm):
    util_id = DecimalField('id')
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

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

load_dotenv()
env = dotenv_values()

app = Flask(__name__)

app.config['SECRET_KEY'] = env['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + env['DB_NAME']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db.init_app(app)

with app.app_context():
    db.create_all()

login.init_app(app)
login.login_view = 'login'

# global vaiablies
the_year = date.today().year
logged_in = False

@app.route('/')
@login_required
def index():
    with app.app_context():
        user = User.query.all()
        utilities = Utility.query.all()
        return render_template('index.html', the_year=the_year, utils=utilities)

@app.route('/view/<int:id>', methods = ['POST', 'GET'])
def view(id):
    with app.app_context():
        util = db.get_or_404(Utility, id)
        return render_template('view.html', the_year=the_year, form_data=util)

@app.route('/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):
    with app.app_context():
        form = Utils()
        utils = db.get_or_404(Utility, id)
        if request.method == 'POST':
            utils.util_name  = request.form['util_name']
            utils.util_site  = request.form['util_site']
            utils.util_acct  = request.form['util_acct']
            utils.util_main  = request.form['util_main']
            utils.util_alt   = request.form['util_alt']
            utils.util_hours = request.form['util_hours']
            utils.util_amt   = request.form['util_amt']
            utils.util_bdate = request.form['util_bdate']
            utils.util_ddate = request.form['util_ddate']
            if request.form['util_autopay'] == 'y':
                utils.util_autopay = True
            else:
                utils.util_autopay = False
            db.session.commit()
            return redirect(url_for('index'))
        else:
            form.process(formdata=None, obj=utils)
            return render_template('edit.html', the_year=the_year, form_data=form)

@app.route('/add', methods = ['POST', 'GET'])
def add():
    form = Utils()
    utils = Utility()
    with app.app_context():
        if request.method == 'POST':
            utils.util_name  = request.form['util_name']
            utils.util_site  = request.form['util_site']
            utils.util_acct  = request.form['util_acct']
            utils.util_main  = request.form['util_main']
            utils.util_alt   = request.form['util_alt']
            utils.util_hours = request.form['util_hours']
            utils.util_amt   = request.form['util_amt']
            utils.util_bdate = request.form['util_bdate']
            utils.util_ddate = request.form['util_ddate']
            if request.form['util_autopay'] == 'y':
                utils.util_autopay = True
            else:
                utils.util_autopay = False
            db.session.add(utils)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('add.html', the_year=the_year, form_data=form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
     
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(user_email = email).first()
        print(user.user_name, user.user_pass, request.form['password'])
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
     
    return render_template('login.html', login_form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='5000', debug=True)

