"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on our db for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
import bcrypt

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

# Register API
class Register(Resource):
    def post(self):
        # Step 1 is to get the posted data by the user
        postedData=request.get_json()

        #Got the data
        username = postedData["username"]
        password = postedData["password"]

        hashed_pw=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        # store username and password in SentencesDatabase
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Sentence":"",
            "Tokens":6
        })

        retJson = {
            "status":200,
            "msg":"You have successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username,password):
    # find the first username and return the password
    hashed_pw=users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf-8'),hashed_pw)==hashed_pw:
        return True
    else:
        return False
# return the no of tokens for the respective username
# return the first searched username
def countTokens(username):
    tokens=users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):

        #Step 1:get the posted data
        postedData = request.get_json()
        #Step 2: read the data from request
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3: Verify the username and password match
        correct_pw = verifyPw(username, password)
        # incorrect response
        if not correct_pw:
            retJson={
                "status":302
            }
            return jsonify(retJson)
        #Step 4:Verify if the user has enough tokens
        num_tokens=countTokens(username)
        if num_tokens<=0:
            retJson={
                "status":301
            }
            return jsonify(retJson)

        #Step 5: Store the sentence, take one token away and return 200
        users.update_one({
            "Username": username,
        },{
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
            }
        })
        retJson = {
            "status": 200,
            "msg": "Sentence saved successfully"
        }
        return jsonify(retJson)

api.add_resource(Register,'/register')
api.add_resource(Store,'/store')

# @app.route('/')
# def hello():
#     return "Hello, welcome to the API. Use /register or /store to interact."

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')

##################################################################################################
# from flask import Flask, jsonify, request
# from flask_restful import Api, Resource
# import os
#
# from pymongo import MongoClient
#
# app = Flask(__name__)
# api = Api(app)
#
# client = MongoClient("mongodb://db:27017")
# db = client.aNewDB
# UserNum = db["UserNum"]
#
# UserNum.insert_one({
#     'num_of_users':0
# })
#
# class Visit(Resource):
#     def get(self):
#         prev_num = UserNum.find({})[0]['num_of_users']
#         new_num = prev_num + 1
#         UserNum.update_one({}, {"$set":{"num_of_users":new_num}})
#         return str("Hello user " + str(new_num))
#
#
# def checkPostedData(postedData, functionName):
#     if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
#         if "x" not in postedData or "y" not in postedData:
#             return 301 #Missing parameter
#         else:
#             return 200
#     elif (functionName == "division"):
#         if "x" not in postedData or "y" not in postedData:
#             return 301
#         elif int(postedData["y"])==0:
#             return 302
#         else:
#             return 200
#
# class Add(Resource):
#     def post(self):
#         #If I am here, then the resouce Add was requested using the method POST
#
#         #Step 1: Get posted data:
#         postedData = request.get_json()
#
#         #Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "add")
#         if (status_code!=200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code":status_code
#             }
#             return jsonify(retJson)
#
#         #If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#
#         #Step 2: Add the posted data
#         ret = x+y
#         retMap = {
#             'Message': ret,
#             'Status Code': 200
#         }
#         return jsonify(retMap)
#
# class Subtract(Resource):
#     def post(self):
#         #If I am here, then the resouce Subtract was requested using the method POST
#
#         #Step 1: Get posted data:
#         postedData = request.get_json()
#
#         #Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "subtract")
#
#
#         if (status_code!=200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code":status_code
#             }
#             return jsonify(retJson)
#
#         #If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#
#         #Step 2: Subtract the posted data
#         ret = x-y
#         retMap = {
#             'Message': ret,
#             'Status Code': 200
#         }
#         return jsonify(retMap)
#
#
# class Multiply(Resource):
#     def post(self):
#         #If I am here, then the resouce Multiply was requested using the method POST
#
#         #Step 1: Get posted data:
#         postedData = request.get_json()
#
#         #Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "multiply")
#
#
#         if (status_code!=200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code":status_code
#             }
#             return jsonify(retJson)
#
#         #If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#
#         #Step 2: Multiply the posted data
#         ret = x*y
#         retMap = {
#             'Message': ret,
#             'Status Code': 200
#         }
#         return jsonify(retMap)
#
# class Divide(Resource):
#     def post(self):
#         #If I am here, then the resouce Divide was requested using the method POST
#
#         #Step 1: Get posted data:
#         postedData = request.get_json()
#
#         #Steb 1b: Verify validity of posted data
#         status_code = checkPostedData(postedData, "division")
#
#
#         if (status_code!=200):
#             retJson = {
#                 "Message": "An error happened",
#                 "Status Code":status_code
#             }
#             return jsonify(retJson)
#
#         #If i am here, then status_code == 200
#         x = postedData["x"]
#         y = postedData["y"]
#         x = int(x)
#         y = int(y)
#
#         #Step 2: Multiply the posted data
#         ret = (x*1.0)/y
#         retMap = {
#             'Message': ret,
#             'Status Code': 200
#         }
#         return jsonify(retMap)
#
#
#
# api.add_resource(Add, "/add")
# api.add_resource(Subtract, "/subtract")
# api.add_resource(Multiply, "/multiply")
# api.add_resource(Divide, "/division")
# api.add_resource(Visit, "/hello")
#
# @app.route('/')
# def hello_world():
#     return "Hello World!"
#
#
# if __name__=="__main__":
#     app.run(debug=True, host='0.0.0.0')
