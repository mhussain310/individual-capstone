import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def clean_weather_data(
    weather_data: pd.DataFrame, file_name: str, sort_by: str
) -> pd.DataFrame:
    # Convert dictionary columns to strings (if any)
    for column in weather_data.columns:
        if isinstance(
            weather_data[column].iloc[0], dict
        ):  # Check if the column contains dictionaries
            weather_data[column] = weather_data[column].apply(str)  # Convert to string

    # Convert date/time column to datetime
    if sort_by in weather_data.columns:
        weather_data[sort_by] = pd.to_datetime(weather_data[sort_by], errors="coerce")

    # Sort values
    weather_data = sort_values(weather_data, sort_by)

    # Convert datetime back to original string format
    str_format = "%Y-%m-%d" if sort_by == "date" else "%Y-%m-%d %H:%M"
    weather_data[sort_by] = weather_data[sort_by].dt.strftime(str_format)

    # Remove duplicates
    weather_data = weather_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="cleaned/weather"
    )
    save_dataframe_to_csv(weather_data, processed_file_path)

    # Return the cleaned dataframe
    return weather_data


def sort_values(weather_data: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    weather_data = weather_data.sort_values(by=sort_by, ascending=True)
    return weather_data
