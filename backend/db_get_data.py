from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra import ConsistencyLevel
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
import os
import json





# Function to create a Cassandra session
def create_session():
    contact_point = "cassandra.us-west-2.amazonaws.com"
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    cert_path = os.path.join(os.path.dirname(__file__), 'resources/sf-class2-root.crt')
    ssl_context.load_verify_locations(cert_path)
    ssl_context.verify_mode = CERT_REQUIRED

    with open('../../../credential/credentials.json', 'r') as file:
        credentials = json.load(file)

    auth_provider = PlainTextAuthProvider(username='twhitlock-at-697306959183', password=credentials["password"])
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.LOCAL_QUORUM)

    cluster = Cluster(contact_points=[contact_point], port=9142, auth_provider=auth_provider, ssl_context=ssl_context,
                      execution_profiles={EXEC_PROFILE_DEFAULT: profile})

    session = cluster.connect()

    return session



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
    table_name = 'Graph_6_Top10_States'
    columns = query_table_and_convert_to_column_lists(table_name)
    print(columns)

if __name__ == "__main__":
    main()