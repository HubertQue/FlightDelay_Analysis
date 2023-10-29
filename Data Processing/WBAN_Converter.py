import pandas as pd

def merge_and_process_data(wban_file, airport_file, output_file):
    # read inputs
    df_WBAN = pd.read_csv(wban_file)
    df_airport = pd.read_csv(airport_file)

    # choose 'WBAN_ID' and 'CALL_SIGN' column
    df_WBAN = df_WBAN[['WBAN_ID', 'CALL_SIGN']]
    print("Initial WBAN DataFrame length:", len(df_WBAN))

    # filter out rows where 'CALL_SIGN' is NaN
    df_WBAN = df_WBAN[~df_WBAN['CALL_SIGN'].isna()]
    print("WBAN DataFrame length without NaN in 'CALL_SIGN':", len(df_WBAN))

    # join two tables
    result = pd.merge(df_airport, df_WBAN, left_on='ORIGIN', right_on='CALL_SIGN')
    print("\nMerged DataFrame:")

    # autofill WBAN_ID to 5 digits
    result['WBAN_ID'] = result['WBAN_ID'].astype(str)
    print("Data type of 'WBAN_ID' after conversion:", result['WBAN_ID'].dtype)
    result['WBAN_ID'] = result['WBAN_ID'].str.zfill(5)

    # Outputs into new file
    result.to_csv(output_file, index=False)
    print(f"\nResults have been written to '{output_file}'.")

# Use the function
merge_and_process_data('WBAN.csv', 'airport_delay.csv', 'airport_delay_new.csv')

