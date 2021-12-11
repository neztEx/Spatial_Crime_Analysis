import json
import os
import logging
import time
import datetime

from pyspark import SQLContext
import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from functools import reduce

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
        self.crime_data = self.LaCountyData(self.sql_context, dataset_path, 'crime_data_2019.csv').data
        self.twitter_data = self.TwitterData(self.sql_context, dataset_path).data
        self.crime_data_2010 = self.crime_data.filter(self.crime_data.year == "2010")
        self.crime_data_2011 = self.crime_data.filter(self.crime_data.year == "2011")
        self.crime_data_2012 = self.crime_data.filter(self.crime_data.year == "2012")
        self.crime_data_2013 = self.crime_data.filter(self.crime_data.year == "2013")
        self.crime_data_2014 = self.crime_data.filter(self.crime_data.year == "2014")
        self.crime_data_2015 = self.crime_data.filter(self.crime_data.year == "2015")
        self.crime_data_2016 = self.crime_data.filter(self.crime_data.year == "2016")
        self.crime_data_2017 = self.crime_data.filter(self.crime_data.year == "2017")
        self.crime_data_2018 = self.crime_data.filter(self.crime_data.year == "2018")
        self.crime_data_2019 = self.crime_data.filter(self.crime_data.year == "2019")
        

    class LaCountyData:


        def __init__(self, sql_la_county_data_context, dataset_path, data_file_path):
            self.crime_data_file_path = os.path.join(dataset_path, data_file_path)

            self.crime_data = sql_la_county_data_context.read.format('com.databricks.spark.csv').options(header='true',
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

        @property
        def data(self):
            """
                Returns Crime Data
            """
            return self.crime_data

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
            date_occurred = data_object.DATE_OCC[0: 10]
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
            year = data_object.DATE_OCC[6: 10]
            race = data_object.Vict_Descent
            # generating timestamp
            date_time = datetime.datetime(int(data_object.DATE_OCC[6: 10]), int(data_object.DATE_OCC[0: 2]),
                                          int(data_object.DATE_OCC[3: 5]))
            timestamp = str(time.mktime(date_time.timetuple())).split('.')[0]

            return (crime_id, date_reported, date_occurred, time_occurred, part_of_the_day, area, area_name, age, sex,
                    crime_type_id, crime_type, location, latitude, longitude, month, year, race, timestamp)

        def __preprocess_data(self):
            """
                adds a column on part of the day(morning, afternoon, evening, night) if it doesnt exist
            """
            if "part_of_the_day" not in self.crime_data.columns:
                self.crime_data = self.crime_data.rdd.map(lambda x: QueryEngine.LaCountyData.__map_function(x)). \
                    toDF(["crime_id", "date_reported", "date_occurred", "time_occurred", "part_of_the_day", "area",
                          "area_name", "age", "sex",
                          "crime_type_id", "crime_type", "location", "latitude", "longitude", "month", "year", "race",
                          "timestamp"])

            logger.info(self.crime_data.columns)
            self.crime_data = self.crime_data.sort(f.col("timestamp"))
            self.crime_data.show(10)

    class TwitterData:

        def __init__(self, sql_twitter_data_context, dataset_path):
            self.crime_data_file_path = os.path.join(dataset_path, 'twitter_data.csv')
            self.twitter_data = sql_twitter_data_context.read.format('com.databricks.spark.csv').options(header='true',
                                                                                                         inferschema='true').load(
                self.crime_data_file_path). \
                selectExpr(
                "id",
                "lat",
                "lon",
                "sentiment"
            )
            self.twitter_data.show(10)
            self.__preprocess_data()

        @property
        def data(self):
            """
                Returns Twitter Crime Data
            """
            return self.twitter_data

        @staticmethod
        def __map_function(data_object):
            """
                Uses timestamp of the day to return the part of the day
            """
            crime_id = data_object.id
            latitude = data_object.lat
            longitude = data_object.lon
            sentiment = data_object.sentiment
            return crime_id, latitude, longitude, sentiment

        def __preprocess_data(self):
            """
                preprocess the data
            """
            self.twitter_data = self.twitter_data.rdd.map(lambda x: QueryEngine.TwitterData.__map_function(x)). \
                toDF(["crime_id", "latitude", "longitude", "sentiment"])

            logger.info(self.twitter_data.columns)
            self.twitter_data.show(10)


def __area_based_query(self, area_name):
    """
        Helper function on area based query
    """
    logger.info("Executing Area Query...")
    query_results = __area_based_query_helper(self, self.crime_data, area_name)
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return response


def __area_based_query_helper(self, crime_data, area_name):
    """
        Loads the crime data on area basis
    """
    logger.info("Running Area Query...")
    crime_data.createOrReplaceTempView("crime_data")
    query = "select * from crime_data where area_name = '{0}' or '{1}' = 'all'".format(area_name, area_name)
    logger.info("Running :- {}".format(query))
    area_query_results = self.sql_context.sql(query)
    area_query_results.show(10)
    return area_query_results


def __date_based_query(self, start_date, end_date):
    """
        Helper function on year based query
    """
    logger.info("Executing Year Query...")
    query_results = __date_based_query_helper(self, self.crime_data, start_date, end_date)
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return response


def __date_based_query_helper(self, crime_data, start_date, end_date):
    """
        Loads the crime data on year basis
    """
    logger.info("Running Year Query...")
    if start_date is None:
        start_date = "1262304000"
    if end_date is None:
        end_date = str(datetime.datetime.now().timestamp()).split(".")[0]
    crime_data.createOrReplaceTempView("crime_data")
    query = "select * from crime_data where timestamp between '{0}' and '{1}'".format(start_date, end_date)
    logger.info("Running :- {}".format(query))
    year_query_results = self.sql_context.sql(query)
    return year_query_results


def __generic_attribute_query(self, start_date, end_date, area_name, grouping_attribute):
    """
        Loads the crime data grouping on different attributes
    """
    logger.info("Running {} Query...".format(grouping_attribute))
    query_results = self.crime_data

    if start_date is not None or end_date is not None:
        query_results = __date_based_query_helper(self, query_results, start_date, end_date)
    if area_name is not None:
        query_results = __area_based_query_helper(self, query_results, area_name)

    final_query_results = query_results.groupBy(grouping_attribute).agg(f.collect_list(f.struct("crime_type",
                                                                                                "latitude",
                                                                                                "longitude")))
    response = final_query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return response


def __aggregate_query(self, area_name, start_date, end_date, type_of_crime, gender, race):
    """
        Aggregate Query based on area_name, start_date, end_date, type_of_crime, gender, race
    """
    logger.info("Running Aggregate Query...")
    # Performance Checking
    start_time = time.time()
    self.crime_data.createOrReplaceTempView("crime_data")
    check_query = "select * from crime_data where (area_name = '{0}' or '{1}' = 'all') and " \
                  "(timestamp between '{2}' and '{3}') and " \
                  "(crime_type = '{4}' or'{4}' = 'all') and (sex = '{5}' or '{5}' = 'all') and " \
                  "(race = '{6}' or '{6}' = 'all')" \
        .format(area_name, area_name, start_date, end_date, type_of_crime, gender, race)
    logger.info("Running :- {}".format(check_query))
    check_query_results = self.sql_context.sql(check_query)
    logger.info(check_query_results.count())
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    response = check_query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return response


# Same queries run on split datasets


def __generic_attribute_new_query(self, start_date, end_date, area_name, grouping_attribute):
    """
        Loads the crime data grouping on different attributes
    """
    logger.info("Running {} Query...".format(grouping_attribute))
    start_time = time.time()
    query_results = []
    start_year = datetime.datetime.fromtimestamp(int(start_date)).year
    end_year = datetime.datetime.fromtimestamp(int(end_date)).year
    for year in range(start_year, end_year + 1):
        dataframe = eval("self.crime_data_" + str(year))
        dataframe.createOrReplaceTempView("crime_data_" + str(year))
        dataframe.show(10)
        intermediate_query = "select * from {4} where (area_name = '{0}' or '{1}' = 'all') and " \
                             "(timestamp between '{2}' and '{3}')" \
            .format(area_name, area_name, start_date, end_date, "crime_data_" + str(year))

        final_query_results = self.sql_context.sql(intermediate_query).groupBy(grouping_attribute).agg(
            f.collect_list(f.struct("crime_type",
                                    "latitude",
                                    "longitude")))
        if final_query_results.count() > 0:
            query_results.append(final_query_results)
    if len(query_results) > 1:
        final_result = reduce(DataFrame.union, query_results)
    elif len(query_results) == 1:
        final_result = query_results[0]
    else:
        final_result = final_query_results
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    response = final_result.toJSON().map(lambda j: json.loads(j)).collect()
    return response


def __aggregate_new_query(self, area_name, start_date, end_date, type_of_crime, gender, race):
    """
        Aggregate Query based on area_name, start_date, end_date, type_of_crime, gender, race
    """
    logger.info("Running Aggregate Query...")
    query_results = []
    start_year = datetime.datetime.fromtimestamp(int(start_date)).year
    end_year = datetime.datetime.fromtimestamp(int(end_date)).year
    for year in range(start_year, end_year + 1):
        dataframe = eval("self.crime_data_" + str(year))
        dataframe.createOrReplaceTempView("crime_data_" + str(year))
        intermediate_query = "select * from {7} where (area_name = '{0}' or '{1}' = 'all') and " \
                             "(timestamp between '{2}' and '{3}') and " \
                             "(crime_type = '{4}' or'{4}' = 'all') and (sex = '{5}' or '{5}' = 'all') and " \
                             "(race = '{6}' or '{6}' = 'all')" \
            .format(area_name, area_name, start_date, end_date, type_of_crime, gender, race, "crime_data_" + str(year))
        logger.info("Running :- {}".format(intermediate_query))
        intermediate_query_results = self.sql_context.sql(intermediate_query)
        if intermediate_query_results.count() > 1:
            query_results.append(intermediate_query_results)
    if len(query_results) > 1:
        final_result = reduce(DataFrame.union, query_results)

    elif len(query_results) == 1:
        final_result = query_results[0]
    else:
        final_result = intermediate_query_results
    response = final_result.toJSON().map(lambda j: json.loads(j)).collect()
    return response


def __twitter_query(self):
    """
        Aggregate Query on Twitter Data
    """
    logger.info("Running Aggregate Query on Twitter Data...")
    self.twitter_data.createOrReplaceTempView("twitter_data")
    query = "select * from twitter_data"
    logger.info("Running :- {}".format(query))
    query_results = self.sql_context.sql(query)
    response = query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return response


QueryEngine.__area_based_query = __area_based_query
QueryEngine.__date_based_query = __date_based_query
QueryEngine.__generic_attribute_query = __generic_attribute_query
QueryEngine.__generic_attribute_new_query = __generic_attribute_new_query
QueryEngine.__aggregate_new_query = __aggregate_new_query
QueryEngine.__aggregate_query = __aggregate_query
QueryEngine.__twitter_query = __twitter_query
