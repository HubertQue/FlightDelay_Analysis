import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime
import json


def data_processing(df_raw, encoder_path='', scaler_path=None):
    loaded_encoder = joblib.load(encoder_path)
    columns_to_encode = ['DAY_OF_WEEK', 'DEP_HOUR', 'MONTH']
    data_encoded = loaded_encoder.transform(df_raw[columns_to_encode])
    df_encoded = pd.DataFrame(data_encoded, columns=loaded_encoder.get_feature_names_out(columns_to_encode))
    df_encoded = pd.concat([df_raw, df_encoded], axis=1)
    df_encoded.drop(columns_to_encode, axis=1, inplace=True)
    if scaler_path is not None:
        loaded_scaler = joblib.load(scaler_path)
        df_scaled = loaded_scaler.transform(df_encoded)
    else:
        df_scaled = df_encoded
    return df_scaled


def prediction_mlp(df_transformed, model_path=''):
    model_loaded = joblib.load(model_path)
    prediction = model_loaded.predict(df_transformed)
    probability = model_loaded.predict_proba(df_transformed)
    return (prediction, probability)


def evaluate_model(data_raw, model_type='mlp', encoder_path='.\\mlp_cls_encoder.joblib', scaler_path=None, model_path='.\\mlp_cls.joblib'):
    df_raw = pd.DataFrame(data_raw)
    df_transformed = data_processing(df_raw, encoder_path=encoder_path, scaler_path=scaler_path)
    if model_type == 'mlp':
        res = prediction_mlp(df_transformed, model_path=model_path)
    elif False:
        res = (0, 0) # todo
    return res


def json_to_row(data_json):
    date_object = datetime.strptime(data_json['date'], '%Y-%m-%d')
    weekday = date_object.weekday() + 1
    month = int(date_object.strftime('%m'))

    def get_geographical_info(airport_id, mapping_file_path):
        airport_mapping = {}
        with open(mapping_file_path, 'r') as json_file:
            airport_mapping = json.load(json_file)
        if airport_id in airport_mapping:
            latitude = airport_mapping[airport_id]['LATITUDE']
            longitude = airport_mapping[airport_id]['LONGITUDE']
            elevation = airport_mapping[airport_id]['ELEVATION']
        else:
            return (None, None, None)
        return (latitude, longitude, elevation)

    airport_name = data_json['airport']
    mapping_file_path = 'airport_data.json'
    latitude, longitude, elevation= get_geographical_info(airport_name, mapping_file_path=mapping_file_path)
    if latitude is None:
        return (None, False)

    visib = data_json['visibility']
    weatherConditions = data_json['weatherConditions']

    def get_visibility(data):
        if data == 'high':
            return 2
        elif data == 'medium':
            return 1
        elif data == 'low':
            return 0
        else:
            return -1

    res = {'DAY_OF_WEEK': [weekday], 'DEP_HOUR': [data_json['hour'].zfill(2)], 'MONTH':[month], 'LATITUDE': [latitude],'LONGITUDE': [longitude], 'ELEVATION': [elevation], 'TEMP':[float(data_json['AveT'])], 'VISIB':[get_visibility(vis)], 'MAX':[float(data_json['MaxT'])], 'MIN':[float(data_json['MinT'])], 'Fog':[int(weatherConditions['Fog'])], 'Rain or Drizzle':[int(weatherConditions['Rain'])], 'Snow or Ice Pellets':[int(weatherConditions['Snow'])], 'Hail':[int(weatherConditions['Hail'])], 'Thunder':[int(weatherConditions['Thunder'])], 'Tornado or Funnel Cloud':[int(weatherConditions['Tornado'])]}
    # res = {'DAY_OF_WEEK': [3], 'DEP_HOUR': ['03'], 'MONTH':[10], 'LATITUDE': [33.3],'LONGITUDE': [-144.4], 'ELEVATION': [4.5], 'TEMP':[15.0], 'VISIB':[1], 'MAX':[20.0], 'MIN':[10.0], 'Fog':[0], 'Rain or Drizzle':[0], 'Snow or Ice Pellets':[0], 'Hail':[0], 'Thunder':[0], 'Tornado or Funnel Cloud':[0]}
    return (res, True)


def predict_delay(data_jsno={}):
    (data_test, flag) = json_to_row(data_json)
    flag = True
    if flag:
        prediction, probability = evaluate_model(data_test, model_type='mlp',
                                                 encoder_path='models\\mlp_os_cls_encoder.joblib',
                                                 scaler_path='models\\mlp_os_cls_scaler.joblib',
                                                 model_path='models\\mlp_os_cls.joblib')
        prediction = prediction[0]
        probability = probability[0][prediction]
    else:
        prediction = -1
        probability = -1
    return (prediction, probability)


if __name__ == '__main__':
    data_test = {'DAY_OF_WEEK': [3], 'DEP_HOUR': ['03'], 'MONTH': [10], 'LATITUDE': [33.3], 'LONGITUDE': [-144.4],
                       'ELEVATION': [4.5], 'TEMP': [15.0], 'VISIB': [1], 'MAX': [20.0], 'MIN': [10.0], 'Fog': [0],
                       'Rain or Drizzle': [0], 'Snow or Ice Pellets': [0], 'Hail': [0], 'Thunder': [0],
                       'Tornado or Funnel Cloud': [0]}
    # data_test = json_to_row(data_json)
    prediction, probability = evaluate_model(data_test, model_type='mlp', encoder_path='models\\mlp_os_cls_encoder.joblib', scaler_path='models\\mlp_os_cls_scaler.joblib', model_path='models\\mlp_os_cls.joblib')
    print('Prediction is:', prediction)
    print('Probability is:', probability)
