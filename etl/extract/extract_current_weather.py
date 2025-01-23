import os

from config.db_config import load_db_config
from utils.db_utils import get_db_connection
from utils.sql_utils import import_sql_query
from etl.extract.extract_query import execute_extract_query

extract_current_weather_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/extract_current_weather.sql"
)


def extract_current_weather_data():
    connection_details = load_db_config()["source_database"]
    connection = get_db_connection(connection_details)

    query = import_sql_query(extract_current_weather_file_path)
    current_weather_df = execute_extract_query(query, connection)

    connection.close()
    return [current_weather_df]
