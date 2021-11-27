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
    return {'crimes': [
      {
        'type': 'Burglary',
        'location': {'latitude': 34.049738, 
                      'longitude': -118.238238}
      },
      {
        'type': 'Assault',
        'location': {'latitude': 34.1, 
                      'longitude': -118.2}
      },
      {
        'type': 'Burglary',
        'location': {'latitude': 34.0, 
                      'longitude': -118.3}
      },
      {
        'type': 'Burglary',
        'location': {'latitude': 34.0498, 
                      'longitude': -118.238}
      },
      {
        'type': 'Assault',
        'location': {'latitude': 34.15, 
                      'longitude': -118.25}
      },
      {
        'type': 'Burglary',
        'location': {'latitude': 34.05, 
                      'longitude': -118.35}
      }

    ]}


api.add_resource(Analysis, '/analysis')
api.add_resource(Map, '/map')

if __name__ == '__main__':
  app.run(port='5002')
