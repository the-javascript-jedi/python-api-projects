from pymongo import MongoClient

client=MongoClient("mongodb+srv://webdev-mongodb:webdev-mongodb@devconnector.ahxye.mongodb.net/?retryWrites=true&w=majority")

db=client.todo_db

collection_name=db["todo_collection"]