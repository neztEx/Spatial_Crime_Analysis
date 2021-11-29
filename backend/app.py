from flask import Blueprint, Flask, request
import json
import logging
from query_builder import QueryEngine

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main.route("/location_based_query", methods=["GET"])
def location_based_query():
    logger.debug(" %s crime data loading....", request.args.get('location'))
    query_results = query_engine.__location_based_query(request.args.get('location'))
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/year_based_query", methods=["GET"])
def year_based_query():
    logger.debug(" crime data between {0} and  {1} loading....".format(request.args.get('start_year'),
                                                                       request.args.get('end_year')))
    query_results = query_engine.__year_based_query(request.args.get('start_year'), request.args.get('end_year'))
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/day_part_based_query", methods=["GET"])
def day_part_based_query(start_year = None, end_year = None, location = None):
    logger.debug(" crime data on part of the day between {0} and  {1} at location {2} loading....".format(
                                                                                        request.args.get('start_year')
                                                                                       , request.args.get('end_year')
                                                                                       , request.args.get('location')))
    query_results = query_engine.__generic_attribute_query(start_year, end_year, location, "part_of_the_day")
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/type_of_crime_based_query", methods=["GET"])
def type_of_crime_based_query(start_year = None, end_year = None, location = None):
    logger.debug(" crime data on type of crime between {0} and  {1} at location {2} loading....".format(
                                                                                        request.args.get('start_year')
                                                                                       , request.args.get('end_year')
                                                                                       , request.args.get('location')))
    query_results = query_engine.__generic_attribute_query(start_year, end_year, location, "crime_type")
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/type_of_age_based_query", methods=["GET"])
def type_of_age_based_query(start_year = None, end_year = None, location = None):
    logger.debug(" crime data on different ages between {0} and  {1} at location {2} loading....".format(
                                                                                        request.args.get('start_year')
                                                                                       , request.args.get('end_year')
                                                                                       , request.args.get('location')))
    query_results = query_engine.__generic_attribute_query(start_year, end_year, location, "age")
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/type_of_sex_based_query", methods=["GET"])
def type_of_sex_based_query(start_year = None, end_year = None, location = None):
    logger.debug(" crime data on different sex between {0} and  {1} at location {2} loading....".format(
                                                                                        request.args.get('start_year')
                                                                                       , request.args.get('end_year')
                                                                                       , request.args.get('location')))
    query_results = query_engine.__generic_attribute_query(start_year, end_year, location, "sex")
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)

@main.route("/month_based_query", methods=["GET"])
def month_based_query(start_year = None, end_year = None, location = None):
    logger.debug(" crime data on different months between {0} and  {1} at location {2} loading....".format(
                                                                                        request.args.get('start_year')
                                                                                       , request.args.get('end_year')
                                                                                       , request.args.get('location')))
    query_results = query_engine.__generic_attribute_query(start_year, end_year, location, "month")
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return json.dumps(response)


def create_app(spark_context, dataset_path):
    global query_engine

    query_engine = QueryEngine(spark_context, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app