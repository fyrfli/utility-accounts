from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

db = SQLAlchemy()
login = LoginManager()

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

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
