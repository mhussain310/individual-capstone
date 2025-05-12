from typing import Dict, List, Tuple

import pandas as pd

from config.api_config import BASE_URL, WEATHER_API_KEY
from config.dates_config import load_date_config
from utils.request_utils import get_url

# The load_date_config fucntion was created to retrieve data for the past 3 months.
# Since the API only allows data requests within 30-day intervals,
# we generate date ranges in 1-month chunks to make 3 separate requests, one for each month.
DATE_PAIRS = load_date_config()


def extract_historical_weather_data() -> List[pd.DataFrame]:
    weather_data_list = fetch_historical_weather_records()

    hourly_historical_weather, daily_historical_weather = (
        parse_historical_weather_records(weather_data_list)
    )

    hourly_historical_weather_df = pd.DataFrame(hourly_historical_weather)
    daily_historical_weather_df = pd.DataFrame(daily_historical_weather)

    return [hourly_historical_weather_df, daily_historical_weather_df]


# Function to fetch current weather data from API
def fetch_historical_weather_records(location: str = "New_York") -> list[dict]:
    if not WEATHER_API_KEY:
        raise ValueError("Missing WEATHER_API_KEY")

    weather_data_list = []
    for date_pair in DATE_PAIRS:
        url = f"{BASE_URL}/history.json?key={WEATHER_API_KEY}&q={location}&dt={date_pair[1]}&end_dt={date_pair[0]}"
        response = get_url(url)

        if isinstance(response, str):
            raise ValueError(f"Request failed: {response}")

        response_data = response.json()
        weather_data_list.append(response_data)

    return weather_data_list


# Function to extract relevant data from response
def parse_historical_weather_records(
    weather_data_list: List[Dict],
) -> Tuple[List[Dict], List[Dict]]:

    parsed_daily_historical_weather_records_list = []
    parsed_hourly_historical_weather_records_list = []

    for weather_data in weather_data_list:
        location = weather_data["location"]

        for forecast in weather_data["forecast"]["forecastday"]:
            parsed_daily_historical_weather_records_list.append(
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
                    "daily_chance_of_rain": forecast["day"]["daily_chance_of_rain"],
                    "daily_will_it_snow": forecast["day"]["daily_will_it_snow"],
                    "daily_chance_of_snow": forecast["day"]["daily_chance_of_snow"],
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
                }
            )

            for hour in forecast["hour"]:
                hour["condition_text"] = hour.get("condition_text", "") or ""
                hour["condition_icon"] = hour.get("condition_icon", "") or ""
                hour["condition_code"] = hour.get("condition_code", "") or 0
                parsed_hourly_historical_weather_records_list.append(
                    {**hour, "date": forecast["date"]}
                )

    return (
        parsed_hourly_historical_weather_records_list,
        parsed_daily_historical_weather_records_list,
    )


if __name__ == "__main__":
    extract_historical_weather_data()
