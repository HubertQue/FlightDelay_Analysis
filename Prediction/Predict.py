import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib


def data_processing(df_raw, encoder_path='', scaler_path=None):
    loaded_encoer = joblib.load(encoder_path)
    columns_to_encode = ['DAY_OF_WEEK', 'DEP_HOUR', 'MONTH']
    df_encoded = loaded_encoer.transform(raw_df[columns_to_encode])
    if scaler_path is not None:
        loaded_scaler = joblib.load(scaler_path)
        df_scaled = loaded_scaler.transform(df)
    else:
        df_scaled = df_encoded
    return df_scaled


def prediction_mlp(df_transformed, model_path=''):
    model_loaded = joblib.load(model_path)
    y_pred = model_loaded.predict(df_transformed)
    return y_pred


def main(data_raw, model_type='mlp', encoder_path='', scaler_path=None, model_path=''):
    df_raw = pd.DataFrame(data_raw)
    df_transformed = data_processing(df_raw, encoder_path=encoder_path, scaler_path=scaler_path)
    if model_type == 'mlp':
        res = prediction_mlp(df_transformed, model_path=model_path)
    elif:
        res = 0 # todo
    return res


data_test = {'DAY_OF_WEEK': [3], 'DEP_HOUR': [20], 'ELEVATION': [1200.0], 'TEMP':[], 'DEWP':[], 'VISIB':[], 'WDSP':[], 'MXSPD':[], 'MAX':[], 'MIN':[], 'Fog':[], 'Rain or Drizzle':[], 'Snow or Ice':[], 'Pellets':[], 'Hail':[], 'Thunder':[], 'Tornado or Funnel':[], 'Cloud':[], 'MONTH':[]}
ans = main(data_test, model_type='mlp', encoder_path='xxx', scaler_path=None, model_path='xxx')
print(ans)
