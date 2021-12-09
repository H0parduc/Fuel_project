import pandas as pd
from sqlalchemy import create_engine
from app import db
from config import Config
from app.models import Fuel_data


def db_fuel_reading():

    db_connection = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    rs = db.Query(Fuel_data)
    df = pd.read_sql(str(rs), con=db_connection)
    # print(rs)
    print(df)


db_fuel_reading()
