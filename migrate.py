from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv, dotenv_values
import models

load_dotenv()
env = dotenv_values()

app = Flask(__name__)
app.config['SECRET_KEY'] = env['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + env['DB_NAME']
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = models.SQLAlchemy(app)
migrate = Migrate(app, db, command='migrate')
