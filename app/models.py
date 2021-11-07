from app import db

class Fuel_data(db.Model):
    id = db.Column(db.bigint, primary_key=True)
    date = db.Column(db.date, index=True, unique=True)
    ULSP = db.Column(db.float)
    ULSD = db.Column(db.float)
    ULSP_duty = db.Column(db.float)
    ULSD_duty = db.Column(db.float)
    ULSP_vat = db.Column(db.float)
    ULSD_vat = db.Column(db.float)

    def __repr__(self):
        return '<Fuel_db {}>'.format(self.date)