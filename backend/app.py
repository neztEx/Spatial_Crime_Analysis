from flask import Blueprint, Flask, request
import json
import logging
from query_builder import QueryEngine

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main.route("/location_based_query/<string:location>", methods=["GET"])
def location_based_query(location):
    logger.debug(" %s crime data loading....", location)
    query_results = query_engine.__location_based_query(location)
    return json.dumps(query_results)



def create_app(spark_context, dataset_path):
    global query_engine

    query_engine = QueryEngine(spark_context, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app