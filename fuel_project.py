from app import app, db
from app.models import Fuel_data


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Fuel_data': Fuel_data}
