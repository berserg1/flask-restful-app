from src.db import db


class UserModel(db.Model):
    # Object-relational mapping is created thanks to inheritance
    # from the Model base class class of SQLAlchemy object.
    __tablename__ = 'users'  # map this model to 'users' table

    # Map model fields to DB columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    # Object properties must be the same as model fields
    # in order to be saved to database
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
