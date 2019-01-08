from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'klucz'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

items = []

class Item(Resource):
    """Klasa odpowiedzialna za pojedyńczy przedmiot"""

    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    @jwt_required() #dekorator mówiący o potrzebie uzyskania klucza JWT
    def get(self, item_id):
        """Funkcja wypełniająca żądanie GET pokazująca liste przemiotów"""
        item = next(filter(lambda x: x['ID'] == item_id, items), None)
        return {'Item': item}, 200 if item else 404

    def post(self, item_id):
        """Funkcja wypełniająca żądanie POST tworząca nowy przedmiot"""
        if next(filter(lambda x: x['ID'] == item_id, items), None):
            return {'message': "An item with ID '{}' already exists.".format(item_id)}, 404

        request_data = Item.parser.parse_args()

        item = {
            'ID': item_id,
            'name': request_data['name'],
            'price': request_data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, item_id):
        """Funkcja wypełniająca żądanie DEL usuwająca przedmiot"""
        global items
        items = list(filter(lambda x: x['ID'] != item_id, items))
        return {'message': 'Item deleted'}

    def put(self, item_id):

        request_data = Item.parser.parse_args()

        while True:

            item = next(filter(lambda x: x['ID'] == item_id, items), None)

            if item['name'] != None:
                if item is None:
                    item = {
                        'ID': item_id,
                        'name': request_data['name'],
                        'price': request_data['price']
                    }
                    items.append(item)
                else:
                    item.update(request_data)
                return item, 201
                break
            else:
                if next(filter(lambda x: x['ID'] == item_id, items), None):
                    request_data['name'] = item['name']
                else:
                    return {'message': "An item with ID '{}' does not exist, if you want create an item the name argument need to be fill"}

class ItemList(Resource):
    """Klasa odpowiadająca za listę przedmiotów"""
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(ItemList, '/items')

app.run(port=8000)
