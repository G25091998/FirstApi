import sqlite3
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="must be filled"
    )
    parser.add_argument('password',
    type=str,
    required=True,
    help="must be filled"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'username exists allredy'}, 400

        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        insert_query = "INSERT INTO users VALUES(NULL,?,?)"
        cursor.execute(insert_query, (data['username'], data['password']))
        con.commit()
        con.close()
        return {'message':'user register successfuly'}

