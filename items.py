from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be blank")
    # data = parser.parse_args()

    @classmethod
    def find_by_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {"name": row[0], "price": row[1]}}
        return None

    @jwt_required()
    def get(self, name):
        row = self.find_by_item(name)
        if row:
            return row
        return {'message': 'No record found for item {}'.format(name)}

    def post(self, name):
        row = self.find_by_item(name)
        if row:
            return {'message': 'item already exists'}, 400

        data = Item.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (name, data['price']))

        connection.commit()
        connection.close()

        return {'message': 'item successfully added'}, 201

    def delete(self, name):
        row = self.find_by_item(name)
        if not row:
            return {'message': 'item {} does not exists'.format(name)}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'item is deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES (?, ?)"
        update_query = "UPDATE items SET price = ? WHERE name = ?"
        row = self.find_by_item(name)
        if row:
            cursor.execute(update_query, (data['price'], name))
        else:
            cursor.execute(insert_query, (name, data['price']))
        connection.commit()
        connection.close()
        return {'message': 'operation successful'}


class Items(Resource):
    def get(self):
        pass
