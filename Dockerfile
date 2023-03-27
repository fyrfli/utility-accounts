from python:3.10-alpine

env PYTHONBUFFERED 1
env PYTHONWRITEBYTECODE 1

env APP_HOME=/home/app/web

# Create an app user in the app group. 
run adduser --disabled-password --home /home/app --shell /bin/bash app && mkdir -p $APP_HOME/staticfiles

# Change the workdir.
workdir $APP_HOME

copy requirements.txt $APP_HOME
run pip install --upgrade pip && pip install -r requirements.txt

copy . $APP_HOME
run chown -R app:app $APP_HOME

user app:app

entrypoint ["hypercorn", "-w", "2", "--bind", "127.0.0.1:8000", "--server-name","accounts.fyrf.li","app.py", "&"]