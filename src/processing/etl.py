from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, from_unixtime
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, LongType

def main():
    spark = SparkSession.builder \
        .appName("CustomerChurnETL") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    # Define the schema of the JSON messages
    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("event_type", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("value", DoubleType(), True)
    ])

    print("Initializing Spark ETL Job...")
    
    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user_events") \
        .option("startingOffsets", "earliest") \
        .load()

    # Transform raw data -> structured tables
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    
    # Add some derived columns
    processed_df = parsed_df.withColumn("event_time", from_unixtime(col("timestamp")).cast("timestamp"))

    # Write the stream to console (for development) or database
    query = processed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
