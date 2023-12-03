#!/usr/bin/env python
# coding: utf-8
import os
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Data processing: Weather Data Merge & Clean')
parser.add_argument('-a', '--airport', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='airport file path')
parser.add_argument('-w', '--weather', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='weather file path')
parser.add_argument('-m', '--mapping', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='id-mapping file path')
parser.add_argument('-o', '--output', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='output file path')
parser.add_argument('-y', '--year', default=2020, help='data of which year?')
args = parser.parse_args()

df_airport = pd.read_csv(os.path.join(args.airport, 'airport-%s-cleaned.csv' % args.year))
df_weather = pd.read_csv(os.path.join(args.weather, 'weather_%s.csv' % args.year))
df_code = pd.read_csv(os.path.join(args.mapping, 'id_mapping.csv'), dtype={'WBAN_ID': str})

df_weather['STATION'] = df_weather['STATION'].astype(str).str[-5:]
weather_code_df = pd.merge(df_weather, df_code, left_on='STATION', right_on='WBAN_ID', how='inner')

weather_code_df['DATE'] = pd.to_datetime(weather_code_df['DATE'])
weather_code_df['MONTH'] = weather_code_df['DATE'].dt.month
weather_code_df['DATE'] = weather_code_df['DATE'].dt.strftime('%Y-%m-%d')

final_df = pd.merge(
    df_airport,
    weather_code_df,
    how='inner',
    left_on=['ORIGIN', 'FL_DATE'],
    right_on=['CALL_SIGN', 'DATE'])
final_df.to_csv(os.path.join(args.output, 'airport_weather_%s.csv' % args.year), index=False)

#final_df = final_df.dropna()
#pearson_corr = final_df.corr(method='pearson')['DEP_DELAY'].sort_values(ascending=False)
#print(pearson_corr)
#corr = final_df.corr()['DEP_DELAY'].sort_values(ascending=False)
#print(corr)
