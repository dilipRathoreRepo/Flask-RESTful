from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import identify, authenticate
from user import UserRegister
from items import Item, Items

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identify) #/auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000)
