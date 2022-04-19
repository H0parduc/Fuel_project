import pandas as pd
from app import db
from config import Config
from app.models import Fuel_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_fuel_reading():

    db_connection = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    rs = db.Query(Fuel_data)
    df = pd.read_sql(str(rs), con=db_connection)
    return df


def create_session():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(engine)
    session = Session()
    return session

