import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import InternalError

from config.db_config import DatabaseConfigError, load_db_config
from utils.db_utils import DatabaseConnectionError, get_db_connection
from utils.request_utils import get_url
from utils.sql_utils import import_sql_query

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

BASE_URL = "http://api.weatherapi.com/v1"

url = f"{BASE_URL}/current.json?key={weather_api_key}&q=New_York&aqi=yes"
response_data = get_url(url).json()

# Extract Relevant Data
location = response_data["location"]
current = response_data["current"]
condition = current["condition"]
air_quality = current["air_quality"]
weather_record = {
    "local_time": location["localtime"],
    "location_name": location["name"],
    "region": location["region"],
    "country": location["country"],
    "lat": location["lat"],
    "lon": location["lon"],
    "tz_id": location["tz_id"],
    "localtime_epoch": location["localtime_epoch"],
    "last_updated_epoch": current["last_updated_epoch"],
    "last_updated": current["last_updated"],
    "temp_c": current["temp_c"],
    "temp_f": current["temp_f"],
    "is_day": current["is_day"],
    "condition_text": condition["text"],
    "condition_icon": condition["icon"],
    "condition_code": condition["code"],
    "wind_mph": current["wind_mph"],
    "wind_kph": current["wind_kph"],
    "wind_degree": current["wind_degree"],
    "wind_dir": current["wind_dir"],
    "pressure_mb": current["pressure_mb"],
    "pressure_in": current["pressure_in"],
    "precip_mm": current["precip_mm"],
    "precip_in": current["precip_in"],
    "humidity": current["humidity"],
    "cloud": current["cloud"],
    "feelslike_c": current["feelslike_c"],
    "feelslike_f": current["feelslike_f"],
    "windchill_c": current["windchill_c"],
    "windchill_f": current["windchill_f"],
    "heatindex_c": current["heatindex_c"],
    "heatindex_f": current["heatindex_f"],
    "dewpoint_c": current["dewpoint_c"],
    "dewpoint_f": current["dewpoint_f"],
    "vis_km": current["vis_km"],
    "vis_miles": current["vis_miles"],
    "uv": current["uv"],
    "gust_mph": current["gust_mph"],
    "gust_kph": current["gust_kph"],
    "co": air_quality["co"],
    "no2": air_quality["no2"],
    "o3": air_quality["o3"],
    "so2": air_quality["so2"],
    "pm2_5": air_quality["pm2_5"],
    "pm10": air_quality["pm10"],
    "us_epa_index": air_quality["us-epa-index"],
    "gb_defra_index": air_quality["gb-defra-index"],
}

# for key, value in weather_record.items():
#     if value is None:
#         weather_record[key] = 0 if isinstance(value, (int, float)) else ""

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
