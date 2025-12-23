from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource, fields, marshal_with

# created flask app and configured with with sqlite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialized database and API with configured flask app
db = SQLAlchemy(app)
api = Api(app)


# Created a database model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "User( name = {}, email = {})".format(self.name, self.email)


# This code ensures while creating user data should be as per the definitions
user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name should not be null")
user_args.add_argument("email", type=str, required=True, help="Email should not be null")


# Helps to defined the output structure with marshal_with decorator 
userfields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}


# Created resource for multiple user update
class Users(Resource):
    @marshal_with(userfields) # help to get back the data in specified format of uerfields
    def get(self):
        return UserModel.query.all(), 200

    @marshal_with(userfields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 200


# Created resource for single user update
class User(Resource):
    @marshal_with(userfields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    # patch will update the data by id value
    @marshal_with(userfields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, "User not found")
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user, 200

    @marshal_with(userfields)
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not fould")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 200   


# Adding new resources to API
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)