from src.db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    # When we set lazy='dynamic', self.items is no longer a list,
    # but a query builder. So we need to call self.items.all()
    # to perform a query and get a list of items.
    # This means that we create stores faster (because we do not
    # access items table at this point. But on the other hand,
    # we need to make a query every time we call json() method.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """Returns JSON representation of the model"""
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        """Searches the DB for an object by it's name. Returns an object or None"""
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()