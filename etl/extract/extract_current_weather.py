from typing import List

import pandas as pd

from config.api_config import BASE_URL, WEATHER_API_KEY
from utils.request_utils import get_url


# Put the extracted data into a csv file and return path to file
def extract_current_weather_data() -> List[pd.DataFrame]:
    raw_data = fetch_current_weather_data()
    weather_record = extract_current_weather_record(raw_data)
    current_weather_df = pd.DataFrame([weather_record])

    return [current_weather_df]


# Function to fetch current weather data from API
def fetch_current_weather_data(location: str = "New_York") -> dict:
    if not WEATHER_API_KEY:
        raise ValueError("Missing WEATHER_API_KEY")

    url = f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={location}&aqi=yes"
    return get_url(url).json()


# Function to extract relevant data from response
def extract_current_weather_record(response_data: dict) -> dict:
    location = response_data["location"]
    current = response_data["current"]
    condition = current["condition"]
    air_quality = current["air_quality"]

    return {
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


if __name__ == "__main__":
    extract_current_weather_data()

# for key, value in weather_record.items():
#     if value is None:
#         weather_record[key] = 0 if isinstance(value, (int, float)) else ""
