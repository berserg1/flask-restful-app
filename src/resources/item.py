from flask_restful import Resource, reqparse
# Resource is an object that rest api is working with
# Resources are usually mapped to databases
# Every resource has to be a class
# reqparse is used for parsing requests (parser can be used both with json and form data)
from flask_jwt import jwt_required

from src.models.item import ItemModel


# Create a resource
class Item(Resource):
    # Initialize a parses object to parse the request
    parser = reqparse.RequestParser()
    # Add arguments for our parser
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs store id")

    @jwt_required()  # This means that we need to authenticate to use this method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):  # The post method should have the same signature (params) within a single Resource
        if ItemModel.find_by_name(name):
            return {'message': "An item with a name '{}' already exists".format(name)}, 400  # 400 - bad request

        # Use parser with args that we've provided
        # Parser belongs to the class itself, so we are calling it with class Name
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred insering the item"}, 500  # 500 - internal server error

        return item.json(), 201  # Code for 'created'

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()  # Use parser with args that we've provided

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # with lambdas:
        # return {'items': list(map(lambda x: x.json, ItemModel.query.all()))}
