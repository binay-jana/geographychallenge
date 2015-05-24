# geographychallenge
Setup:
- sudo apt-get install python-dev
- sudo apt-get install libmysqlclient-dev
- CREATE DATABASE challenge;
- pip install virtualenv
- Start a virtualenv directory in home directory
    virtualenv challenge
- load all the libraries in requirements.txt
    pip install -r requirements.txt
- start the app with: gunicorn -c gunicorn.conf.py start_app
- The app should be rendered in localhost:8000
