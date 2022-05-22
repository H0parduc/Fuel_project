from app import db
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Fuel_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    uslp = db.Column(db.Float)
    usld = db.Column(db.Float)
    uslp_duty = db.Column(db.Float)
    usld_duty = db.Column(db.Float)
    uslp_vat = db.Column(db.Float)
    usld_vat = db.Column(db.Float)
