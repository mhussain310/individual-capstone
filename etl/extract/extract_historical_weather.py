import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import InternalError

from config.dates_config import load_date_config
from config.db_config import DatabaseConfigError, load_db_config
from etl.extract.extract_query import execute_extract_query
from utils.db_utils import DatabaseConnectionError, get_db_connection
from utils.request_utils import get_url
from utils.sql_utils import import_sql_query

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

BASE_URL = "http://api.weatherapi.com/v1"

date_pairs = load_date_config()

# SQL to Create historical_weather_daily table
create_historical_weather_daily_table_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/create_historical_weather_daily_table.sql"
)
create_historical_weather_daily_table_sql = text(
    import_sql_query(
        create_historical_weather_daily_table_sql_file_path, remove_newlines=False
    )
)

# SQL to Create historical_weather_hourly table
create_historical_weather_hourly_table_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/create_historical_weather_hourly_table.sql"
)
create_historical_weather_hourly_table_sql = text(
    import_sql_query(
        create_historical_weather_hourly_table_sql_file_path, remove_newlines=False
    )
)

# SQL to insert/update rows in historical_weather_daily table
insert_historical_weather_daily_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/insert_historical_weather_daily.sql"
)
insert_historical_weather_daily_sql = text(
    import_sql_query(
        insert_historical_weather_daily_sql_file_path, remove_newlines=False
    )
)

# SQL to insert/update rows in historical_weather_hourly table
insert_historical_weather_hourly_sql_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/insert_historical_weather_hourly.sql"
)
insert_historical_weather_hourly_sql = text(
    import_sql_query(
        insert_historical_weather_hourly_sql_file_path, remove_newlines=False
    )
)

# SQL to extract hour historical weather data
extract_historical_weather_hourly_data_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/extract_historical_weather_hourly.sql"
)
extract_historical_weather_hourly_data_sql = import_sql_query(
    extract_historical_weather_hourly_data_file_path
)

# SQL to extract daily historical weather data
extract_historical_weather_daily_data_file_path = os.path.join(
    os.path.dirname(__file__), "../sql/extract_historical_weather_daily.sql"
)
extract_historical_weather_daily_data_sql = import_sql_query(
    extract_historical_weather_daily_data_file_path
)


def extract_historical_weather_data():
    add_historical_weather_data_to_db()

    connection_details = load_db_config()["source_database"]
    connection = get_db_connection(connection_details)

    hourly_historical_weather_df = execute_extract_query(
        extract_historical_weather_hourly_data_sql, connection
    )

    daily_historical_weather_df = execute_extract_query(
        extract_historical_weather_daily_data_sql, connection
    )

    connection.close()

    return [hourly_historical_weather_df, daily_historical_weather_df]


def add_historical_weather_data_to_db():
    try:
        weather_data_list = []
        for date_pair in date_pairs:
            url = f"{BASE_URL}/history.json?key={weather_api_key}&q=New_York&dt={date_pair[1]}&end_dt={date_pair[0]}"
            response_data = get_url(url).json()
            weather_data_list.append(response_data)

        connection_details = load_db_config()["source_database"]
        connection = get_db_connection(connection_details)

        # Create historical weather tables
        with connection as conn:
            conn.execute(create_historical_weather_daily_table_sql)
            conn.execute(create_historical_weather_hourly_table_sql)
            conn.commit()

        # Insert data into tables
        connection = get_db_connection(connection_details)
        with connection as conn:
            for weather_data in weather_data_list:
                location = weather_data["location"]
                for forecast in weather_data["forecast"]["forecastday"]:
                    conn.execute(
                        insert_historical_weather_daily_sql,
                        {
                            "date": forecast["date"],
                            "location_name": location["name"],
                            "location_region": location["region"],
                            "location_country": location["country"],
                            "location_lat": location["lat"],
                            "location_lon": location["lon"],
                            "location_tz_id": location["tz_id"],
                            "location_localtime": location["localtime"],
                            "date_epoch": forecast["date_epoch"],
                            "maxtemp_c": forecast["day"]["maxtemp_c"],
                            "maxtemp_f": forecast["day"]["maxtemp_f"],
                            "mintemp_c": forecast["day"]["mintemp_c"],
                            "mintemp_f": forecast["day"]["mintemp_f"],
                            "avgtemp_c": forecast["day"]["avgtemp_c"],
                            "avgtemp_f": forecast["day"]["avgtemp_f"],
                            "maxwind_mph": forecast["day"]["maxwind_mph"],
                            "maxwind_kph": forecast["day"]["maxwind_kph"],
                            "totalprecip_mm": forecast["day"]["totalprecip_mm"],
                            "totalprecip_in": forecast["day"]["totalprecip_in"],
                            "totalsnow_cm": forecast["day"]["totalsnow_cm"],
                            "avgvis_km": forecast["day"]["avgvis_km"],
                            "avgvis_miles": forecast["day"]["avgvis_miles"],
                            "avghumidity": forecast["day"]["avghumidity"],
                            "daily_will_it_rain": forecast["day"]["daily_will_it_rain"],
                            "daily_chance_of_rain": forecast["day"][
                                "daily_chance_of_rain"
                            ],
                            "daily_will_it_snow": forecast["day"]["daily_will_it_snow"],
                            "daily_chance_of_snow": forecast["day"][
                                "daily_chance_of_snow"
                            ],
                            "condition_text": forecast["day"]["condition"]["text"],
                            "condition_icon": forecast["day"]["condition"]["icon"],
                            "condition_code": forecast["day"]["condition"]["code"],
                            "uv": forecast["day"]["uv"],
                            "sunrise": forecast["astro"]["sunrise"],
                            "sunset": forecast["astro"]["sunset"],
                            "moonrise": forecast["astro"]["moonrise"],
                            "moonset": forecast["astro"]["moonset"],
                            "moon_phase": forecast["astro"]["moon_phase"],
                            "moon_illumination": forecast["astro"]["moon_illumination"],
                        },
                    )

                    for hour in forecast["hour"]:
                        hour["condition_text"] = hour.get("condition_text", "") or ""
                        hour["condition_icon"] = hour.get("condition_icon", "") or ""
                        hour["condition_code"] = hour.get("condition_code", "") or 0
                        conn.execute(
                            insert_historical_weather_hourly_sql,
                            {**hour, "date": forecast["date"]},
                        )

                conn.commit()

        print("Data inserted successfully without duplicates.")
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
