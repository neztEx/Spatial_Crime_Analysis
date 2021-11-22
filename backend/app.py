import os
from flask import Flask, jsonify
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from query_generator import query_builder


app = Flask(__name__)

conf = SparkConf().setAppName('Spatial-Crime-Analysis')
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
csv_file = '../datasets/example.csv'
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(csv_file).\
    selectExpr(
    "RatecodeID",
    "VendorID",
    "passenger_count",
    "DATE(CAST(tpep_pickup_datetime AS timestamp)) AS date",
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude"
    ).where("date between '2016-01-01' AND '2016-01-05'")


@app.route('/run_sample', methods=['GET'])
def table():
    try:
        result = query_builder.sample_query(df)
        return result
    except Exception as e:
        print(e)
        return e

if __name__ == '__main__':
    try:
        app.run(port=os.environ.get('FLASK_PORT', 8080), host='0.0.0.0')
    finally:
        sc.stop()