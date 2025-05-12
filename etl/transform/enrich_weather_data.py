import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from etl.transform.date_transformations import floor_date_to_hour, format_date
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def enrich_weather_data(
    weather_data: pd.DataFrame, file_name: str, column: str, to_hour: bool = False
) -> pd.DataFrame:
    # Transform the date column
    weather_data = format_date(weather_data, column=column)

    if to_hour:
        weather_data = floor_date_to_hour(weather_data, column=column)

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="enriched/weather"
    )
    save_dataframe_to_csv(weather_data, processed_file_path)

    # Return the file path of the csv
    return weather_data
