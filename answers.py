import pandas as pd
from app import db
from config import Config
from app.models import Fuel_data
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import ipychart as ipc

# ordered by date
db_connection = create_engine(Config.SQLALCHEMY_DATABASE_URI)
rs = db.Query(Fuel_data).order_by(Fuel_data.id.desc())
df = pd.read_sql(str(rs), con=db_connection)
df['date2'] = df['fuel_data_date'].str.replace("/", "")
df['date_norm'] = df['date2'].str[4:8] + df['date2'].str[2:4] + df['date2'].str[:2]
df['date_norm2'] = pd.to_datetime(df['date_norm'])
df = df.sort_values(by="date_norm2")


def last_record():
    l_record = df.tail(1)
    print(l_record)
    return l_record


def this_month_records():
    lstm_records = df.set_index('date_norm2').last('D')
    print(lstm_records)
    return lstm_records


def this_year_records():
    first_year_records = df.set_index('date_norm2').last('1Y')
    print(first_year_records)
    return first_year_records


def last_12_month_average_month():
    avg1 = df.groupby(pd.PeriodIndex(df['date_norm2'], freq='M'))['fuel_data_usld', 'fuel_data_uslp'].mean().tail(12)
    print(avg1)
    return avg1


def last_12_year_average():
    avg1 = df.groupby(pd.PeriodIndex(df['date_norm2'], freq='Y'))['fuel_data_usld', 'fuel_data_uslp'].mean().tail(12)
    avg1.to_json('Data\g12.json')
    avg1.plot()
    print(avg1)
    plt.show()
    # print(avg1)
    return avg1


last_12_year_average()
# last_record()
# this_month_records()
# this_year_records()
