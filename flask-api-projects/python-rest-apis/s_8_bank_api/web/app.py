from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import debugpy


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db=client.BankAPI
users = db["Users"]

def UserExist(username):
    if users.find({"Username":username}).count()==0:
        return False
    else:
        return True
    
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson={
                "status":"301",
                "msg":"Invalid Username"
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        users.insert_one({
            "Username":username,
            "Password":hashed_pw,
            "Own":0,
            "Debt":0,
        })
        retJson={
                "status":"200",
                "msg":"You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username,password):
    if not UserExist(username):
        return False
    
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'),hashed_pw)==hashed_pw:
        return True
    else:
        return False

def cashWithUser(username):
    cash=users.find({
        "Username":username
    })[0]["Own"]
    return cash

def debtWithUser(username):
    cash=users.find({
        "Username":username
    })[0]["Debt"]
    return cash

def generateReturnDictionary(status,msg):
    retJson = {
        "status":status,
        "msg":msg
    }
    return retJson

#ErrorDictionary, True/False
def verifyCredentials(username,password):
    if not UserExist(username):
        return generateReturnDictionary(301,"Invalid Username"), True
    
    correct_pw = verifyPw(username,password)

    if not correct_pw:
        return generateReturnDictionary(302,"Invalid Password"), True
    return None, False

def updateAccount(username,balance):
    users.update_one({
        "Username":username
    },{
        "$set":{
            "Own":balance
        }
    })

def updateDebt(username,balance):
    users.update_one({
        "Username":username
    },{
        "$set":{
            "Debt":balance
        }
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)