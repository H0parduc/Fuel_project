import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # OS Enterprise variable Set/export  DATABASE_URL = mysql://username:password@localhost:3306/db_fuel
    SECRET_KEY = 'q1w2w3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
