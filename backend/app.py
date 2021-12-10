from flask import Blueprint, Flask, request
import json
import logging
from query_builder import QueryEngine

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main.route("/area_based_query", methods=["GET"])
def area_based_query():
    logger.debug(" %s crime data loading....", request.args.get('area_name'))
    query_results = query_engine.__area_based_query(request.args.get('area_name'))
    return json.dumps(query_results)


@main.route("/date_based_query", methods=["GET"])
def date_based_query():
    logger.debug(" crime data between {0} and  {1} loading....".format(request.args.get('start_date'),
                                                                       request.args.get('end_date')))
    query_results = query_engine.__date_based_query(request.args.get('start_date'), request.args.get('end_date'))
    return json.dumps(query_results)


@main.route("/day_part_based_query", methods=["GET"])
def day_part_based_query():
    logger.debug(" crime data on part of the day between {0} and  {1} at area {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_query(request.args.get('start_date'), request.args.get('end_date'),
                                                           request.args.get('area_name'), "part_of_the_day")
    return json.dumps(query_results)


@main.route("/type_of_crime_based_query", methods=["GET"])
def type_of_crime_based_query():
    logger.debug(" crime data on type of crime between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_query(request.args.get('start_date'), request.args.get('end_date'),
                                                           request.args.get('area_name'), "crime_type")
    return json.dumps(query_results)


@main.route("/type_of_age_based_query", methods=["GET"])
def type_of_age_based_query():
    logger.debug(" crime data on different ages between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_query(request.args.get('start_date'), request.args.get('end_date'),
                                                           request.args.get('area_name'), "age")
    return json.dumps(query_results)


@main.route("/type_of_sex_based_query", methods=["GET"])
def type_of_sex_based_query():
    logger.debug(" crime data on different sex between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_query(request.args.get('start_date'),
                                                           request.args.get('end_date'),
                                                           request.args.get('area_name'), "sex")
    return json.dumps(query_results)


@main.route("/month_based_query", methods=["GET"])
def month_based_query():
    logger.debug(" crime data on different months between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_query(request.args.get('start_date'), request.args.get('end_date'),
                                                           request.args.get('area_name'), "month")
    return json.dumps(query_results)


@main.route("/aggregate_query", methods=["GET"])
def aggregate_query():
    logger.debug("Executing Aggregate Query...")
    query_results = query_engine.__aggregate_query(request.args.get('area_name'), request.args.get('start_date'),
                                                   request.args.get('end_date'), request.args.get('type_of_crime'),
                                                   request.args.get('gender'), request.args.get('race'))
    return json.dumps(query_results)


# New Apis to call on split dataset

@main.route("/day_part_based_new_query", methods=["GET"])
def day_part_based_new_query():
    logger.debug(" crime data on part of the day between {0} and  {1} at area {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_new_query(request.args.get('start_date'),
                                                               request.args.get('end_date'),
                                                               request.args.get('area_name'), "part_of_the_day")
    return json.dumps(query_results)


@main.route("/type_of_crime_based_new_query", methods=["GET"])
def type_of_crime_based_new_query():
    logger.debug(" crime data on type of crime between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_new_query(request.args.get('start_date'),
                                                               request.args.get('end_date'),
                                                               request.args.get('area_name'), "crime_type")
    return json.dumps(query_results)


@main.route("/type_of_age_based_new_query", methods=["GET"])
def type_of_age_based_new_query():
    logger.debug(" crime data on different ages between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_new_query(request.args.get('start_date'),
                                                               request.args.get('end_date'),
                                                               request.args.get('area_name'), "age")
    return json.dumps(query_results)


@main.route("/type_of_sex_based_new_query", methods=["GET"])
def type_of_sex_based_new_query():
    logger.debug(" crime data on different sex between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_new_query(request.args.get('start_date'),
                                                               request.args.get('end_date'),
                                                               request.args.get('area_name'), "sex")
    return json.dumps(query_results)


@main.route("/month_based_new_query", methods=["GET"])
def month_based_new_query():
    logger.debug(" crime data on different months between {0} and  {1} at area_name {2} loading....".format(
        request.args.get('start_date')
        , request.args.get('end_date')
        , request.args.get('area_name')))
    query_results = query_engine.__generic_attribute_new_query(request.args.get('start_date'),
                                                               request.args.get('end_date'),
                                                               request.args.get('area_name'), "month")
    return json.dumps(query_results)


@main.route("/aggregate_new_query", methods=["GET"])
def aggregate_new_query():
    logger.debug("Executing Aggregate Query...")
    query_results = query_engine.__aggregate_new_query(request.args.get('area_name'), request.args.get('start_date'),
                                                       request.args.get('end_date'), request.args.get('type_of_crime'),
                                                       request.args.get('gender'), request.args.get('race'))
    return json.dumps(query_results)


@main.route("/twitter_query", methods=["GET"])
def twitter_query():
    logger.debug("Executing Twitter Query...")
    query_results = query_engine.__twitter_query()
    return json.dumps(query_results)


def create_app(spark_context, dataset_path):
    global query_engine

    query_engine = QueryEngine(spark_context, dataset_path)

    app = Flask(__name__)
    app.register_blueprint(main)
    return app
