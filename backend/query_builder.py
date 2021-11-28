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
        self.crime_data = self.sql_context.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(self.crime_data_file_path).\
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

def __location_based_query(self, location):
    """
        Loads the crime data on location basis
    """
    logger.info("Running Location Query...")
    location_query_results = self.crime_data.where(self.crime_data.LOCATION == location)
    location_query_results.show(10)
    results = location_query_results.toJSON().map(lambda j: json.loads(j)).collect()
    return results


QueryEngine.__location_based_query = __location_based_query