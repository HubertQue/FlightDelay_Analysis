import os
import pandas as pd

data_dir = 'E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\2020'
output_file = 'E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\full_2020.csv'

df_list = []

files = os.listdir(data_dir)
for file in files:
    if not os.path.isdir(file) and os.path.splitext(file)[-1] == '.csv':
        file_path = os.path.join(data_dir, file)
        df_list.append(pd.read_csv(file_path))

df_merged = pd.concat(df_list, ignore_index=True)
df_merged = df_merged.drop('LATITUDE', axis=1)
df_merged = df_merged.drop('LONGITUDE', axis=1)
df_merged = df_merged.drop('TEMP_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('DEWP_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('SLP', axis=1)
df_merged = df_merged.drop('SLP_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('STP', axis=1)
df_merged = df_merged.drop('STP_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('VISIB_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('WDSP_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('GUST', axis=1)
df_merged = df_merged.drop('MAX_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('MIN_ATTRIBUTES', axis=1)
df_merged = df_merged.drop('PRCP_ATTRIBUTES', axis=1)
df_merged.to_csv(output_file, index=False)