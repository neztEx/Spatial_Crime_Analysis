from pyspark.sql.types import *

def sample_query(df):
    try:
        """Query"""
        return {
            "output": "Query Executed Successfully"
            }
    except Exception as e:
        return e