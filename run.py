from src.app import app
from src.db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()  # Creates DB with required tables (don't forget to import corresponding Resources)
