from app import db

class Fuel_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, unique=True)
    ULSP = db.Column(db.Float)
    ULSD = db.Column(db.Float)
    ULSP_duty = db.Column(db.Float)
    ULSD_duty = db.Column(db.Float)
    ULSP_vat = db.Column(db.Float)
    ULSD_vat = db.Column(db.Float)

