from pyspark.sql import DataFrame
from IPython.display import display as ipy_display
import pandas as pd

def display(df: DataFrame, n: int = 20):
    """Mimic Databricks display for Spark DataFrames."""
    if not isinstance(df, DataFrame):
        raise TypeError("display() only supports Spark DataFrames.")
    
    pdf = df.limit(n).toPandas()  # Convert first N rows to pandas
    ipy_display(pdf)
