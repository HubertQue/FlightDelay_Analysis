from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, udf, format_number, hour
from pyspark.sql.types import IntegerType, StringType, FloatType
from timeit import default_timer as timer
import sys, calendar

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

def main():
    # Load the CSV data into a DataFrame
    df = spark.read.csv('./airport_weather_2020.csv', header=True, inferSchema=True)

    # Filter rows where DEP_DELAY > 0
    df = df.withColumn("DEP_DELAY", df["DEP_DELAY"].cast(IntegerType()))
    df_delayed = df.filter(col("DEP_DELAY") > 0)
    df_delayed.cache()

    # GRAPH 1: Delays by Year
    year_analysis = df_delayed.filter(col("YEAR").isNotNull())
    year_analysis = year_analysis.withColumn("YEAR", year_analysis["YEAR"].cast(IntegerType()))
    year_analysis = year_analysis.groupBy("YEAR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("YEAR")
    print(year_analysis.show())
    year_analysis.coalesce(1).write.csv('Graph_1', header=True, mode='overwrite')

    # GET THE MONTH NAME FROM THE MONTH NUMBER
    def get_month_name(month_num):
        return calendar.month_name[month_num]

    month_udf = udf(get_month_name, StringType())

    # GRAPH 2: Delays by Month
    month_analysis = df_delayed.filter(col("MONTH").isNotNull())
    month_analysis = month_analysis.withColumn("MONTH", month_analysis["MONTH"].cast(IntegerType()))
    month_analysis = month_analysis.groupBy("MONTH").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH")
    month_analysis = month_analysis.withColumn("MONTH", month_udf(col("MONTH")))
    print(month_analysis.show())
    month_analysis.coalesce(1).write.csv('Graph_2', header=True, mode='overwrite')

    # GET THE DAY OF WEEK NAME FROM THE NUMBER
    def get_day_of_week_name(day_num):
        return calendar.day_name[day_num - 1]

    day_of_week_udf = udf(get_day_of_week_name, StringType())

    # GRAPH 3: Delays by Day of Week
    weekday_analysis = df_delayed.filter(col("DAY_OF_WEEK").isNotNull())
    weekday_analysis = weekday_analysis.withColumn("DAY_OF_WEEK", weekday_analysis["DAY_OF_WEEK"].cast(IntegerType()))
    weekday_analysis = weekday_analysis.groupBy("DAY_OF_WEEK").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DAY_OF_WEEK")
    weekday_analysis = weekday_analysis.withColumn("DAY_OF_WEEK", day_of_week_udf(col("DAY_OF_WEEK")))
    print(weekday_analysis.show())
    weekday_analysis.coalesce(1).write.csv('Graph_3', header=True, mode='overwrite')

    # GRAPH 4: Delays by Hour
    hour_analysis = df_delayed.filter(col("DEP_TIME").isNotNull())
    hour_analysis = hour_analysis.withColumn("HOUR", hour("DEP_TIME"))
    hour_analysis = hour_analysis.groupBy("HOUR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("HOUR")
    print(hour_analysis.show())
    hour_analysis.coalesce(1).write.csv('Graph_4', header=True, mode='overwrite')

    # GRAPH 5: Delays by State
    state_analysis = df_delayed.filter(col("ORIGIN_STATE_NM").isNotNull())
    state_analysis = state_analysis.groupBy("ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    )
    state_analysis = state_analysis.orderBy(col("num_delays").desc(), col("avg_delay_time").desc())
    print(state_analysis.show())
    state_analysis.coalesce(1).write.csv('Graph_5', header=True, mode='overwrite')

    # GRAPH 6: Delays by Month in Top 10 States
    top_states = df_delayed.filter(col("ORIGIN_STATE_NM").isNotNull() & col("MONTH").isNotNull())
    top_states = top_states.groupBy("ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays")
    ).orderBy(col("num_delays").desc()).limit(10)
    df_top_states = df_delayed.join(top_states.hint("broadcast"), "ORIGIN_STATE_NM")
    df_top_states = df_top_states.groupBy("MONTH", "ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH", "ORIGIN_STATE_NM")
    df_top_states = df_top_states.withColumn("MONTH", month_udf(col("MONTH")))
    print(df_top_states.show())
    df_top_states.coalesce(1).write.csv('Graph_6', header=True, mode='overwrite')

    # GRAPH 7: Delays by City
    city_analysis = df_delayed.filter(col("ORIGIN").isNotNull())
    city_analysis = city_analysis.groupBy(col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    )
    city_analysis = city_analysis.orderBy(col("num_delays").desc(), col("avg_delay_time").desc())
    print(city_analysis.show())
    city_analysis.coalesce(1).write.csv('Graph_7', header=True, mode='overwrite')

    # GRAPH 8: Delays by Month in Top 20 Cities
    top_cities = df_delayed.filter(col("ORIGIN").isNotNull() & col("MONTH").isNotNull())
    top_cities = top_cities.groupBy("ORIGIN").agg(
        count("DEP_DELAY").alias("num_delays")
    ).orderBy(col("num_delays").desc()).limit(20)
    df_top_cities = df_delayed.join(top_cities.hint("broadcast"), "ORIGIN")
    df_top_cities = df_top_cities.groupBy(col("MONTH"), col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH", "ORIGIN_CITY")
    df_top_cities = df_top_cities.withColumn("MONTH", month_udf(col("MONTH")))
    print(df_top_cities.show())
    df_top_cities.coalesce(1).write.csv('Graph_8', header=True, mode='overwrite')

    # GRAPH 9: Delays by Elevation
    elevation_analysis = df_delayed.filter(col("ELEVATION").isNotNull())
    elevation_analysis = elevation_analysis.withColumn("ELEVATION", elevation_analysis["ELEVATION"].cast(FloatType()))
    elevation_analysis = elevation_analysis.groupBy("ELEVATION").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy(col("ELEVATION").desc())
    print(elevation_analysis.show())
    elevation_analysis.coalesce(1).write.csv('Graph_9', header=True, mode='overwrite')

    # Function to convert Fahrenheit to Celsius
    def fahrenheit_to_celsius(fahrenheit):
        celsius = (fahrenheit - 32) / 1.8
        return round(celsius, 2)

    fahrenheit_to_celsius_udf = udf(fahrenheit_to_celsius, FloatType())

    # GRAPH 10: Delays by Temp
    temp_analysis = df_delayed.filter(col("TEMP").isNotNull())
    temp_analysis = temp_analysis.withColumn("TEMP", df["TEMP"].cast(FloatType()))
    temp_analysis = temp_analysis.withColumn("TEMP", fahrenheit_to_celsius_udf(col("TEMP")))
    temp_analysis = temp_analysis.groupBy("TEMP").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("TEMP")
    print(temp_analysis.show())
    temp_analysis.coalesce(1).write.csv('Graph_10', header=True, mode='overwrite')

    # GRAPH 11: Delays by DEWP
    dewp_analysis = df_delayed.filter(col("DEWP").isNotNull())
    dewp_analysis = dewp_analysis.withColumn("DEWP", df["DEWP"].cast(FloatType()))
    dewp_analysis = dewp_analysis.groupBy("DEWP").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DEWP")
    print(dewp_analysis.show())
    dewp_analysis.coalesce(1).write.csv('Graph_11', header=True, mode='overwrite')

    # GRAPH 12: Delays by VISIB
    visib_analysis = df_delayed.filter(col("VISIB").isNotNull())
    visib_analysis = visib_analysis.withColumn("VISIB", df["VISIB"].cast(FloatType()))
    visib_analysis = visib_analysis.groupBy("VISIB").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB")
    print(visib_analysis.show())
    visib_analysis.coalesce(1).write.csv('Graph_12', header=True, mode='overwrite')

    # Function to categorize visibility
    def categorize_visibility(visib):
        if visib < 4:
            return "Low_VISIB"
        elif visib <= 10:
            return "Medium_VISIB"
        else:
            return "High_VISIB"

    categorize_visibility_udf = udf(categorize_visibility, StringType())

    # GRAPH 13: Delays by Category of VISIB
    visib_category = df_delayed.filter(col("VISIB").isNotNull())
    visib_category = visib_category.withColumn("VISIB", df["VISIB"].cast(FloatType()))
    visib_category = visib_category.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_category = visib_category.groupBy("VISIB_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY")
    print(visib_category.show())
    visib_category.coalesce(1).write.csv('Graph_13', header=True, mode='overwrite')

    # GRAPH 14: Delays by Category of VISIB in Different STATES
    visib_states = df_delayed.filter(col("VISIB").isNotNull() & col("ORIGIN_STATE_NM").isNotNull())
    visib_states = visib_states.withColumn("VISIB", df["VISIB"].cast(FloatType()))
    visib_states = visib_states.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_states = visib_states.groupBy("VISIB_CATEGORY", "ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY", col("num_delays").desc())
    print(visib_states.show())
    visib_states.coalesce(1).write.csv('Graph_14', header=True, mode='overwrite')

    # GRAPH 15: Delays by Category of VISIB in Different CITIES
    visib_cities = df_delayed.filter(col("VISIB").isNotNull() & col("ORIGIN").isNotNull())
    visib_cities = visib_cities.withColumn("VISIB", df["VISIB"].cast(FloatType()))
    visib_cities = visib_cities.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_cities = visib_cities.groupBy("VISIB_CATEGORY", col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY", col("num_delays").desc())
    print(visib_cities.show())
    visib_cities.coalesce(1).write.csv('Graph_15', header=True, mode='overwrite')

    # GRAPH 16: Delays by WDSP
    wdsp_analysis = df_delayed.filter(col("WDSP").isNotNull())
    wdsp_analysis = wdsp_analysis.withColumn("WDSP", df["WDSP"].cast(FloatType()))
    wdsp_analysis = wdsp_analysis.groupBy("WDSP").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("WDSP")
    print(wdsp_analysis.show())
    wdsp_analysis.coalesce(1).write.csv('Graph_16', header=True, mode='overwrite')

    # GRAPH 17: Delays by MXSPD
    mxspd_analysis = df_delayed.filter(col("MXSPD").isNotNull())
    mxspd_analysis = mxspd_analysis.withColumn("MXSPD", df["MXSPD"].cast(FloatType()))
    mxspd_analysis = mxspd_analysis.groupBy("MXSPD").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MXSPD")
    print(mxspd_analysis.show())
    mxspd_analysis.coalesce(1).write.csv('Graph_17', header=True, mode='overwrite')

    # GRAPH 18: Delays by PRCP
    prcp_analysis = df_delayed.filter(col("PRCP").isNotNull())
    prcp_analysis = prcp_analysis.withColumn("PRCP", df["PRCP"].cast(FloatType()))
    prcp_analysis = prcp_analysis.groupBy("PRCP").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("PRCP")
    print(prcp_analysis.show())
    prcp_analysis.coalesce(1).write.csv('Graph_18', header=True, mode='overwrite')

    # GRAPH 19: Delays by SNDP
    sndp_analysis = df_delayed.filter(col("SNDP").isNotNull())
    sndp_analysis = sndp_analysis.withColumn("SNDP", df["SNDP"].cast(FloatType()))
    sndp_analysis = sndp_analysis.groupBy("SNDP").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("SNDP")
    print(sndp_analysis.show())
    sndp_analysis.coalesce(1).write.csv('Graph_19', header=True, mode='overwrite')

    # GRAPH 20: Delays by Fog
    fog_analysis = df_delayed.filter(col("Fog").isNotNull())
    fog_analysis = fog_analysis.groupBy("Fog").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Fog")
    print(fog_analysis.show())
    fog_analysis.coalesce(1).write.csv('Graph_20', header=True, mode='overwrite')

    # GRAPH 21: Delays by Rain or Drizzle
    RainorDrizzle_analysis = df_delayed.filter(col("Rain or Drizzle").isNotNull())
    RainorDrizzle_analysis = RainorDrizzle_analysis.groupBy("Rain or Drizzle").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Rain or Drizzle")
    print(RainorDrizzle_analysis.show())
    RainorDrizzle_analysis.coalesce(1).write.csv('Graph_21', header=True, mode='overwrite')

    # GRAPH 22: Delays by Snow or Ice Pellets
    Snow_IcePellets_analysis = df_delayed.filter(col("Snow or Ice Pellets").isNotNull())
    Snow_IcePellets_analysis = Snow_IcePellets_analysis.groupBy("Snow or Ice Pellets").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Snow or Ice Pellets")
    print(Snow_IcePellets_analysis.show())
    Snow_IcePellets_analysis.coalesce(1).write.csv('Graph_22', header=True, mode='overwrite')

    # GRAPH 23: Delays by Hail
    hail_analysis = df_delayed.filter(col("Hail").isNotNull())
    hail_analysis = hail_analysis.groupBy("Hail").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Hail")
    print(hail_analysis.show())
    hail_analysis.coalesce(1).write.csv('Graph_23', header=True, mode='overwrite')

    # GRAPH 24: Delays by Thunder
    thunder_analysis = df_delayed.filter(col("Thunder").isNotNull())
    thunder_analysis = thunder_analysis.groupBy("Thunder").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Thunder")
    print(thunder_analysis.show())
    thunder_analysis.coalesce(1).write.csv('Graph_24', header=True, mode='overwrite')

    # GRAPH 25: Delays by Tornado or Funnel Cloud
    Tornado_FunnelCloud_analysis = df_delayed.filter(col("Tornado or Funnel Cloud").isNotNull())
    Tornado_FunnelCloud_analysis = Tornado_FunnelCloud_analysis.groupBy("Tornado or Funnel Cloud").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Tornado or Funnel Cloud")
    print(Tornado_FunnelCloud_analysis.show())
    Tornado_FunnelCloud_analysis.coalesce(1).write.csv('Graph_25', header=True, mode='overwrite')


if __name__ == '__main__':
    spark = SparkSession.builder.appName('FlightDelayAnalysis').getOrCreate()
    assert spark.version >= '3.0' # make sure we have Spark 3.0+
    spark.sparkContext.setLogLevel('WARN')
    start_time = timer()
    main()
    spark.stop()
    end_time = timer()
    execution_time = end_time - start_time
    print("Execution time: {} seconds".format(execution_time))