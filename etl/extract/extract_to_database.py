import os

import requests
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import InternalError

from config.db_config import DatabaseConfigError, load_db_config
from utils.db_utils import DatabaseConnectionError, get_db_connection

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

SOURCE_TABLE_NAME = "current_weather_mh_de11"
BASE_URL = "http://api.weatherapi.com/v1"

url = f"{BASE_URL}/current.json?key={weather_api_key}&q=New_York&aqi=yes"

response_json = requests.get(url)
response_data = response_json.json()

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
create_table_sql = text(
    """
    CREATE TABLE IF NOT EXISTS student.current_weather_mh_de11 (
        id SERIAL PRIMARY KEY,
        location_name TEXT NOT NULL,
        region TEXT,
        country TEXT,
        latitude FLOAT,
        longitude FLOAT,
        local_time TIMESTAMP,
        temp_c FLOAT,
        temp_f FLOAT,
        condition TEXT,
        wind_mph FLOAT,
        wind_kph FLOAT,
        wind_degree INT,
        wind_dir TEXT,
        pressure_mb FLOAT,
        humidity INT,
        cloud INT,
        feelslike_c FLOAT,
        feelslike_f FLOAT,
        air_quality_co FLOAT,
        air_quality_no2 FLOAT,
        air_quality_o3 FLOAT,
        air_quality_so2 FLOAT,
        air_quality_pm2_5 FLOAT,
        air_quality_pm10 FLOAT,
        air_quality_us_epa_index INT,
        air_quality_gb_defra_index INT,
        UNIQUE(location_name, local_time)  -- Prevents duplicate weather entries for same location & time
    );
"""
)

# SQL Query for insert or update
insert_sql = text(
    """
    INSERT INTO student.current_weather_mh_de11 (
        location_name, region, country, latitude, longitude, local_time,
        temp_c, temp_f, condition, wind_mph, wind_kph, wind_degree, wind_dir,
        pressure_mb, humidity, cloud, feelslike_c, feelslike_f,
        air_quality_co, air_quality_no2, air_quality_o3, air_quality_so2,
        air_quality_pm2_5, air_quality_pm10, air_quality_us_epa_index, air_quality_gb_defra_index
    )
    VALUES (
        :location_name, :region, :country, :latitude, :longitude, :local_time,
        :temp_c, :temp_f, :condition, :wind_mph, :wind_kph, :wind_degree, :wind_dir,
        :pressure_mb, :humidity, :cloud, :feelslike_c, :feelslike_f,
        :air_quality_co, :air_quality_no2, :air_quality_o3, :air_quality_so2,
        :air_quality_pm2_5, :air_quality_pm10, :air_quality_us_epa_index, :air_quality_gb_defra_index
    )
    ON CONFLICT (location_name, local_time)
    DO UPDATE SET
        temp_c = EXCLUDED.temp_c,
        temp_f = EXCLUDED.temp_f,
        condition = EXCLUDED.condition,
        wind_mph = EXCLUDED.wind_mph,
        wind_kph = EXCLUDED.wind_kph,
        wind_degree = EXCLUDED.wind_degree,
        wind_dir = EXCLUDED.wind_dir,
        pressure_mb = EXCLUDED.pressure_mb,
        humidity = EXCLUDED.humidity,
        cloud = EXCLUDED.cloud,
        feelslike_c = EXCLUDED.feelslike_c,
        feelslike_f = EXCLUDED.feelslike_f,
        air_quality_co = EXCLUDED.air_quality_co,
        air_quality_no2 = EXCLUDED.air_quality_no2,
        air_quality_o3 = EXCLUDED.air_quality_o3,
        air_quality_so2 = EXCLUDED.air_quality_so2,
        air_quality_pm2_5 = EXCLUDED.air_quality_pm2_5,
        air_quality_pm10 = EXCLUDED.air_quality_pm10,
        air_quality_us_epa_index = EXCLUDED.air_quality_us_epa_index,
        air_quality_gb_defra_index = EXCLUDED.air_quality_gb_defra_index;
"""
)

# Execute table creation (if it does not already exist) and Insert/Update data into table
try:
    connection_details = load_db_config()["source_database"]
    connection = get_db_connection(connection_details)
    with connection:
        connection.execute(create_table_sql)
        connection.execute(insert_sql, weather_record)
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
