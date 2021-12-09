import cherrypy, os
from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf


def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("Spatial-Crime-Analysis").setAll(
        [('spark.eventLog.enabled', 'true'), ('spark.eventLog.dir',
                                              '/Users/suraj/Documents/Crime '
                                              'Analysis/Apache-Spark/spark-3.1.2-bin-hadoop3.2/logs'),
         ('spark.history.fs.logDirectory',
          '/Users/suraj/Documents/Crime Analysis/Apache-Spark/spark-3.1.2-bin-hadoop3.2/logs')])

    # IMPORTANT: pass aditional Python modules to each worker
    sc = SparkContext(conf=conf, pyFiles=['query_builder.py', 'app.py'])
    print("############################################################")
    print(sc.getConf().getAll())
    print("############################################################")
    return sc


def run_server(app):
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    # get the path of the dataset directory
    dataset_path = os.path.join('datasets')
    app = create_app(sc, dataset_path)

    # start web server
    run_server(app)
