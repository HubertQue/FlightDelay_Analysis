from Prediction import Predict
from flask import Flask, request, jsonify
from flask_cors import CORS


import os
import csv
import pandas as pd
from db_get_data import query_table_and_convert_to_column_lists

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra import ConsistencyLevel
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
import os
import json


def create_session():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.load_verify_locations(os.path.join(os.path.dirname(__file__), 'resources/sf-class2-root.crt'))
    ssl_context.verify_mode = CERT_REQUIRED

    #pw_file = open('../../../credential/credentials.json', 'r')
    pw_file = open('./credentials.json', 'r')
    login_info = json.load(pw_file)
    if pw_file:
        pw_file.close()
    auth_provider = PlainTextAuthProvider(username='twhitlock-at-697306959183', password=login_info["password"])
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
    contact_endpoint = "cassandra.us-west-2.amazonaws.com"
    default_db_port = 9142
    db_cluster = Cluster(contact_points=[contact_endpoint], port=default_db_port, auth_provider=auth_provider, ssl_context=ssl_context,
                      execution_profiles={EXEC_PROFILE_DEFAULT: profile})

    return db_cluster.connect()


    
session = create_session()



def get_value(string_name, df):
   return ([value for value in df[string_name]])

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://52.9.248.230:3000"}})
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def sort_month(data):
         month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
         index_map = {month: index for index, month in enumerate(month_order)}

         sorted_indices = sorted(range(len(data['month'])), key=lambda i: index_map[data['month'][i]])
         for key in data:
                data[key] = [data[key][i] for i in sorted_indices]
         return data

def sort_week(data):
         weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
         index_map = {week: index for index, week in enumerate(weekday_order)}

         sorted_indices = sorted(range(len(data['day_of_week'])), key=lambda i: index_map[data['day_of_week'][i]])
         for key in data:
                data[key] = [data[key][i] for i in sorted_indices]
         return data


def sort_high_low(data, attribute_name):
         weekday_order = ['High_VISIB', 'Medium_VISIB', 'Low_VISIB']
         index_map = {week: index for index, week in enumerate(weekday_order)}

         sorted_indices = sorted(range(len(data[attribute_name])), key=lambda i: index_map[data[attribute_name][i]])
         for key in data:
                data[key] = [data[key][i] for i in sorted_indices]
         return data


def sort_number(data, attribute_name):
    sorted_indices = sorted(range(len(data[attribute_name])), key=lambda i: data[attribute_name][i])
    for key in data:
        data[key] = [data[key][i] for i in sorted_indices]
    return data


# file_path = "../cmpt732_client/CSV Files/"
file_path = "../Data_Analyzing/CSV Files/"


path2 = "Graph_2_Month_2020.csv"
full_path = os.path.join(file_path, path2)
df = pd.read_csv(full_path)
df = df.drop(df.index[0])


df = pd.read_csv(os.path.join(file_path, "Graph_5_State.csv"))

data = {"state": get_value('ORIGIN_STATE_NM', df),
          "average": get_value('avg_delay_time',df)}
state_avg_dict = dict(zip(data['state'], data['average']))

result_list = []
for key in state_avg_dict:
   result_list.append({key: state_avg_dict[key]})

result_list2 = []
for d in result_list:
    for key, value in d.items():
        result_list2.append({'key': key, 'value': value})


label_list = []
data_list = []
file_list = ["Graph_20_Fog.csv", "Graph_21_Rain_Drizzle.csv", "Graph_22_Snow_Ice_Pellets.csv", "Graph_23_Hail.csv", "Graph_24_Thunder.csv", "Graph_25_Tornado_Funnel_Cloud.csv"]

for file_name in file_list:
      full_path = os.path.join(file_path, file_name)
      # print(full_path)
      df = pd.read_csv(full_path)
      # print(df)
      filename_without_extension = file_name.split('.csv')[0]

      parts = filename_without_extension.split('_')
      label_list.append(parts[-1] + '0')
      label_list.append(parts[-1] + '1')
      data_list.append(get_value('avg_delay_time', df))
      flattened_list = [item for sublist in data_list for item in sublist]

