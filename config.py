import os


class Config(object):
    # OS Enterprise variable Set/export  DATABASE_URL = mysql://username:password@localhost:3306/Fuel_data
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
