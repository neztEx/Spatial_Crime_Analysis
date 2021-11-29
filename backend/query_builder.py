import json
import os
import logging

from pyspark import SQLContext
import pyspark.sql.functions as f

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryEngine:
    """
        Instantiates Query Engine and runs queries
    """

    def __init__(self, sc, dataset_path):
        """
            Init the query engine given a PySpark context and a dataset path
        """

        logger.info("Starting up the Query Engine: ")

        self.sc = sc

        # Load crime data for later use
        logger.info("Loading Crime data...")
        self.sql_context = SQLContext(sc)
        self.crime_data_file_path = os.path.join(dataset_path, 'crime_data.csv')
        self.crime_data = self.sql_context.read.format('com.databricks.spark.csv').options(header='true',
                                                                                           inferschema='true').load(
            self.crime_data_file_path). \
            selectExpr(
            "DR_NO",
            "Date_Rptd",
            "DATE_OCC",
            "TIME_OCC",
            "AREA",
            "AREA_NAME",
            "Rpt_Dist_No",
            "Part_1_2",
            "Crm_Cd",
            "Crm_Cd_Desc",
            "Mocodes",
            "Vict_Age",
            "Vict_Sex",
            "Vict_Descent",
            "Premis_Cd",
            "Premis_Desc",
            "Weapon_Used_Cd",
            "Weapon_Desc",
            "Status",
            "Status_Desc",
            "Crm_Cd_1",
            "Crm_Cd_2",
            "Crm_Cd_3",
            "Crm_Cd_4",
            "LOCATION",
            "Cross_Street",
            "LAT",
            "LON"
        )
        logger.info("Preprocessing the data...")
        self.__preprocess_data()

    @staticmethod
    def __map_function(data_object):
        """
            Uses timestamp of the day to return the part of the day
        """
        ts = int(data_object.TIME_OCC)
        if 400 <= ts < 1100:
            part_of_the_day = "morning"
        elif 1100 <= ts < 1600:
            part_of_the_day = "afternoon"
        elif 1600 <= ts < 2100:
            part_of_the_day = "evening"
        else:
            part_of_the_day = "night"
        crime_id = data_object.DR_NO
        date_reported = data_object.Date_Rptd
        date_occurred = data_object.DATE_OCC
        time_occurred = data_object.TIME_OCC
        area = data_object.AREA
        area_name = data_object.AREA_NAME
        age = data_object.Vict_Age
        sex = data_object.Vict_Sex
        crime_type_id = data_object.Crm_Cd
        crime_type = data_object.Crm_Cd_Desc
        location = data_object.LOCATION
        latitude = data_object.LAT
        longitude = data_object.LON
        month = data_object.DATE_OCC[0: 2]

        return (crime_id, date_reported, date_occurred, time_occurred, part_of_the_day, area, area_name, age, sex,
                crime_type_id, crime_type, location, latitude, longitude, month)

    def __preprocess_data(self):
        """
            adds a column on part of the day(morning, afternoon, evening, night) if it doesnt exist
        """
        if "part_of_the_day" not in self.crime_data.columns:
            self.crime_data = self.crime_data.rdd.map(lambda x: QueryEngine.__map_function(x)). \
                toDF(["crime_id", "date_reported", "date_occurred", "time_occurred", "part_of_the_day", "area",
                      "area_name", "age", "sex",
                      "crime_type_id", "crime_type", "location", "latitude", "longitude", "month"])
            self.crime_data.show(10)

def __location_based_query(self, location):
    """
        Helper function on location based query
    """
    logger.info("Executing Location Query...")
    return __location_based_query_helper(self.crime_data, location)


def __location_based_query_helper(crime_data, location):
    """
        Loads the crime data on location basis
    """
    logger.info("Running Location Query...")
    location_query_results = crime_data.where(crime_data.location == location)
    location_query_results.show(10)
    return location_query_results

def __year_based_query(self, start_year, end_year):
    """
        Helper function on year based query
    """
    logger.info("Executing Year Query...")
    return __year_based_query_helper(self.crime_data, start_year, end_year)

def __year_based_query_helper(crime_data, start_year, end_year):
    """
        Loads the crime data on year basis
    """
    logger.info("Running Year Query...")
    if start_year is None:
        start_year = "2010"
    if end_year is None:
        end_year = "2021"
    year_query_results = crime_data.where((start_year <= f.substring(crime_data.date_occurred, 7, 4)) &
                                               (f.substring(crime_data.date_occurred, 7, 4) <= end_year))
    year_query_results.show(10)
    return year_query_results

def __generic_attribute_query(self, start_year, end_year, location, grouping_attribue):
    """
        Loads the crime data grouping on different attributes
    """
    logger.info("Running {} Query...".format(grouping_attribue))
    day_part_query_results = self.crime_data

    if start_year is not None or end_year is not None:
        day_part_query_results = __year_based_query_helper(day_part_query_results, start_year, end_year)
    if location is not None:
        day_part_query_results = __location_based_query_helper(day_part_query_results, location)

    part_of_the_day_query_results = day_part_query_results.groupBy(grouping_attribue).count()
    part_of_the_day_query_results.show()
    return part_of_the_day_query_results


QueryEngine.__location_based_query = __location_based_query
QueryEngine.__year_based_query = __year_based_query
QueryEngine.__generic_attribute_query = __generic_attribute_query