@app.route('/')
def hello_world():
	return 'Check 123'

@app.route("/dataCheck")
def getData():
  return ({"label": "a",
          "attribute1": "b",
          "attribute2":  "c"})


@app.route("/lineChartData/Year")
def getLineChartDataYear():
  table = "Graph_1_Year"
  df = sort_number(query_table_and_convert_to_column_lists(session, table), str.lower('YEAR'))
  print(df)
  return ({"label": get_value(str.lower('YEAR'), df),
          "attribute2": get_value('avg_delay_time', df)})



@app.route("/lineChartData/Month")
def getLineChartDataMonth():
  path2 = "Graph_2_Month_2020"
  path3 = "Graph_2_Month_2021"
  path4 = "Graph_2_Month_2022"
  
  a = query_table_and_convert_to_column_lists(session, path2)
  print(' ---------- ')
  print(a)
  df = sort_month(query_table_and_convert_to_column_lists(session, path2))
  df3 = sort_month(query_table_and_convert_to_column_lists(session, path3))
  df4 = sort_month(query_table_and_convert_to_column_lists(session, path4))
  print(df)
  
  return ({"label": get_value('month', df),
          "attribute2": get_value('avg_delay_time', df),
          "attribute3": get_value('avg_delay_time', df3),
          "attribute4": get_value('avg_delay_time', df4)})


@app.route("/lineChartData/Week")
def getLineChartDataWeek():
  path2 = "Graph_3_Weekday_2020"
  path3 = "Graph_3_Weekday_2021"
  path4 = "Graph_3_Weekday_2022"
  print(query_table_and_convert_to_column_lists(session, path2))
  df = sort_week(query_table_and_convert_to_column_lists(session, path2))
  df3 = sort_week(query_table_and_convert_to_column_lists(session, path3))
  df4 = sort_week(query_table_and_convert_to_column_lists(session, path4))
  
  
  return ({"label": get_value('day_of_week', df),
          "attribute2": get_value('avg_delay_time', df),
          "attribute3": get_value('avg_delay_time', df3),
          "attribute4": get_value('avg_delay_time', df4)})


@app.route("/lineChartData/Hour")
def getLineChartDataHour():
  path2 = "Graph_4_Hour_2020"
  path3 = "Graph_4_Hour_2021"
  path4 = "Graph_4_Hour_2022"
  df = sort_number(query_table_and_convert_to_column_lists(session, path2), str.lower('HOUR'))
  df3 = sort_number(query_table_and_convert_to_column_lists(session, path3), str.lower('HOUR'))
  df4 = sort_number(query_table_and_convert_to_column_lists(session, path4), str.lower('HOUR'))


  

  
  return ({"label": get_value(str.lower('HOUR'), df),
          "attribute2": get_value('avg_delay_time', df),
          "attribute3": get_value('avg_delay_time', df3),
          "attribute4": get_value('avg_delay_time', df4)})

@app.route("/lineChartData/Country")
def getLineChartDataCountry():
  path2 = "Graph_5_State.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"state": get_value('ORIGIN_STATE_NM', df),
          "average": get_value('avg_delay_time',df)})


