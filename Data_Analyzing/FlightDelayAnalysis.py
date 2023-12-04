from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, udf, format_number, hour
from pyspark.sql.types import IntegerType, StringType, FloatType
from timeit import default_timer as timer
import sys, calendar

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

def main():
    # Load the CSV data into three DataFrames
    df_2020 = spark.read.csv('./airport_weather_2020.csv', header=True, inferSchema=True)
    df_2021 = spark.read.csv('./airport_weather_2021.csv', header=True, inferSchema=True)
    df_2022 = spark.read.csv('./airport_weather_2022.csv', header=True, inferSchema=True)


    # Filter rows where DEP_DELAY > 0
    df_2020 = df_2020.withColumn("DEP_DELAY", df_2020["DEP_DELAY"].cast(IntegerType()))
    df_2020 = df_2020.filter(col("DEP_DELAY") > 0)
    df_2020.cache()

    # GET THE MONTH NAME FROM THE MONTH NUMBER
    def get_month_name(month_num):
        return calendar.month_name[month_num]

    month_udf = udf(get_month_name, StringType())

    # GRAPH 2-1: Delays by Month in 2020
    month_2020 = df_2020.filter(col("MONTH").isNotNull())
    month_2020 = month_2020.withColumn("MONTH", month_2020["MONTH"].cast(IntegerType()))
    month_2020 = month_2020.groupBy("MONTH").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH")
    month_2020 = month_2020.withColumn("MONTH", month_udf(col("MONTH")))
    print(month_2020.show())
    month_2020.coalesce(1).write.csv('Graph_2_Month_2020', header=True, mode='overwrite')

    # GET THE DAY OF WEEK NAME FROM THE NUMBER
    def get_day_of_week_name(day_num):
        return calendar.day_name[day_num - 1]

    day_of_week_udf = udf(get_day_of_week_name, StringType())

    # GRAPH 3-1: Delays by Day of Week in 2020
    weekday_2020 = df_2020.filter(col("DAY_OF_WEEK").isNotNull())
    weekday_2020 = weekday_2020.withColumn("DAY_OF_WEEK", weekday_2020["DAY_OF_WEEK"].cast(IntegerType()))
    weekday_2020 = weekday_2020.groupBy("DAY_OF_WEEK").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DAY_OF_WEEK")
    weekday_2020 = weekday_2020.withColumn("DAY_OF_WEEK", day_of_week_udf(col("DAY_OF_WEEK")))
    print(weekday_2020.show())
    weekday_2020.coalesce(1).write.csv('Graph_3_Weekday_2020', header=True, mode='overwrite')

    # GRAPH 4-1: Delays by Hour in 2020
    hour_2020 = df_2020.filter(col("DEP_TIME").isNotNull())
    hour_2020 = hour_2020.withColumn("HOUR", hour("DEP_TIME"))
    hour_2020 = hour_2020.groupBy("HOUR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("HOUR")
    hour_2020 = hour_2020.filter(col("HOUR").isNotNull())
    print(hour_2020.show())
    hour_2020.coalesce(1).write.csv('Graph_4_Hour_2020', header=True, mode='overwrite')


    # Filter rows where DEP_DELAY > 0
    df_2021 = df_2021.withColumn("DEP_DELAY", df_2021["DEP_DELAY"].cast(IntegerType()))
    df_2021 = df_2021.filter(col("DEP_DELAY") > 0)
    df_2021.cache()

    # GRAPH 2-2: Delays by Month in 2021
    month_2021 = df_2021.filter(col("MONTH").isNotNull())
    month_2021 = month_2021.withColumn("MONTH", month_2021["MONTH"].cast(IntegerType()))
    month_2021 = month_2021.groupBy("MONTH").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH")
    month_2021 = month_2021.withColumn("MONTH", month_udf(col("MONTH")))
    print(month_2021.show())
    month_2021.coalesce(1).write.csv('Graph_2_Month_2021', header=True, mode='overwrite')

    # GRAPH 3-2: Delays by Day of Week in 2021
    weekday_2021 = df_2021.filter(col("DAY_OF_WEEK").isNotNull())
    weekday_2021 = weekday_2021.withColumn("DAY_OF_WEEK", weekday_2021["DAY_OF_WEEK"].cast(IntegerType()))
    weekday_2021 = weekday_2021.groupBy("DAY_OF_WEEK").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DAY_OF_WEEK")
    weekday_2021 = weekday_2021.withColumn("DAY_OF_WEEK", day_of_week_udf(col("DAY_OF_WEEK")))
    print(weekday_2021.show())
    weekday_2021.coalesce(1).write.csv('Graph_3_Weekday_2021', header=True, mode='overwrite')

    # GRAPH 4-2: Delays by Hour in 2021
    hour_2021 = df_2021.filter(col("DEP_TIME").isNotNull())
    hour_2021 = hour_2021.withColumn("HOUR", hour("DEP_TIME"))
    hour_2021 = hour_2021.groupBy("HOUR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("HOUR")
    hour_2021 = hour_2021.filter(col("HOUR").isNotNull())
    print(hour_2021.show())
    hour_2021.coalesce(1).write.csv('Graph_4_Hour_2021', header=True, mode='overwrite')


    # Filter rows where DEP_DELAY > 0
    df_2022 = df_2022.withColumn("DEP_DELAY", df_2022["DEP_DELAY"].cast(IntegerType()))
    df_2022 = df_2022.filter(col("DEP_DELAY") > 0)
    df_2022.cache()

    # GRAPH 2-3: Delays by Month in 2022
    month_2022 = df_2022.filter(col("MONTH").isNotNull())
    month_2022 = month_2022.withColumn("MONTH", month_2022["MONTH"].cast(IntegerType()))
    month_2022 = month_2022.groupBy("MONTH").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH")
    month_2022 = month_2022.withColumn("MONTH", month_udf(col("MONTH")))
    print(month_2022.show())
    month_2022.coalesce(1).write.csv('Graph_2_Month_2022', header=True, mode='overwrite')

    # GRAPH 3-3: Delays by Day of Week in 2022
    weekday_2022 = df_2022.filter(col("DAY_OF_WEEK").isNotNull())
    weekday_2022 = weekday_2022.withColumn("DAY_OF_WEEK", weekday_2022["DAY_OF_WEEK"].cast(IntegerType()))
    weekday_2022 = weekday_2022.groupBy("DAY_OF_WEEK").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DAY_OF_WEEK")
    weekday_2022 = weekday_2022.withColumn("DAY_OF_WEEK", day_of_week_udf(col("DAY_OF_WEEK")))
    print(weekday_2022.show())
    weekday_2022.coalesce(1).write.csv('Graph_3_Weekday_2022', header=True, mode='overwrite')

    # GRAPH 4-3: Delays by Hour in 2022
    hour_2022 = df_2022.filter(col("DEP_TIME").isNotNull())
    hour_2022 = hour_2022.withColumn("HOUR", hour("DEP_TIME"))
    hour_2022 = hour_2022.groupBy("HOUR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("HOUR")
    hour_2022 = hour_2022.filter(col("HOUR").isNotNull())
    print(hour_2022.show())
    hour_2022.coalesce(1).write.csv('Graph_4_Hour_2022', header=True, mode='overwrite')


    # Use union method to merge these three DataFrames
    df_merged = df_2020.union(df_2021).union(df_2022)
    df_merged.cache()

    # GRAPH 1: Delays by Year
    year_analysis = df_merged.filter(col("YEAR").isNotNull())
    year_analysis = year_analysis.withColumn("YEAR", year_analysis["YEAR"].cast(IntegerType()))
    year_analysis = year_analysis.groupBy("YEAR").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("YEAR")
    print(year_analysis.show())
    year_analysis.coalesce(1).write.csv('Graph_1_Year', header=True, mode='overwrite')

    # GRAPH 5: Delays by State
    state_analysis = df_merged.filter(col("ORIGIN_STATE_NM").isNotNull())
    state_analysis = state_analysis.groupBy("ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    )
    state_analysis = state_analysis.orderBy(col("num_delays").desc(), col("avg_delay_time").desc())
    print(state_analysis.show())
    state_analysis.coalesce(1).write.csv('Graph_5_State', header=True, mode='overwrite')

    # GRAPH 6: Delays by Month in Top 10 States
    top_states = df_merged.filter(col("ORIGIN_STATE_NM").isNotNull() & col("MONTH").isNotNull())
    top_states = top_states.groupBy("ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays")
    ).orderBy(col("num_delays").desc()).limit(10)
    df_top_states = df_merged.join(top_states.hint("broadcast"), "ORIGIN_STATE_NM")
    df_top_states = df_top_states.groupBy("MONTH", "ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH", "ORIGIN_STATE_NM")
    df_top_states = df_top_states.withColumn("MONTH", month_udf(col("MONTH")))
    print(df_top_states.show())
    df_top_states.coalesce(1).write.csv('Graph_6_Top10_States', header=True, mode='overwrite')

    # GRAPH 7: Delays by City
    city_analysis = df_merged.filter(col("ORIGIN").isNotNull())
    city_analysis = city_analysis.groupBy(col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    )
    city_analysis = city_analysis.orderBy(col("num_delays").desc(), col("avg_delay_time").desc())
    print(city_analysis.show())
    city_analysis.coalesce(1).write.csv('Graph_7_City', header=True, mode='overwrite')

    # GRAPH 8: Delays by Month in Top 20 Cities
    top_cities = df_merged.filter(col("ORIGIN").isNotNull() & col("MONTH").isNotNull())
    top_cities = top_cities.groupBy("ORIGIN").agg(
        count("DEP_DELAY").alias("num_delays")
    ).orderBy(col("num_delays").desc()).limit(20)
    df_top_cities = df_merged.join(top_cities.hint("broadcast"), "ORIGIN")
    df_top_cities = df_top_cities.groupBy(col("MONTH"), col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MONTH", "ORIGIN_CITY")
    df_top_cities = df_top_cities.withColumn("MONTH", month_udf(col("MONTH")))
    print(df_top_cities.show())
    df_top_cities.coalesce(1).write.csv('Graph_8_Top20_Cities', header=True, mode='overwrite')

    # Function to categorize elevation
    def categorize_elevation(elevation):
        return ((int(elevation / 100)) + 1) * 100

    categorize_elevation_udf = udf(categorize_elevation, IntegerType())

    # GRAPH 9: Delays by Elevation
    elevation_analysis = df_merged.filter(col("ELEVATION").isNotNull())
    elevation_analysis = elevation_analysis.withColumn("ELEVATION", elevation_analysis["ELEVATION"].cast(FloatType()))
    elevation_analysis = elevation_analysis.withColumn("ELEVATION_CATEGORY", categorize_elevation_udf(col("ELEVATION")))
    elevation_analysis = elevation_analysis.groupBy("ELEVATION_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy(col("ELEVATION_CATEGORY"))
    print(elevation_analysis.show())
    elevation_analysis.coalesce(1).write.csv('Graph_9_Elevation', header=True, mode='overwrite')

    # Function to convert Fahrenheit to Celsius
    def fahrenheit_to_celsius(fahrenheit):
        celsius = (fahrenheit - 32) / 1.8
        return round(celsius, 2)

    fahrenheit_to_celsius_udf = udf(fahrenheit_to_celsius, FloatType())

    # Function to categorize temperature
    def categorize_temperature(temp):
        return int((temp + 40) // 5) * 5 - 35

    categorize_temperature_udf = udf(categorize_temperature, IntegerType())

    # GRAPH 10: Delays by Temp
    temp_analysis = df_merged.filter(col("TEMP").isNotNull())
    temp_analysis = temp_analysis.withColumn("TEMP", temp_analysis["TEMP"].cast(FloatType()))
    temp_analysis = temp_analysis.withColumn("TEMP", fahrenheit_to_celsius_udf(col("TEMP")))
    temp_analysis = temp_analysis.withColumn("TEMP_CATEGORY", categorize_temperature_udf(col("TEMP")))
    temp_analysis = temp_analysis.groupBy("TEMP_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("TEMP_CATEGORY")
    print(temp_analysis.show())
    temp_analysis.coalesce(1).write.csv('Graph_10_Temp', header=True, mode='overwrite')

    # Function to categorize dew point
    def categorize_dew_point(dewp):
        return int((dewp + 40) // 5) * 5 - 35

    categorize_dew_point_udf = udf(categorize_dew_point, IntegerType())

    # GRAPH 11: Delays by DEWP
    dewp_analysis = df_merged.filter(col("DEWP").isNotNull())
    dewp_analysis = dewp_analysis.withColumn("DEWP", dewp_analysis["DEWP"].cast(FloatType()))
    dewp_analysis = dewp_analysis.withColumn("DEWP_CATEGORY", categorize_dew_point_udf(col("DEWP")))
    dewp_analysis = dewp_analysis.groupBy("DEWP_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("DEWP_CATEGORY")
    print(dewp_analysis.show())
    dewp_analysis.coalesce(1).write.csv('Graph_11_DEWP', header=True, mode='overwrite')

    # GRAPH 12: Delays by VISIB
    visib_analysis = df_merged.filter(col("VISIB").isNotNull())
    visib_analysis = visib_analysis.withColumn("VISIB", visib_analysis["VISIB"].cast(FloatType()))
    visib_analysis = visib_analysis.groupBy("VISIB").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB")
    print(visib_analysis.show())
    visib_analysis.coalesce(1).write.csv('Graph_12_VISIB', header=True, mode='overwrite')

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
    visib_category = df_merged.filter(col("VISIB").isNotNull())
    visib_category = visib_category.withColumn("VISIB", visib_category["VISIB"].cast(FloatType()))
    visib_category = visib_category.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_category = visib_category.groupBy("VISIB_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY")
    print(visib_category.show())
    visib_category.coalesce(1).write.csv('Graph_13_VISIB_Category', header=True, mode='overwrite')

    # GRAPH 14: Delays by Category of VISIB in Different STATES
    visib_states = df_merged.filter(col("VISIB").isNotNull() & col("ORIGIN_STATE_NM").isNotNull())
    visib_states = visib_states.withColumn("VISIB", visib_states["VISIB"].cast(FloatType()))
    visib_states = visib_states.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_states = visib_states.groupBy("VISIB_CATEGORY", "ORIGIN_STATE_NM").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY", col("num_delays").desc())
    print(visib_states.show())
    visib_states.coalesce(1).write.csv('Graph_14_VISIB_States', header=True, mode='overwrite')

    # GRAPH 15: Delays by Category of VISIB in Different CITIES
    visib_cities = df_merged.filter(col("VISIB").isNotNull() & col("ORIGIN").isNotNull())
    visib_cities = visib_cities.withColumn("VISIB", visib_cities["VISIB"].cast(FloatType()))
    visib_cities = visib_cities.withColumn("VISIB_CATEGORY", categorize_visibility_udf(col("VISIB")))
    visib_cities = visib_cities.groupBy("VISIB_CATEGORY", col("ORIGIN").alias("ORIGIN_CITY")).agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("VISIB_CATEGORY", col("num_delays").desc())
    print(visib_cities.show())
    visib_cities.coalesce(1).write.csv('Graph_15_VISIB_Cities', header=True, mode='overwrite')

    # Function to categorize wind speed
    def categorize_wind_speed(wdsp):
        return int((wdsp // 5) * 5 + 5)

    categorize_wind_speed_udf = udf(categorize_wind_speed, IntegerType())

    # GRAPH 16: Delays by WDSP
    wdsp_analysis = df_merged.filter(col("WDSP").isNotNull())
    wdsp_analysis = wdsp_analysis.withColumn("WDSP", wdsp_analysis["WDSP"].cast(FloatType()))
    wdsp_analysis = wdsp_analysis.withColumn("WDSP_CATEGORY", categorize_wind_speed_udf(col("WDSP")))
    wdsp_analysis = wdsp_analysis.groupBy("WDSP_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("WDSP_CATEGORY")
    print(wdsp_analysis.show())
    wdsp_analysis.coalesce(1).write.csv('Graph_16_WDSP', header=True, mode='overwrite')

    # Function to categorize maximum sustained wind speed
    def categorize_max_wind_speed(mxspd):
        return int((mxspd // 10) * 10 + 10)

    categorize_max_wind_speed_udf = udf(categorize_max_wind_speed, IntegerType())

    # GRAPH 17: Delays by MXSPD
    mxspd_analysis = df_merged.filter(col("MXSPD").isNotNull())
    mxspd_analysis = mxspd_analysis.withColumn("MXSPD", mxspd_analysis["MXSPD"].cast(FloatType()))
    mxspd_analysis = mxspd_analysis.withColumn("MXSPD_CATEGORY", categorize_max_wind_speed_udf(col("MXSPD")))
    mxspd_analysis = mxspd_analysis.groupBy("MXSPD_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("MXSPD_CATEGORY")
    print(mxspd_analysis.show())
    mxspd_analysis.coalesce(1).write.csv('Graph_17_MXSPD', header=True, mode='overwrite')

    # Function to categorize precipitation
    def categorize_precipitation(prcp):
        return int((prcp // 2) * 2 + 2)

    categorize_precipitation_udf = udf(categorize_precipitation, IntegerType())

    # GRAPH 18: Delays by PRCP
    prcp_analysis = df_merged.filter(col("PRCP").isNotNull())
    prcp_analysis = prcp_analysis.withColumn("PRCP", prcp_analysis["PRCP"].cast(FloatType()))
    prcp_analysis = prcp_analysis.withColumn("PRCP_CATEGORY", categorize_precipitation_udf(col("PRCP")))
    prcp_analysis = prcp_analysis.groupBy("PRCP_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("PRCP_CATEGORY")
    print(prcp_analysis.show())
    prcp_analysis.coalesce(1).write.csv('Graph_18_PRCP', header=True, mode='overwrite')

    # Function to categorize snow depth
    def categorize_snow_depth(sndp):
        return int((sndp // 5) * 5 + 5)

    categorize_snow_depth_udf = udf(categorize_snow_depth, IntegerType())

    # GRAPH 19: Delays by SNDP
    sndp_analysis = df_merged.filter(col("SNDP").isNotNull())
    sndp_analysis = sndp_analysis.withColumn("SNDP", sndp_analysis["SNDP"].cast(FloatType()))
    sndp_analysis = sndp_analysis.withColumn("SNDP_CATEGORY", categorize_snow_depth_udf(col("SNDP")))
    sndp_analysis = sndp_analysis.groupBy("SNDP_CATEGORY").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("SNDP_CATEGORY")
    print(sndp_analysis.show())
    sndp_analysis.coalesce(1).write.csv('Graph_19_SNDP', header=True, mode='overwrite')

    # GRAPH 20: Delays by Fog
    fog_analysis = df_merged.filter(col("Fog").isNotNull())
    fog_analysis = fog_analysis.groupBy("Fog").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Fog")
    print(fog_analysis.show())
    fog_analysis.coalesce(1).write.csv('Graph_20_Fog', header=True, mode='overwrite')

    # GRAPH 21: Delays by Rain or Drizzle
    RainorDrizzle_analysis = df_merged.filter(col("Rain or Drizzle").isNotNull())
    RainorDrizzle_analysis = RainorDrizzle_analysis.withColumnRenamed("Rain or Drizzle", "Rain_or_Drizzle")
    RainorDrizzle_analysis = RainorDrizzle_analysis.groupBy("Rain_or_Drizzle").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Rain_or_Drizzle")
    print(RainorDrizzle_analysis.show())
    RainorDrizzle_analysis.coalesce(1).write.csv('Graph_21_Rain_Drizzle', header=True, mode='overwrite')

    # GRAPH 22: Delays by Snow or Ice Pellets
    Snow_IcePellets_analysis = df_merged.filter(col("Snow or Ice Pellets").isNotNull())
    Snow_IcePellets_analysis = Snow_IcePellets_analysis.withColumnRenamed("Snow or Ice Pellets", "Snow_or_Ice_Pellets")
    Snow_IcePellets_analysis = Snow_IcePellets_analysis.groupBy("Snow_or_Ice_Pellets").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Snow_or_Ice_Pellets")
    print(Snow_IcePellets_analysis.show())
    Snow_IcePellets_analysis.coalesce(1).write.csv('Graph_22_Snow_Ice_Pellets', header=True, mode='overwrite')

    # GRAPH 23: Delays by Hail
    hail_analysis = df_merged.filter(col("Hail").isNotNull())
    hail_analysis = hail_analysis.groupBy("Hail").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Hail")
    print(hail_analysis.show())
    hail_analysis.coalesce(1).write.csv('Graph_23_Hail', header=True, mode='overwrite')

    # GRAPH 24: Delays by Thunder
    thunder_analysis = df_merged.filter(col("Thunder").isNotNull())
    thunder_analysis = thunder_analysis.groupBy("Thunder").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Thunder")
    print(thunder_analysis.show())
    thunder_analysis.coalesce(1).write.csv('Graph_24_Thunder', header=True, mode='overwrite')

    # GRAPH 25: Delays by Tornado or Funnel Cloud
    Tornado_FunnelCloud_analysis = df_merged.filter(col("Tornado or Funnel Cloud").isNotNull())
    Tornado_FunnelCloud_analysis = Tornado_FunnelCloud_analysis.withColumnRenamed("Tornado or Funnel Cloud", "Tornado_or_Funnel_Cloud")
    Tornado_FunnelCloud_analysis = Tornado_FunnelCloud_analysis.groupBy("Tornado_or_Funnel_Cloud").agg(
        count("DEP_DELAY").alias("num_delays"),
        format_number(avg("DEP_DELAY"), 2).alias("avg_delay_time")
    ).orderBy("Tornado_or_Funnel_Cloud")
    print(Tornado_FunnelCloud_analysis.show())
    Tornado_FunnelCloud_analysis.coalesce(1).write.csv('Graph_25_Tornado_Funnel_Cloud', header=True, mode='overwrite')


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