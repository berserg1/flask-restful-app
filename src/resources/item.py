from flask_restful import Resource, reqparse

from flask_jwt import jwt_required

from src.models.item import ItemModel


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

    def post(self, name):  # Methods should have the same signature (params) within a single Resource
        if ItemModel.find_by_name(name):
            return {'message': "An item with a name '{}' already exists".format(name)}, 400

        # Parser belongs to the class itself, so we are calling it with class Name
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred insering the item"}, 500

        return item.json(), 201  # Code for 'created'

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @staticmethod
    def get():
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # with lambdas:
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