@app.route("/barChartData/Elevation")
def getLineChartDataElevation():
  path2 = "Graph_9_Elevation"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2), str.lower('ELEVATION_CATEGORY'))


  return ({"label": get_value(str.lower('ELEVATION_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),          
          })


@app.route("/barChartData/Temperature")
def getLineChartDataTemp():
  path2 = "Graph_10_Temp"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2), str.lower('TEMP_CATEGORY'))
  
  return ({"label": get_value(str.lower('TEMP_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/DEWP")
def getLineChartDataDEWP():
  path2 = "Graph_11_DEWP"

  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2), str.lower('DEWP_CATEGORY'))
  

  
  return ({"label": get_value(str.lower('DEWP_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })

  
@app.route("/barChartData/VISIB")
def getLineChartDataVISIB():
  path2 = "Graph_12_VISIB"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2), str.lower('VISIB'))


  
  return ({"label": get_value(str.lower('VISIB'), df),
          "data": get_value('avg_delay_time', df),
          })


  
@app.route("/barChartData/VISIB_CATEGORY")
def getLineChartDataVISIB_CATEGORY():
  path2 = "Graph_13_VISIB_Category"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_high_low(query_table_and_convert_to_column_lists(session, path2), str.lower('VISIB_CATEGORY'))

  
  return ({"label": get_value(str.lower('VISIB_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/WDSP")
def getLineChartDataWDSP():
  path2 = "Graph_16_WDSP"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2),str.lower('WDSP_CATEGORY'))


  
  return ({"label": get_value(str.lower('WDSP_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/MXSPD")
def getLineChartDataMXSPD():
  path2 = "Graph_17_MXSPD"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2),str.lower('MXSPD_CATEGORY'))


  
  return ({"label": get_value(str.lower('MXSPD_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/PRCP")
def getLineChartDataPRCP():
  path2 = "Graph_18_PRCP"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2),str.lower('PRCP_CATEGORY'))

  
  return ({"label": get_value(str.lower('PRCP_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/SNDP")
def getLineChartDataSNDP():
  path2 = "Graph_19_SNDP"
  #df = query_table_and_convert_to_column_lists(session, path2)
  df = sort_number(query_table_and_convert_to_column_lists(session, path2),str.lower('SNDP_CATEGORY'))

  
  return ({"label": get_value(str.lower('SNDP_CATEGORY'), df),
          "data": get_value('avg_delay_time', df),
          })

# This bar combines 6 different weather conditions

@app.route("/barChartData/FRSHTT")
def getLineChartDatasixWeatherDigits():
    label_list = []
    data_list = []
    file_list = ["Graph_20_Fog.csv", "Graph_21_Rain_Drizzle.csv", "Graph_22_Snow_Ice_Pellets.csv", "Graph_23_Hail.csv", "Graph_24_Thunder.csv", "Graph_25_Tornado_Funnel_Cloud.csv"]

    for file_name in file_list:
        full_path = os.path.join(file_path, file_name)
        # print(full_path)
        df = pd.read_csv(full_path)
        # print(df)
        filename_without_extension = file_name.split('.csv')[0]

        parts = filename_without_extension.split('_')
        label_list.append(parts[-1] + '0')
        label_list.append(parts[-1] + '1')
        data_list.append(get_value('avg_delay_time', df))
        flattened_list = [item for sublist in data_list for item in sublist]
  
        unique_labels = list(set(label[:-1] for label in label_list))
        data1 = [flattened_list[i] for i in range(len(flattened_list)) if label_list[i].endswith('0')]
        data2 = [flattened_list[i] for i in range(len(flattened_list)) if label_list[i].endswith('1')]


    return({
        "label": unique_labels,
        "data": data1,
        "data1": data2,
        })


@app.route("/weatherform", methods=['POST'])
def getWeatherData():
    # 获取 JSON 数据
    data = request.json
    date = data.get('date')
    hour = data.get('hour')
    airport = data.get('airport')
    AveT = data.get('AveT')
    MaxT = data.get('MaxT')
    MinT = data.get('MinT')
    visibility = data.get('visibility')
    weatherConditions = data.get('weatherConditions')

    result = {
        "date": date,
        "hour": hour,
        "airport": airport,
        "AveT": AveT,
        "MaxT": MaxT,
        "MinT": MinT,
        "visibility": visibility,
        "weatherConditions": weatherConditions
    }
    print("result is: " , result)
    prediction, probability = Predict.predict_delay(result)

    return str(prediction)

if __name__ == "__main__":
  app.run(debug=True)
