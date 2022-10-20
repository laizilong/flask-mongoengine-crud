from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine

# Create an instance of the Flask app
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'user',
    'host': 'localhost',
    'port': 27017
}

# Create an instance of the mongo engine
db = MongoEngine()
db.init_app(app)

# Initialize the rest api instance
api = Api(app)


# Use the mongo engine to create a model of a mongodb collection
class User(db.Document):
    id = db.IntField(max_length=50, primary_key=True)
    name = db.StringField(max_length=50, required=True)
    age = db.IntField(max_length=50)


# Add the parser to be able to accept body{} content
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('age')


# Add or retrieve users to the mongodb collection
class UserList(Resource):
    def get(self):
        args = parser.parse_args()
        if args["id"] is None:
            user = User.objects.get(id=args["id"])
            return Response(user, mimetype="application/json", status=200)
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        args = parser.parse_args()
        user = User(id=args['id'], name=args["name"], age=args["age"]).save()
        id = user.id
        if id == user.id:
            return {"id": str(id), "message": "文档已添加"}, 200
        return {"message": "文档已存在"}

    def delete(self):
        args = parser.parse_args()
        if args["id"] is None:
            user = User.objects().delete()
        user = User.objects(id=args["id"]).delete()
        return {"message": "文档已删除 Deleted"}, 200

    def put(self):
        args = parser.parse_args()
        # user = User.objects(id=args["id"])
        # user.update(name=args['name'],age=args["age"])
        print(args)
        user = User.objects(id=args["id"])
        user.update(name=args["name"], age=args["age"])
        return {"message": "文档已更新 Updated"}, 200


# class UserOne(Resource):
#     def get(self, id):
#         user = User.objects.get(id=args["id"])
#         return Response(user, mimetype="application/json", status=200)


# Edit or delete the users
# class Users(Resource):
#     def put(self, name):
#         args = parser.parse_args()
#         user = User.objects(name=name)
#         user.update(age=args["age"])
#         return {"message": "文档已更新 Updated"}, 200
#
#     def delete(self, name):
#         args = parser.parse_args()
#         user = User.objects(name=name).delete()
#         return {"message": "文档已删除 Deleted"}, 200

# Add the resources (API endpoints)


api.add_resource(UserList, '/userlist')
# api.add_resource(UserOne, '/user/<id>')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)
