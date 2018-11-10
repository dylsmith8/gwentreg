import os
import markdown
import shelve
import uuid
import src.gwent_objects as gwent_objects
import src.request_helper as request_helper
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from urllib.parse import unquote

app = Flask(__name__)
api = Api(app)

def get_cards():
    kvp = getattr(g, '_database', None)
    if kvp is None:
        kvp = g._database = shelve.open("cards.db")
    return kvp

@app.teardown_appcontext
def teardown_kvp(exception):
    kvp = getattr(g, '_database', None)
    if kvp is not None:
        kvp.close()

def validate(argument, is_update, name):
    shelf = get_cards()

    # need to validate that the string is in fact an enum value
    # string get rid of these magic ints - Enum.Max or Enum.Min or something like that?
    card_type = argument['card_type']
    if card_type != 'null':
        card_type_value = gwent_objects.Type[card_type].value
        if card_type_value > 3 or card_type_value < 1:
            return {'message' : 'Error', 'data' : 'Card type ' + card_type + 'is not valid'}, 400

    faction = argument['faction']
    if faction != 'null':
        faction_value = gwent_objects.Faction[faction].value
        if faction_value > 5 or faction_value < 1:
            return {'message' : 'Error', 'data' : 'Card faction ' + faction + 'is not valid'}, 400

    row = argument['row']
    if row != 'null':
        row_value = gwent_objects.Row[row].value
        if row_value > 3 or row_value < 1:
            return {'message' : 'Error', 'data' : 'Row value ' + row + 'is not valid'}, 400

    if is_update:
        if not (name in shelf):
            return {'message' : 'Error', 'data' : 'Card with name ' + name + ' does not exist. update failed'}, 400

        shelf[name] = argument
        return {'message' : 'Card updated', 'data' : argument}, 200    

    # an addition
    if (name in shelf):
        return {'message' : 'Error', 'data' : 'Card with name ' + name + ' already exists'}, 400
    return add_card(argument)         

def add_card(argument):
    shelf = get_cards()
    shelf[argument['name']] = argument

    return {'message' : 'Card added', 'data' : argument}, 200

@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/readme.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)

class CardList(Resource):
    def get(self):
        shelf = get_cards()
        keys = list(shelf.keys())
        cards = []

        for key in keys:
            cards.append(shelf[key])

        return {'message' : 'success', 'data' : cards}

    def post(self):
        parser = reqparse.RequestParser()

        args = request_helper.helper.parse_request(parser)

        return validate(args, False, args['name'])        

class CardItem(Resource):
    def get(self, name):
        shelf = get_cards()    

        if not request_helper.helper.validate_card_name(shelf, name):
            return {'message' : 'card not found', 'data' : {}}, 404
        
        return {'message' : 'card found', 'data' : shelf[name]}, 200

    def delete(self, name):
        shelf = get_cards()

        if not request_helper.helper.validate_card_name(shelf, name):
            return {'message' : 'delete failed - card not found', 'data' : name}, 404

        current_card = shelf[name]
        quantity = current_card['quantity']

        q = int(quantity)

        if q > 0:
            q = q - 1
            if q == 0:
                del shelf[name]
            else:
                current_card['quantity'] = q
                shelf[name] = current_card        

        return {'message' : 'card deleted'}, 204
    
    def put(self, name):
        shelf = get_cards()

        if not request_helper.helper.validate_card_name(shelf, name):
            return {'message' : 'update failed - card not found', 'data' : shelf[name]}, 404
        
        parser = reqparse.RequestParser()
        args = request_helper.helper.parse_request(parser)

        return validate(args, True, name)
    
api.add_resource(CardList, '/cardlist')
api.add_resource(CardItem, '/carditem/<string:name>')