from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparser
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.secret_key = 'keep it in ur pocket!'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return { 'item': item }, 200 if item else 404

    def post(self, name):
        foundItem = next(filter(lambda item: item['name'] == name, items), None)
        if (foundItem is not None):
             return { 'msg': "Item with name '{}' already exists!".format(name)}, 400
        data = request.get_json()
        item = { 'name': name, 'price': data['price'] }
        items.append(item)
        return item, 201 

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return { 'success': True }
        # todo: case name does not exist, return false

    def put(self, name):
        # parser = reqparser.RequestParser()
        # parser.add_argument('price',
        #     type=float,
        #     required=True,
        #     help="You need to provide price"
        # )
        # data = parse.parse_args()
        data = request.get_json()

        item = next(filter(lambda i: safe_str_cmp(i['name'], name), items), None)
        if (item is None):
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return { 'items': items }

@app.route('/')
def home():
    return 'homepage'

api.add_resource(Item, '/item/<string:name>')

api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)