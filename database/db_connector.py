
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
import os
import json
import csv
import subprocess
import re
import time



# Function to create a Cassandra session


def create_session():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.load_verify_locations(os.path.join(os.path.dirname(__file__), 'resources/sf-class2-root.crt'))
    ssl_context.verify_mode = CERT_REQUIRED

    #pw_file = open('../../../credential/credentials.json', 'r')
    pw_file = open('./credentials.json', 'r')
    login_info = json.load(pw_file)
    if pw_file:
        pw_file.close()
    auth_provider = PlainTextAuthProvider(username='twhitlock-at-697306959183', password=login_info["password"])
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
    contact_endpoint = "cassandra.us-west-2.amazonaws.com"
    default_db_port = 9142
    db_cluster = Cluster(contact_points=[contact_endpoint], port=default_db_port, auth_provider=auth_provider, ssl_context=ssl_context,
                      execution_profiles={EXEC_PROFILE_DEFAULT: profile})

    return db_cluster.connect()

'''

def create_session():
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    cert_path = os.path.join(os.path.dirname(__file__), 'resources/sf-class2-root.crt')
    ssl_context.load_verify_locations(cert_path)
    ssl_context.verify_mode = CERT_REQUIRED

    with open('../../../credential/credentials.json', 'r') as file:
        credentials = json.load(file)

    auth_provider = PlainTextAuthProvider(username='twhitlock-at-697306959183', password=credentials["password"])
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
    contact_endpoint = "cassandra.us-west-2.amazonaws.com"
    default_db_port = 9142
    db_cluster = Cluster(contact_points=[contact_endpoint], port=default_db_port, auth_provider=auth_provider, ssl_context=ssl_context,
                      execution_profiles={EXEC_PROFILE_DEFAULT: profile})
    return db_cluster.connect()

'''


def query_table_and_convert_to_column_lists(session, keyspace_name, table_name):
    try:
        query = f"SELECT * FROM {keyspace_name}.{table_name}"
        rows = session.execute(query)

        # Determine column names and create an empty list for each column
        columns = {col: [] for col in rows.column_names}

        # Iterate over the results and populate the data
        for row in rows:
            for col in rows.column_names:
                columns[col].append(getattr(row, col))

        return columns
    except Exception as e:
        print(f"Error querying table {table_name}: ", e)
        return {}


def drop_all_tables_in_keyspace(session, keyspace_name):
    try:
            # get all the table
        query = f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{keyspace_name}'"
        result = session.execute(query)

            # delete every table
        for row in result:
            table_name = row.table_name
            try:
                query = f"DROP TABLE IF EXISTS {keyspace_name}.{table_name}"
                session.execute(query)
                print(f"Table '{table_name}' has been dropped.")
            except Exception as e:
                print(f"Error dropping table {table_name}: ", e)

    except Exception as e:
        print(f"Error connecting to Cassandra: ", e)




def create_tables(session, keyspace_name, tables_info):
    # List to keep track of created tables

    created_table = [];
    # Iterate over table names and their corresponding structures

    for table_name, table_structure in tables_info.items():
        try:
            query = f"CREATE TABLE IF NOT EXISTS {keyspace_name}.{table_name} ({', '.join(table_structure)})"

            session.execute(query)
            print(f"Table {table_name} created successfully.")
            created_table.append(table_name)
            time.sleep(15)
        except Exception as e:
            print(f"Error creating table {table_name}: ", e)
    return created_table



def get_csv_headers(csv_file_path):
    # Open the CSV file in reading mode with specified encoding
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        # Create a CSV reader for the file
        reader = csv.reader(csvfile)
        headers = next(reader, None)
    # Return the extracted headers
    return headers


def build_tables_info(csv_folder_path, graph_dic, type_mapping, column_dic):
    tables_info = {}
    for key, value in graph_dic.items():
        filename = key
        column_list = value
        #print(filename)
        csv_file_path = os.path.join(csv_folder_path, filename)
        headers = get_csv_headers(csv_file_path)
        table_name = filename.split('.')[0]
        primary_key_columns = column_dic[key]
        columns_info = []

        # Determine the primary key columns
        primary_key = None
        if primary_key_columns is not None:
            primary_key = ", ".join([headers[i] for i in primary_key_columns])

        # Add the columns with data types
        for j in range(len(column_list)):
            columns_info.append(f"{headers[j]} {type_mapping[column_list[j]]}")
        # Add the primary key information to the columns
        columns_info.append(f"PRIMARY KEY ({primary_key})")
        tables_info[table_name] = columns_info

    return tables_info








def import_csv_to_cassandra(session, keyspace_name, table_name, csv_file_path, current_type_list):
    # Open the CSV file for reading

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Iterate over each row in the CSV file

        for row in reader:
            # Convert data types based on the provided type list

            for j in range(len(current_type_list)):
                if current_type_list[j] == 'int':
                    row[reader.fieldnames[j]] = int(row[reader.fieldnames[j]])
                elif current_type_list[j] == 'string':
                    row[reader.fieldnames[j]] = str(row[reader.fieldnames[j]])
                elif current_type_list[j] == 'float':
                    row[reader.fieldnames[j]] = float(row[reader.fieldnames[j]])

                columns = ', '.join(row.keys())
                placeholders = ', '.join(['%s'] * len(row))
                query = f"INSERT INTO {keyspace_name}.{table_name} ({columns}) VALUES ({placeholders})"

            try:
                # Sleep for a short duration to avoid overloading Cassandra

                time.sleep(1)
                # Execute the INSERT query with row values

                session.execute(query, list(row.values()))
                #print(table_name)
                #print(f"Inserted row successful: {row}")
            except Exception as e:
                print(table_name)
                print(f"Error occurred: {e}")



