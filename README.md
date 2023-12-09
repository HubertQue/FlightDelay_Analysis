# Airline Delays Analysis and Prediction

## Project Introduction

Inspired by [a Kaggle dataset](https://www.kaggle.com/datasets/threnjen/2019-airline-delays-and-cancellations), our group decided to further investigate the relationship between airport weather conditions and flight delays/cancellations. Notice that this Kaggle dataset is made by joining two public datasets from which limited attributes are included and only data in 2019 was used. From the source datasets, we found that the source dataset contains a wealth of relevant attributes, which has rich potential that we can do more research by using more attributes and expanding the target year from a single year to several years.

## Project Data Source

From Bureau of Transportation statistics
https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGK

From National Centers for Environmental Information (NOAA)
https://www.ncei.noaa.gov/access/search/data-search/global-summary-of-the-day

## Demo

Use 'SFUNET' wifi might have problem to connect;
Please use 'eduroam', 'SFUNET-SECURE' or other wifi to connect.

Live demo of the UI Design can be accessed at the following link: http://52.9.248.230:3000/

## Final Presentation

Final presentation of our project can be accessed at the following link: https://youtu.be/5akKUK-J2tU

## Notes

This submission serves as the final project for CMPT 732: Programming for Big Data Lab 1.
For guidance on running the code, please refer to the instructions provided in the RUNNING.md
Comprehensive project information and details can be accessed in the report.pdf

## Contributors

Zizheng Que
Lingyun Li
Shan Chen
Yangyang Jiang

## Main project structure

```
FlightDelay_Analysis
├── Data_Analyzing
├── Data_Processing
├── backend
│   	└─── Prediction
├── client
└── database
```

Above is an overview of our project's directory structure. Detailed introductions for important files and folders in each section are provided below:

```
	Data_Analyzing
│   ├── CSV Files
│   └── FlightDelayAnalysis.py
```

This folder contains the source code for data analyzing files and our csv data source.
Details are as follows:
FlightDelayAnalysis.py - Python file used for analyzing various factors that affect flight delays and generating (.csv) files.
CSV Files/ - 31 CSV files created after running the PySpark code of data analyzing.

```
	Data_Processing
│   ├── Airport_Data_Clean.py
│   ├── TableJoin.py
│   ├── WBAN_Converter.py
│   └── Weather_Data_Merge_Clean.py
```

This folder contains the source code for data preprocessing files.
Details are as follows:
Airport_Data_Clean.py - python file used to clean unnecessary attributes of airport data files.
Weather_Data_Merge_Clean.py - Python file used to clean unnecessary attributes of weather data files.
WBAN_Converter.py - python file used to retrieve the corresponding weather station ID based on the IATA airport code for each airport
TableJoin.py - python file used to join airport data and weather data.

```
	backend
│   ├── Prediction
│   ├── db_get_data.py
│   ├── resources
│   ├── server.py
│   ├── server_db.py
│   ├── ……
```

This folder contains the source code for backend files.
Details are as follows:
Server.py - backend file that connects with local csv files
Server_db.py - backend file that connects with Cassandra database

```
   client
│   └── src
│   │   ├── components
│   │   ├── HomePage.js
│   │   ├── DataAnalysis.js
│   │   ├── BarChart.js
│   │   ├── LineChart.js
│   │   ├── ……
│   │   └── css
```

This folder contains the source code for all the React components, like DataAnalysis.js, LineChart.js, BarChart.js and css styling code, like HomePage.css.

```
Database
│   ├── db_connector.py
│   ├── db_get_data.py
│   ├── resources
│   │   ├── cassandra_truststore.jks
│   │   ├── sf-class2-root.crt
│   │   └── temp_file.der
```

This folder contains the source code for all the Database, like db_connector.py, db_get_data.py, and resources.
db_connector.py - A Python script for managing database connections and operations.
db_get_data.py - A Python script for executing CQL to get relevant data.
resources/ - Certificates needed to connect AWS Cassandra database.

```
├── backend
│   ├── Prediction
│   │   ├── MLP.py
│   │   ├── MLP_oversample.py
│   │   ├── Predict.py
│   │   ├── gen_city_mapping.py
│   │   ├── get_importance.py
│   │   ├── ...
│   │   ├── models
│   │   │     └── ...
```

This folder contains the source code for model training, testing, and related tools for our machine learning section.
Details are as follows:
MLP.py - Train MLP Classifier (w/o oversampling).
MLP_oversample.py - Train MLP Classifier (with oversampling).
Predict.py - Load the trained model and predict results based on the input data.
gen_city_mapping.py - Retrieve the mapping from airport codes to their corresponding geographical coordinates.
get_importance.py - Retrieve the importance of different features in the random forest model.
models/ - This folder contains trained models.
