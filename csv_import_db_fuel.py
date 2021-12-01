import pandas as pd
from app import app
from config import Config
# from csv_download import monday_data


def csv_read_to_sql():
    app.config.from_object(Config)
    # mo = monday_data()
    # filename = f'CSV_{mo}.csv'
    filename = 'CSV_151121.csv'
    read_sql = pd.read_sql('select date, uslp, usld, uslp_duty, usld_duty, uslp_vat, usld_vat from fuel_data',
                           con=Config.SQLALCHEMY_DATABASE_URI)
    read_data = pd.read_csv(filename, encoding='unicode_escape', skiprows=3, usecols=[0, 1, 2, 3, 4, 5, 6])
    headers = ["date", "uslp", "usld", "uslp_duty", "usld_duty", "uslp_vat", "usld_vat"]
    read_data.columns = headers

    diff = pd.concat([read_sql, read_data]).drop_duplicates(keep=False)
    print(diff)


csv_read_to_sql()
