from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests
import debugpy
import os

# import the InceptionV3 model from keras app model
from keras.applications import InceptionV3
# imports preprocess_input - specifice to v3 model
from keras.applications.inception_v3 import preprocess_input
# used for decoding the predictions
from keras.applications import imagenet_utils
# it converts the PIL image, which is the Python image library image instance. So, the image that we have, we will be converting into PIL instance and it helps us convert this to a numpy array and which can be given as an input to the deep learning model
from tensorflow.keras.preprocessing.image import img_to_array
# this library provides us with the capability to working with images (resize,open etc)
from PIL import Image
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
    

def verify_credentials(username,password):
    if not user_exists(username):
        return generate_return_dictionary(301,"Invalid Username"),True
    
    correct_pw=verify_pw(username,password)

    if not correct_pw:
        return generate_return_dictionary(302,"Invalid Password"),True
    
    # if nothing matches
    return None,False
    
def verify_pw(username,password):
    if not user_exists(username):
        return False
    hashed_pw=users.find({
        "Username":username
    })[0]["Password"]
    
    if bcrypt.hashpw(password.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else:
        return False


def generate_return_dictionary(status,msg):
    ret_json={
        "status":status,
        "msg":msg
    }
    return ret_json


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
        # Load Image from URL
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        # Pre process the image for Inception V3 model
        img = img.resize((299,299))
        # convert to numpy array
        img_array = img_to_array(img)
        # set axis value of the model
        img_array = np.expand_dims(img_array,axis=0)
        # pre process the image
        img_array = preprocess_input(img_array)

        # Make Prediction
        # We have the preprocessed image which we fed to the pre-trained inception model and the prediction is made and it is stored in this prediction object
        prediction = pretrained_model.predict(img_array)
        # so there might be a lot of probabilities on the image. So, if you pass an image of a ball, it might be like it's a ball, it's an apple, it looks resembles like pineapple, it's an orange, so there will be like a lot of thousand probabilities. And these probabilities correspond to those many number of classes in the ImageNet database. So for every probability, there is a class. So for example, if it's a dog, the probability is a dog, then there's a class representing the dog. And then these probabilities are decoded into human readable class labels using the decode prediction,
        actual_prediction=imagenet_utils.decode_predictions(prediction,top=5)
            
        # return classification response
        ret_json = {}
        for pred in actual_prediction[0]:
            ret_json[pred[1]] = float(pred[2]*100)

        # reduce token
        users.update_one({
            "Username":username
        },{
            "$set":{
                "Tokens":tokens-1
            }
        })
        print("users",users)
        return jsonify(ret_json)

class Refill(Resource):
    def post(self):
        # get posted data
        posted_data=request.get_json()

        # get credentials
        username=posted_data["username"]
        password=posted_data["password"]
        amount=posted_data["amount"]

        # check if user exists
        if not user_exists(username):
            return jsonify(generate_return_dictionary(301,"Invalid Username"))
        
        # check admin password
        correct_pw="abc123"
        if not password==correct_pw:
            return jsonify(generate_return_dictionary(302,"Invalid Password"))

        # update the token and respond
        users.update_one({
            "Username":username
        },{
            "$set":{
                "Tokens":amount
            }
        })
        return jsonify(generate_return_dictionary(200,"Refilled"))

api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
# if os.getenv("ENABLE_DEBUGPY", "false") == "true":
#     debugpy.listen(('0.0.0.0', 5678))
#     print("⏳ Waiting for debugger attach...")
#     debugpy.wait_for_client()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)