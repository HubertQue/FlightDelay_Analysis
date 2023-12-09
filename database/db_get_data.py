from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra import ConsistencyLevel
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
import os
import json





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



def query_table_and_convert_to_column_lists(table_name):
    keyspace_name = 'flightdb'
    session = create_session()
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


def main():
    # Create a Cassandra session

    #session = create_session()
    #your_keyspace = 'flightdb'
    table_name = 'Graph_4_Hour_2021'
    columns = query_table_and_convert_to_column_lists(table_name)
    print(columns)

if __name__ == "__main__":
    main()