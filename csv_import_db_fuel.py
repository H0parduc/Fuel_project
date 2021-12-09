import pandas as pd
from app import app, db
from config import Config
from app.models import Fuel_data
from csv_download import monday_data
# from csv_download import monday_data


def csv_read_to_sql():
    app.config.from_object(Config)
    mo = monday_data()
    records = db.Query(Fuel_data)
    filename = './Data/' + f'CSV_{mo}.csv'
    read_sql = pd.read_sql(str(records), con=Config.SQLALCHEMY_DATABASE_URI)
    read_data = pd.read_csv(filename, encoding='unicode_escape', skiprows=3, usecols=[0, 1, 2, 3, 4, 5, 6])
    headers = ["fuel_data_date", "fuel_data_uslp", "fuel_data_usld", "fuel_data_uslp_duty",
               "fuel_data_usld_duty", "fuel_data_uslp_vat", "fuel_data_usld_vat"]
    read_data.columns = headers
    read_data.insert(0, 'fuel_data_id', range(0, 0 + len(read_data)))
    diff = pd.concat([read_sql, read_data]).drop_duplicates(keep=False)
    diff.drop('fuel_data_id', inplace=True, axis=1)
    # print(diff)
    diff_headers = ["date", "uslp", "usld", "uslp_duty",
                    "usld_duty", "uslp_vat", "usld_vat"]
    diff.columns = diff_headers
    # print(diff)
    diff.to_sql('fuel_data', con=Config.SQLALCHEMY_DATABASE_URI, if_exists='append', chunksize=1000, index=False)

    # diff.to_csv('data.csv', header=True)

    # print(diff)


csv_read_to_sql()
