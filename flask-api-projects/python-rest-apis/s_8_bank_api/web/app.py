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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)