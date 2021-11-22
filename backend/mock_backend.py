from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func

import csv

'''
col_name = []
data = []

with open('../dataset/crime_data.csv') as csvfile:
  crime_data = csv.reader(csvfile)
  
  for i, row in enumerate(crime_data):
    for j, datum in enumerate(row):
      if(i ==0):
        col_name.append(datum)
      else:
        data.append(datum)
'''


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
