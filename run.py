# This file will be used for running the app on Heroku or Digital Ocean

from src.app import app
from src.db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
