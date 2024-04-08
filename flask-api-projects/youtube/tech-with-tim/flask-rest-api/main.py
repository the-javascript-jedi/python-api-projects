# run app - python main.py
from flask import Flask
# from flask_restful import Api, Resource
from flask_restx import Api, Resource

app = Flask(__name__)
api=Api(app)

# using namespace
ns = api.namespace('my_namespace', description='My operations')

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        """Returns a simple Hello World message"""
        return {'hello': 'world'}
    def post(self):
        return {"data":"Posted"}

if __name__ == '__main__':
    app.run(debug=True)
