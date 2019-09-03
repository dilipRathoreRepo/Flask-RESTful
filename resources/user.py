import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}

        user = UserModel(**data)
        # user = UserModel(data['username'], data['password'])
        user.save_to_db()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        #
        # # print("username is {}, password is {}".format(data['username'], data['password']))
        # cursor.execute(insert_query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        return {"message": "User was created successfully"}, 201
