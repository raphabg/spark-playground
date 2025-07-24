from pyspark.sql import SparkSession

spark = None

def setup_spark_session():
    global spark
    spark = (SparkSession
             .builder
             .getOrCreate()
             )

