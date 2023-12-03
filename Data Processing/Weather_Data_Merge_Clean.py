import os
import pandas as pd
import argparse


def replace_by_zero(data_frame, attribute_name, value):
    data_frame[attribute_name] = data_frame[attribute_name].replace(value, 0)
    return data_frame

'''def split_columns(FRSHTT_code):
    FRSHTT_str = str(FRSHTT_code)
    return_list = []
    if FRSHTT_str[0] == '0':      #if the first digit is 0, there is no record for the specific weather type
        for i in range(7):
            return_list.append(None)
    elif FRSHTT_str[0] == '1':
            return_list.append('1')
            for i in range(len(FRSHTT_str)):
                return_list.append(FRSHTT_str[i])
            for j in range(6 - len(FRSHTT_str)):  # there are 7 columns to split, python stars with 0. the first one is if we have the weather records,
                return_list.append(None)
    else:
        print(FRSHTT_str)
        print('Special values in FRSHTT_str')
    return pd.Series(return_list)'''

def replace_datetime(data_frame, attribute_name=''):
    data_frame[attribute_name] = data_frame[attribute_name].replace(value, 0)
    return data_frame


def split_columns(FRSHTT_code):
    FRSHTT_str = str(FRSHTT_code)
    return_list = []
    if FRSHTT_str[0] == '0':      
        for i in range(6):
            return_list.append('0')
    elif FRSHTT_str[0] == '1':
            #return_list.append('1')
            for i in range(len(FRSHTT_str)):
                return_list.append(FRSHTT_str[i])
            for j in range(6 - len(FRSHTT_str)):  # there are 6 columns to split, 
                return_list.append(0)
    else:
        print(FRSHTT_str)
        print('Special values in FRSHTT_str')
    return pd.Series(return_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data processing: Weather Data Merge & Clean')
    parser.add_argument('-i', '--input_dir', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='input file dir')
    parser.add_argument('-o', '--output_dir', default='E:\\SFU\\classes\\CMPT-732\\Project\\get_data', help='output file dir')
    parser.add_argument('-y', '--year', default=2020, help='data of which year?')

    args = parser.parse_args()
    data_dir = os.path.join(args.input_dir, str(args.year))
    output_file = os.path.join(args.output_dir, 'weather_%s.csv' % str(args.year))

    df_list = []

    files = os.listdir(data_dir)
    for file in files:
        if not os.path.isdir(file) and os.path.splitext(file)[-1] == '.csv':
            file_path = os.path.join(data_dir, file)
            df_list.append(pd.read_csv(file_path))

    df_merged = pd.concat(df_list, ignore_index=True)

    required_columns = ['STATION', 'DATE', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME', 'TEMP', 'DEWP', 'VISIB', 'WDSP', 'MXSPD', 'MAX', 'MIN', 'PRCP', 'SNDP', 'FRSHTT']
    excluded_columns = ['TEMP_ATTRIBUTES', 'DEWP_ATTRIBUTES', 'SLP_ATTRIBUTES', 'STP_ATTRIBUTES', 'VISIB_ATTRIBUTES', 'WDSP_ATTRIBUTES', 'GUST', 'MAX_ATTRIBUTES', 'MIN_ATTRIBUTES', 'PRCP_ATTRIBUTES']
    optional_columns = ['SLP', 'STP',]

    #delete the optional_columns
    for i in range(len(optional_columns)):
        df_merged = df_merged.drop(optional_columns[i], axis=1)

    #delete the excluded_columns
    for i in range(len(excluded_columns)):
        df_merged = df_merged.drop(excluded_columns[i], axis=1)

    #------------clean data------------#

    ##------------replace with None------------##
    replace_list = [['TEMP', 9999.9], ['DEWP', 9999.9], ['VISIB', 999.9], ['WDSP', 999.9], ['MXSPD', 999.9], ['MAX', 9999.9], ['MIN', 9999.9], ['PRCP', 99.99], ['SNDP', 999.9]]

    for i in range(len(replace_list)):
        df_merged = replace_by_zero(df_merged, replace_list[i][0], replace_list[i][1])

    ##------------Split FRSHTT to 6 columns ------------##
    df_merged[['Fog', 'Rain or Drizzle', 'Snow or Ice Pellets', 'Hail','Thunder','Tornado or Funnel Cloud']] = df_merged['FRSHTT'].apply(split_columns)

    df_merged.to_csv(output_file, index=False)
    print(f'Weather data of year {args.year} merged.')
