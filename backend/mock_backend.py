from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func


app = Flask(__name__)
api = Api(app)

class Analysis(Resource):
  def get(self):
    return {'analysis': 'test'}

class Map(Resource):
  def get(self):
    return {'map': 'test'}


api.add_resource(Analysis, '/analysis')
api.add_resource(Map, '/map')

if __name__ == '__main__':
  #app.run(port='5002')
  conn.engine.connect()
  conn.close()
