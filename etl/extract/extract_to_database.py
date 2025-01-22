import os

import requests
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import InternalError

from config.db_config import DatabaseConfigError, load_db_config
from utils.db_utils import DatabaseConnectionError, get_db_connection
from utils.sql_utils import import_sql_query
from utils.request_utils import get_url

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

SOURCE_TABLE_NAME = "current_weather_mh_de11"
BASE_URL = "http://api.weatherapi.com/v1"

url = f"{BASE_URL}/current.json?key={weather_api_key}&q=New_York&aqi=yes"
response_data = get_url(url).json()

# Extract Relevant Data
location = response_data["location"]
current = response_data["current"]
condition = current["condition"]
air_quality = current["air_quality"]
weather_record = {
    "location_name": location["name"],
    "region": location["region"],
    "country": location["country"],
    "latitude": location["lat"],
    "longitude": location["lon"],
    "local_time": location["localtime"],
    "temp_c": current["temp_c"],
    "temp_f": current["temp_f"],
    "condition": condition["text"],
    "wind_mph": current["wind_mph"],
    "wind_kph": current["wind_kph"],
    "wind_degree": current["wind_degree"],
    "wind_dir": current["wind_dir"],
    "pressure_mb": current["pressure_mb"],
    "humidity": current["humidity"],
    "cloud": current["cloud"],
    "feelslike_c": current["feelslike_c"],
    "feelslike_f": current["feelslike_f"],
    "air_quality_co": air_quality["co"],
    "air_quality_no2": air_quality["no2"],
    "air_quality_o3": air_quality["o3"],
    "air_quality_so2": air_quality["so2"],
    "air_quality_pm2_5": air_quality["pm2_5"],
    "air_quality_pm10": air_quality["pm10"],
    "air_quality_us_epa_index": air_quality["us-epa-index"],
    "air_quality_gb_defra_index": air_quality["gb-defra-index"],
}

# SQL to create table
create_current_weather_table_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/create_current_weather_table.sql"
)
create_current_weather_table_sql = text(
    import_sql_query(create_current_weather_table_sql_file_path, remove_newlines=False)
)

# SQL Query for insert or update
insert_current_weather_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/insert_current_weather.sql"
)
insert_current_weather_sql = text(
    import_sql_query(insert_current_weather_sql_file_path, remove_newlines=False)
)

# Execute table creation (if it does not already exist) and Insert/Update data into table
try:
    connection_details = load_db_config()["source_database"]
    connection = get_db_connection(connection_details)
    with connection:
        connection.execute(create_current_weather_table_sql)
        connection.execute(insert_current_weather_sql, weather_record)
        connection.commit()
        print("Table exists and has successfully been updated.")
except InternalError:
    print("Source table exists")
    raise
except DatabaseConfigError as e:
    print(f"Source database not configured correctly: {e}")
    raise
except DatabaseConnectionError as e:
    f"Failed to connect to the database when creating the table:"
    f" {e}"
    raise
