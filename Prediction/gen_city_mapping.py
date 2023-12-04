import pandas as pd
import json

csv_file_paths = ['E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\airport_weather_2020.csv', 'E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\airport_weather_2021.csv', ]
# csv_file_paths = ['E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\airport_weather_2020.csv', 'E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\airport_weather_2021.csv', 'E:\\SFU\\classes\\CMPT-732\\Project\\get_data\\airport_weather_2022.csv']

# get geographical info
airport_data_merged = None
for csv_file in csv_file_paths:
    df = pd.read_csv(csv_file)
    airport_data = df[['ORIGIN', 'LATITUDE', 'LONGITUDE', 'ELEVATION']].drop_duplicates()
    airport_data = airport_data.drop_duplicates(subset='ORIGIN')
    if airport_data_merged is None:
        airport_data_merged = airport_data
    else:
        airport_data_merged = pd.concat([airport_data_merged, airport_data], ignore_index=True)
airport_data_merged = airport_data_merged.drop_duplicates(subset='ORIGIN')
airport_dict = airport_data_merged.set_index('ORIGIN').to_dict(orient='index')
print(airport_dict)

# save as JSON mapping file
json_file_path = '.\\airport_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(airport_dict, json_file, indent=2)

print(f'Mapping JSON file has been successfully stored in: {json_file_path}')
