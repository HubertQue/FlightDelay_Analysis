from Prediction import Predict
from flask import Flask, request, jsonify
from flask_cors import CORS


import os
import csv
import pandas as pd



def get_value(string_name, df):
   return ([value for value in df[string_name]])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# CORS(app, resources={r"/*": {"origins": "http://52.9.248.230:3000"}})


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
	return 'Hello &^&***)(())'

@app.route("/dataCheck")
def getData():
  return ({"label": "a",
          "attribute1": "b",
          "attribute2":  "c"})


@app.route("/lineChartData/Year")
def getLineChartDataYear():
  path2 = "Graph_1_Year_2020.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('YEAR', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})



@app.route("/lineChartData/Month")
def getLineChartDataMonth():
  path2 = "Graph_2_Month_2020.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('MONTH', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})


@app.route("/lineChartData/Week")
def getLineChartDataWeek():
  path2 = "Graph_3_Weekday_2020.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('DAY_OF_WEEK', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})


@app.route("/lineChartData/Hour")
def getLineChartDataHour():
  path2 = "Graph_4_Hour_2020.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  df = df.drop(df.index[0])

  
  return ({"label": get_value('HOUR', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})

@app.route("/lineChartData/Country")
def getLineChartDataCountry():
  path2 = "Graph_5_State.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"state": get_value('ORIGIN_STATE_NM', df),
          "average": get_value('avg_delay_time',df)})


@app.route("/barChartData/Elevation")
def getLineChartDataElevation():
  path2 = "Graph_9_Elevation.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('ELEVATION_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/Temperature")
def getLineChartDataTemp():
  path2 = "Graph_10_Temp.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('TEMP_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/DEWP")
def getLineChartDataDEWP():
  path2 = "Graph_11_DEWP.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('DEWP_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })

  
@app.route("/barChartData/VISIB")
def getLineChartDataVISIB():
  path2 = "Graph_12_VISIB.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('VISIB', df),
          "data": get_value('avg_delay_time', df),
          })


  
@app.route("/barChartData/VISIB_CATEGORY")
def getLineChartDataVISIB_CATEGORY():
  path2 = "Graph_13_VISIB Category.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('VISIB_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/WDSP")
def getLineChartDataWDSP():
  path2 = "Graph_16_WDSP.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('WDSP_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/MXSPD")
def getLineChartDataMXSPD():
  path2 = "Graph_17_MXSPD.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('MXSPD_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/PRCP")
def getLineChartDataPRCP():
  path2 = "Graph_18_PRCP.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('PRCP_CATEGORY', df),
          "data": get_value('avg_delay_time', df),
          })


@app.route("/barChartData/SNDP")
def getLineChartDataSNDP():
  path2 = "Graph_19_SNDP.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)

  
  return ({"label": get_value('SNDP_CATEGORY', df),
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
