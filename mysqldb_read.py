import pandas as pd
from app import app
from config import Config


def db_fuel_reading():
    app.config.from_object(Config)
    df = pd.read_sql('SELECT * FROM fuel_data', Config.SQLALCHEMY_DATABASE_URI)
    print(df)
