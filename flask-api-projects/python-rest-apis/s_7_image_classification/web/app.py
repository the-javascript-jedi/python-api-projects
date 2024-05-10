from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

app = Flask(__name__)
api = Api(app)

#Initialize mongo db client
client = MongoClient("mongodb://db:27017")

# create a new db and collection
db = client.SimilarityDB
users = db["Users"]

# check if user exists in db
def user_exists(username):
    if users.count_documents({"Username":username})==0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        # we first get the posted data
        posted_data=request.get_json()
        # get user name and password
        username=posted_data["username"]
        password=posted_data["password"]

        # check if user already exists
        if user_exists(username):
            ret_json={
                "status":301,
                "message":"Invalid username,user already exists"
            }
            return jsonify(ret_json)

        # if user is new hash password
        hashed_pw=bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        # store the new user in db
        users.insert_one({
            "Username":username,
            "Password":hashed_pw,
            "Tokens":4
        })

        # return success
        ret_json={
                "status":200,
                "message":"You have successfully signed up for the API"
            }
        return jsonify(ret_json)
    

api.add_resource(Register,'/register')

