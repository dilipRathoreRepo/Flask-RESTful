from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be blank")
    # data = parser.parse_args()

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_item(name)
        if item:
            return item.json()
        return {'message': 'No record found for item {}'.format(name)}

    def post(self, name):
        item = ItemModel.find_by_item(name)
        if item:
            return {'message': 'item already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred while inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_item(name)
        if item:
            item.delete_from_db()
        #     return {'message': 'item {} does not exists'.format(name)}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        return {'message': 'item is deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_item(name)
        # updated_item = ItemModel(name, data['price'])
        if item:
            item.price = data['price']
            # updated_item.update()
        else:
            item = ItemModel(name, data['price'])
            # updated_item.insert()
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

