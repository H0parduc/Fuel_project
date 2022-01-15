from mysqldb_read import db_fuel_reading
from app import app
from collections import Counter
from datetime import date, datetime
from math import ceil
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import render_template, request

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
SEPARATOR = "++"

engine = create_engine(DATABASE_URL)
session = sessionmaker(engine)()

metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()


def get_data(table, column):
    sa_table = getattr(Base.classes, table)
    col = getattr(sa_table, column)
    rows = session.query(col).all()
    cnt = Counter()
    for row in rows:
        attr = row[0]

        if attr is None:
            continue

        if isinstance(attr, (date, datetime)):
            attr = attr.strftime("%Y-%m")

        cnt[attr] += 1
    return sorted(cnt.items())


def calculate_max_height_graph(values):
    max_value = max(values)
    return int(ceil(max_value / 100.0)) * 100


@app.route('/')
def index():
    tables = sorted(Base.classes.keys())
    print(tables)
    return render_template("index.html", tables=tables)


@app.route('/columns')
def show_columns():
    table_str = request.args["table"]
    # table_str = request.args["fuel_data"]
    table = Base.classes.get(table_str)
    table_columns = {
        col: f"{table_str}{SEPARATOR}{col}" for col in
        table.__table__.columns.keys()
    }
    return render_template('_columns.html',
                           table_columns=sorted(table_columns.items()))


@app.route('/graph')
def build_graph():
    tcolumn = request.args["tcolumn"]
    table, column = tcolumn.split(SEPARATOR)
    data = get_data(table, column)
    labels, values = zip(*data)
    max_height = calculate_max_height_graph(values)
    return render_template('_graph.html',
                           labels=labels,
                           values=values,
                           max_height=max_height)


@app.route("/sp")
def sp():
    return "Hello word"


@app.route('/all_record', methods=("POST", "GET"))
def all_record():
    df = db_fuel_reading()
    return render_template('all_record.html', tables=[df.to_html(classes='Fuel_data')],
                           titles=df.columns.values, index=False)
