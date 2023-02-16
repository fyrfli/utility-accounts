#!/usr/bin/env python
from getpass import getpass
import sys
from hashlib import sha256
from werkzeug.security import generate_password_hash

from models import User, db
from app import app

from dotenv import load_dotenv, dotenv_values

load_dotenv()
env = dotenv_values()

def main():
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print ('Admin user already exists!')
            return

        user = User(
            user_name = env['ADMIN_USERNAME'],
            user_email = env['ADMIN_EMAIL'], 
            user_pass = generate_password_hash(env['ADMIN_PASSWORD'])
            )
        db.session.add(user)
        db.session.commit()
        print ('User added.')


if __name__ == '__main__':
    sys.exit(main())

