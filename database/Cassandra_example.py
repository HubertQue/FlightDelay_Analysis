from pyspark.sql import SparkSession,types
import json

def main(credentials):
    # 创建 SparkSession
    spark = SparkSession.builder \
        .appName("Cassandra Integration") \
        .config("spark.cassandra.connection.host", "cassandra.us-west-2.amazonaws.com") \
        .config("spark.cassandra.connection.port", "9142") \
        .config("spark.cassandra.input.consistency.level", "LOCAL_QUORUM") \
        .config("spark.cassandra.output.consistency.level", "LOCAL_QUORUM") \
        .config("spark.cassandra.auth.username", "twhitlock-at-697306959183") \
        .config("spark.cassandra.auth.password", credentials.password) \
        .config("spark.cassandra.connection.ssl.enabled", "true") \
        .config("spark.cassandra.connection.ssl.clientAuth.enabled", "true") \
        .config("spark.cassandra.connection.ssl.trustStore.path", "./resources/cassandra_truststore.jks") \
        .config("spark.cassandra.connection.ssl.trustStore.password", "123456") \
        .getOrCreate()

    df_read = spark.read \
      .format("org.apache.spark.sql.cassandra") \
      .options(table="test_table", keyspace="flightdb") \
      .load()

    df_read.printSchema()
    df_read = df_read.withColumn("test_key",df_read["test_key"].cast("integer")+1)
    df_read.show()

    #create schema
    data = [(3,)]
    schema = types.StructType([types.StructField("test_key", types.IntegerType(), False)])
    # create DataFrame
    df_write = spark.createDataFrame(data, schema)
    df_write.printSchema()

    #write into Cassandra
    df_write.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="test_table", keyspace="732_final").save()

if __name__ == "__main__":
    with open('credentials.json', 'r') as file:
        credentials = json.load(file)
    main(credentials)