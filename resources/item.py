from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


# create a resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help='must be filled'
    )

    # get request
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return {'name':item['name'], 'price':item['price']}
        return {'message':'item not found'}

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        con.close()

        if row:
            return {'name':row[0], 'price':row[1]}
        else:
            return None

    # @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        if Item.find_by_name(name):
            return {'message': f'{name} all ready exist'}, 400
        else:
            item = {'name': name, 'price': data['price']}
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            query = "INSERT INTO items VALUES(?,?)"
            cursor.execute(query, (item['name'], item['price']))
            con.commit()
            con.close()

            return item, 201
    
    # @jwt_required()
    def delete(self, name):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        con.commit()
        con.close()
        return {
            'message':f'{name} has been deleted'
        }

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        if item is None:
            item = {'name':name, 'price':data['price']}
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            query = "INSERT INTO items VALUES(?,?)"
            cursor.execute(query, (item['name'], item['price']))
            con.commit()
            con.close()
        else:
            item.update(data)
            con = sqlite3.connect('data.db')
            cursor = con.cursor()
            query = f"UPDATE items SET price='{item['price']}' WHERE name='{name}'"
            cursor.execute(query)
            con.commit()
            con.close()

        
        return item

class ItemList(Resource):
    def get(self):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = "SELECT * FROM items"
        rows = cursor.execute(query)
        if rows:
            list_item = []
            for row in rows:
                list_item.append({'name':row[0], 'price':row[1]})
            return {'items':list_item}
        return {'message': 'items not found'}
        con.close()