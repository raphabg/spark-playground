from utils.spark_session import spark

# Create a sample list of data
data = [
    ("Alice", 25),
    ("Bob", 30),
    ("Charlie", 35)
]

# Define column names
columns = ["Name", "Age"]

# Create DataFrame
df = spark.createDataFrame(data, columns).filter("Age > 28")

# Show DataFrame content
df.show()