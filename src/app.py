from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from src.resources.item import Item, ItemList
from src.resources.user import UserRegister
from src.resources.store import Store, StoreList
from src.security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
# Turn off flask-sqlalchemy modification tracker
# sqlalchemy mod tracker will work instead, which is faster
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'  # in production, we will use a secure key.
api = Api(app)


# Uncomment this for local testing
# @app.before_first_request
# def create_tables():
#     db.create_all()  # Creates DB with required tables (don't forget to import corresponding Resources)

# Initialize JWT object with our app and authentication and identity handlers
jwt = JWT(app, authenticate, identity)  # creates a new endpoint /auth


# Add resources to our api and provide routes
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # This means that the following statement will run only if we run this file
    # It won't run if we import it elsewhere
    from src.db import db  # import db here to prevent circular import
    db.init_app(app)
    app.run(debug=True)
