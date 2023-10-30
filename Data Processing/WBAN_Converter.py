import pandas as pd


def merge_and_process_data(wban_file, airport_file):
    # read inputs
    df_WBAN = pd.read_csv(wban_file)
    np_airport = pd.read_csv(airport_file)['ORIGIN'].unique()
    df_airport = pd.DataFrame(np_airport, columns=['ORIGIN'])
    # print(df_airport.dtype())
    print('count:', len(df_airport))

    # choose 'WBAN_ID' and 'CALL_SIGN' column
    df_WBAN = df_WBAN[['WBAN_ID', 'CALL_SIGN']]
    print("Initial WBAN DataFrame length:", len(df_WBAN))

    # filter out rows where 'CALL_SIGN' is NaN
    df_WBAN = df_WBAN[~df_WBAN['CALL_SIGN'].isna()]
    print("WBAN DataFrame length without NaN in 'CALL_SIGN':", len(df_WBAN))

    # join two tables
    result = pd.merge(df_airport, df_WBAN, left_on='ORIGIN', right_on='CALL_SIGN')
    print("\nDataFrame Merged.")

    # autofill WBAN_ID to 5 digits
    result['WBAN_ID'] = result['WBAN_ID'].astype(str)
    print("Data type of 'WBAN_ID' after conversion:", result['WBAN_ID'].dtype)
    result['WBAN_ID'] = result['WBAN_ID'].str.zfill(5)

    # result.to_csv(output_file, index=False)
    print(f"\nResults have been returned.")
    return result.drop(columns=['ORIGIN'])


def get_station_id(wban_to_wmo_csv, sign_wban_df):
    # df = pd.read_csv('data.csv')
    opening_rows = 5
    raw_df = pd.read_csv(wban_to_wmo_csv, encoding='latin1', dtype=str,skiprows=range(opening_rows))
    print('Read WBAN mapping file.')
    mapping_columns = raw_df.loc[:, ['wmo', 'wban']]  # .loc() can avoid SettingWithCopyWarning
    # mapping_columns['wban'] = mapping_columns['wban'].astype(str)
    mapping_columns['wban'] = mapping_columns['wban'].str.zfill(5)
    # mapping_columns['wmo'] = mapping_columns['wmo'].astype(str)
    mapping_columns['wmo'] = mapping_columns['wmo'].str.zfill(6)
    print("Data type of 'wmo' after conversion:", mapping_columns['wmo'].dtype)

    merged_df = pd.merge(mapping_columns, sign_wban_df, left_on='wban', right_on='WBAN_ID')
    print('merged_count:', len(merged_df))

    merged_df['stationID'] = merged_df['wmo'] + merged_df['wban']
    id_mapping = merged_df.loc[:, ['CALL_SIGN', 'stationID']]
    # print('ID mapper count:', len(id_mapping))
    print(id_mapping.head(100))
    return id_mapping


# sign_to_stationID (csv/json)
# ['sign', 'stationID']


airport_delay_csv = 'data/airport_delay.csv'
sign_to_WBAN_csv = 'data/WBAN.csv'
WBAN_to_WMO_csv = 'data/master-location-identifier-database-202307_standard.csv'
output_mapper_csv = 'airport_delay_final.csv'

sign_WBAN_df = merge_and_process_data(sign_to_WBAN_csv, airport_delay_csv)
sign_stationID_df = get_station_id(WBAN_to_WMO_csv, sign_WBAN_df)
