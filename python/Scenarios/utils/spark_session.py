from pyspark.sql import SparkSession
from pyspark import SparkConf

spark_configs = {
    "spark.app.name": "Balogo Raphael's Spark Playground",
    "spark.master": "spark://localhost:7077",
    "spark.executor.instances": "5",
    "spark.executor.memory": "2g",
    "spark.executor.cores": "1",
    "spark.driver.memory": "2g",
    "spark.eventLog.enabled": "true",
    "spark.eventLog.dir": "/mnt/c/wsl_mount_point/spark_logs/eventlogs",
    "spark.sql.shuffle.partitions": "100",
}

conf = SparkConf().setAll(spark_configs.items())
spark = SparkSession.builder.config(conf=conf).getOrCreate()