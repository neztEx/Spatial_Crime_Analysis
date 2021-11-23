from pyspark.sql.types import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext


def configure_spark():
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