def main():
    # Create a Cassandra session

    session = create_session()
    your_keyspace = 'flightdb'
    csv_file_path = ('../Data_Analyzing/CSV Files/')

    graph_dic = {'Graph_1_Year.csv': ['int', 'int', 'float'], 'Graph_2_Month_2020.csv': ['string', 'int', 'float'],'Graph_2_Month_2021.csv': ['string', 'int', 'float'],'Graph_2_Month_2022.csv': ['string', 'int', 'float'],
     'Graph_3_Weekday_2020.csv': ['string', 'int', 'float'], 'Graph_3_Weekday_2021.csv': ['string', 'int', 'float'],'Graph_3_Weekday_2022.csv': ['string', 'int', 'float'],'Graph_4_Hour_2020.csv':['int', 'int', 'float'], 'Graph_4_Hour_2021.csv':['int', 'int', 'float'],'Graph_4_Hour_2022.csv':['int', 'int', 'float'],
     'Graph_5_State.csv': ['string', 'int', 'float'], 'Graph_6_Top10_States.csv': ['string', 'string', 'int', 'float'],
     'Graph_7_City.csv': ['string', 'int', 'float'], 'Graph_8_Top20_Cities.csv': ['string', 'string', 'int', 'float'],
     'Graph_9_Elevation.csv': ['int', 'int', 'float'], 'Graph_10_Temp.csv': ['int', 'int', 'float'],
     'Graph_11_DEWP.csv': ['int', 'int', 'float'], 'Graph_12_VISIB.csv': ['float', 'int', 'float'],
     'Graph_13_VISIB_Category.csv': ['string', 'int', 'float'],
     'Graph_14_VISIB_States.csv': ['string', 'string', 'int', 'float'],
     #'Graph_15_VISIB_Cities.csv': ['string', 'string', 'int', 'float'],
     'Graph_16_WDSP.csv': ['int', 'int', 'float'],
     'Graph_17_MXSPD.csv': ['int', 'int', 'float'], 'Graph_18_PRCP.csv': ['int', 'int', 'float'],
     'Graph_19_SNDP.csv': ['int', 'int', 'float'], 'Graph_20_Fog.csv': ['int', 'int', 'float'],
     'Graph_21_Rain_Drizzle.csv': ['int', 'int', 'float'], 'Graph_22_Snow_Ice_Pellets.csv': ['int', 'int', 'float'],
     'Graph_23_Hail.csv': ['int', 'int', 'float'], 'Graph_24_Thunder.csv': ['int', 'int', 'float'],
     'Graph_25_Tornado_Funnel_Cloud.csv': ['int', 'int', 'float']}

    column_dic = {'Graph_1_Year.csv': [0], 'Graph_2_Month_2020.csv': [0], 'Graph_2_Month_2021.csv': [0], 'Graph_2_Month_2022.csv': [0],
                 'Graph_3_Weekday_2020.csv': [0], 'Graph_3_Weekday_2021.csv': [0],'Graph_3_Weekday_2022.csv': [0],'Graph_4_Hour_2020.csv':[0], 'Graph_4_Hour_2021.csv':[0],'Graph_4_Hour_2022.csv':[0],
                 'Graph_5_State.csv': [0],
                 'Graph_6_Top10_States.csv': [0, 1],
                 'Graph_7_City.csv': [0],
                 'Graph_8_Top20_Cities.csv': [0, 1],
                 'Graph_9_Elevation.csv': [0], 'Graph_10_Temp.csv': [0],
                 'Graph_11_DEWP.csv': [0], 'Graph_12_VISIB.csv': [0],
                 'Graph_13_VISIB_Category.csv': [0],
                 'Graph_14_VISIB_States.csv': [0, 1],
                 #'Graph_15_VISIB_Cities.csv': [0, 1],
                 'Graph_16_WDSP.csv': [0],
                 'Graph_17_MXSPD.csv': [0], 'Graph_18_PRCP.csv': [0],
                 'Graph_19_SNDP.csv': [0], 'Graph_20_Fog.csv': [0],
                 'Graph_21_Rain_Drizzle.csv': [0],
                 'Graph_22_Snow_Ice_Pellets.csv': [0],
                 'Graph_23_Hail.csv': [0], 'Graph_24_Thunder.csv': [0],
                 'Graph_25_Tornado_Funnel_Cloud.csv': [0]}

    type_mapping = {
        'string': 'text',
        'int': 'int',
        'float': 'double'
    }



    #testing, delete all the tables before creating tables
    drop_all_tables_in_keyspace(session, your_keyspace)
    #create the column structure based on the csv files
    tables_info = build_tables_info(csv_file_path, graph_dic, type_mapping, column_dic)



    # create tables
    created_table = create_tables(session, your_keyspace, tables_info)
    time.sleep(120)
    for m in range(len(created_table)):
        table_name = created_table[m]
        print(f'{table_name}, is in processing')

        csv_file_path_current = os.path.join(csv_file_path, f"{table_name}.csv")
        import_csv_to_cassandra(session, your_keyspace, table_name, csv_file_path_current, graph_dic[f"{table_name}.csv"])
        columns = query_table_and_convert_to_column_lists(session, your_keyspace, table_name)
        print(columns)






# Define the main function
if __name__ == "__main__":
    main()





