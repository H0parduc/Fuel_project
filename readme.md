Database settings
Crate a MySQL database db_fuel
set up an admin user for this database
Set/export  DATABASE_URL=mysql://username:password@localhost:3306/db_fuel

flask db init
environment variable set:
open .flaskenv file and FLASK_APP=fuelproject.py

flask db migrate -m "Fuel_data table"
flask db upgrade
Run app:
flask run

