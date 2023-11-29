from flask import Flask
from flask_cors import CORS
import os
import csv
import pandas as pd


def get_value(string_name, df):
   return ([value for value in df[string_name]])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


file_path = "../Data Analyzing/CSV Files/"

'''path2 = "Graph_4_Hour.csv"
full_path = os.path.join(file_path, path2)
df = pd.read_csv(full_path)

print(df)

print(({"label": get_value('HOUR', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)}))'''

path2 = "Graph_2_Month.csv"
full_path = os.path.join(file_path, path2)
df = pd.read_csv(full_path)
df = df.drop(df.index[0])

print({"label": get_value('MONTH', df),
          "data": get_value('avg_delay_time', df),
          })


label_list = []
data_list = []
file_list = ["Graph_20_Fog.csv", "Graph_21_Rain_Drizzle.csv", "Graph_22_Snow_Ice Pellets.csv", "Graph_23_Hail.csv", "Graph_24_Thunder.csv", "Graph_25_Tornado_FunnelCloud.csv"]

for file_name in file_list:
      full_path = os.path.join(file_path, file_name)
      print(full_path)
      df = pd.read_csv(full_path)
      print(df)
      filename_without_extension = file_name.split('.csv')[0]

      parts = filename_without_extension.split('_')
      label_list.append(parts[-1] + '0')
      label_list.append(parts[-1] + '1')
      data_list.append(get_value('avg_delay_time', df))
      flattened_list = [item for sublist in data_list for item in sublist]

      #print(label_list)
      #print(flattened_list)



    # 假设 'SNDP' 和 'avg_delay_time' 是在最后一个文件中
    # 读取最后一个文件
    #last_file_path = os.path.join(file_path, "Graph_19_SNDP.csv")
    #df_last = pd.read_csv(last_file_path)

print ({
        "label": label_list,
       "data": flattened_list,
    })


@app.route("/lineChartData/Year")
def getLineChartDataYear():
  path2 = "Graph_1_Year.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('YEAR', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})


@app.route("/lineChartData/Month")
def getLineChartDataMonth():
  path2 = "Graph_2_Month.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('MONTH', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})




@app.route("/lineChartData/Week")
def getLineChartDataWeek():
  path2 = "Graph_3_Weekday.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  
  return ({"label": get_value('DAY_OF_WEEK', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})


@app.route("/lineChartData/Hour")
def getLineChartDataHour():
  path2 = "Graph_4_Hour.csv"
  full_path = os.path.join(file_path, path2)
  df = pd.read_csv(full_path)
  df = df.drop(df.index[0])

  
  return ({"label": get_value('HOUR', df),
          "attribute1": get_value('num_delays', df),
          "attribute2": get_value('avg_delay_time', df)})


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

@app.route("/barChartData/sixWeatherDigits")
def getLineChartDatasixWeatherDigits():
    label_list = []
    data_list = []
    file_list = ["Graph_20_Fog.csv", "Graph_21_Rain_Drizzle.csv", "Graph_22_Snow_Ice Pellets.csv", "Graph_23_Hail.csv", "Graph_24_Thunder.csv", "Graph_25_Tornado_FunnelCloud.csv"]

    for file_name in file_list:
        full_path = os.path.join(file_path, file_name)
        print(full_path)
        df = pd.read_csv(full_path)
        print(df)
        filename_without_extension = file_name.split('.csv')[0]

        parts = filename_without_extension.split('_')
        label_list.append(parts[-1] + '0')
        label_list.append(parts[-1] + '1')
        data_list.append(get_value('avg_delay_time', df))
        flattened_list = [item for sublist in data_list for item in sublist]


  
    return({
        "label": label_list,
       "data": flattened_list,
        })









@app.route("/pieChartData")
def getPieChartData():
  return {"label":['January', 'February', 'March', 'April', 'May'],
          "attribute":[12, 19, 3, 5, 2, 13],
          "colors":['red', 'orange', 'yellow', 'green', 'blue', 'purple']}


if __name__ == "__main__":
  app.run(debug=True)
