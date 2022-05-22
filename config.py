import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # OS Enterprise variable Set/export  DATABASE_URL = mysql://username:password@localhost:3306/db_fuel
    SECRET_KEY = 'q1w2w3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_session():
    # from sqlalchemy.ext.declarative import declarative_base
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(engine)
    session = Session()
    # print(session)
    return session


create_session()
