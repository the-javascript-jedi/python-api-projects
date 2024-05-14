from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

# import the InceptionV3 model from keras app model
from keras.applications import InceptionV3
# imports preprocess_input - specifice to v3 model
from keras.applications.inception_v3 import preprocess_input
# used for decoding the predictions
from keras.applications import imagenet_utils
# it converts the PIL image, which is the Python image library image instance. So, the image that we have, we will be converting into PIL instance and it helps us convert this to a numpy array and which can be given as an input to the deep learning model
from tensorflow.keras.preprocessing.image import img_to_array
# this library provides us with the capability to working with images (resize,open etc)
from PIL import image
# this class provides a file like object interface for raw byte data. And what we are going to do with this is We are going to convert the content of an image received from the Http response into a stream that can be used as an input to PIL's image class.
from io import BytesIO


app = Flask(__name__)
api = Api(app)

#Load the pre trained model
pretrained_model = InceptionV3(weights="imagenet")

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
    
class Classify(Resource):
    def post(self):
        # Get posted data
        posted_data=request.get_json()
      
        # we get credentials and url
        username=posted_data["username"]
        password=posted_data["password"]
        url=posted_data["url"]

        # verify credentials
        ret_json,error=verify_credentials(username,password)
        if error:
            return jsonify(ret_json)

        # check if user has tokens
        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return jsonify(generate_return_dictionary(303, "Not Enough Tokens"))

        # classify the image
        if not url:
            return jsonify(({"error":"No url provided"}),400)       
        

        # return classification response

api.add_resource(Register,'/register')

