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

class Add(Resource):
    def post(self):
        postedData=request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["money"]

        retJson,error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        
        if money<=0:
            return jsonify(generateReturnDictionary(304,"The money amount entered must be >0"))
        
        cash = cashWithUser(username)
        # deduct a transaction fee from the user
        money-=1
        bank_cash=cashWithUser("BANK")
        # add the transaction fee to bank
        updateAccount("BANK",bank_cash+1)
        updateAccount(username,cash+money)
        return jsonify(generateReturnDictionary(301,"Amount added successfully to account"))

class Transfer(Resource):
    def post(self):
        postedData=request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        money = postedData["money"]

        retJson,error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        
        cash = cashWithUser(username)
        if cash<=0:
            return jsonify(generateReturnDictionary(3004,"You are out of money please add or take a loan"))

        if not UserExist(to):
            return jsonify(generateReturnDictionary(301, "Receiver username is invalid"))
        
        # transaction fees
        cash_from=cashWithUser(username)
        cash_to=cashWithUser(to)
        bank_cash=cashWithUser("BANK")

        updateAccount("BANK",bank_cash+1)
        updateAccount(to,cash_to+money-1)
        # deduct money from user after transaction
        updateAccount(username+cash_from-money)

        return jsonify(generateReturnDictionary(200, "Amount Transferred succesfully"))
    
class Balance(Resource):
    def post(self):
        postedData=request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        retJson,error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        
        retJson = users.find({
            "Username":username
        },{
            # add 0 to not send this values
            "Password": 0,
            "_id":0
        })[0]

        return jsonify(retJson)
    
class TakeLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson,error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        
        cash=cashWithUser(username)
        debt=debtWithUser(username)
        updateAccount(username,cash+money)
        updateDebt(username,debt+money)
        
        return jsonify(generateReturnDictionary(200, "Loan added to your account"))
    

class PayLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        money = postedData["amount"]

        retJson,error = verifyCredentials(username,password)

        if error:
            return jsonify(retJson)
        
        cash=cashWithUser(username)

        if cash<money:
            return jsonify(generateReturnDictionary(303, "Not enough cash in your account"))
        
        debt=debtWithUser(username)
        updateAccount(username,cash-money)
        updateDebt(username,debt-money)

        return jsonify(generateReturnDictionary(200, "You've successfully paid your loan"))
    
api.add_resource(Register,'/register')
api.add_resource(Add,'/add')
api.add_resource(Transfer,'/transfer')
api.add_resource(Balance,'/balance')
api.add_resource(TakeLoan,'/takeloan')
api.add_resource(PayLoan,'/payloan')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)