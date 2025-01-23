import pandas as pd
from utils.file_utils import save_dataframe_to_csv


def clean_weather_data(
    weather_data: pd.DataFrame, file_name: str, sort_by: str
) -> pd.DataFrame:
    # Sort values
    # Remove duplicates
    weather_data = sort_values(weather_data, sort_by)
    weather_data = weather_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    # Ensure the directory exists
    output_dir = "data/processed"
    save_dataframe_to_csv(weather_data, output_dir, file_name)

    return weather_data


def sort_values(weather_data: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    weather_data = weather_data.sort_values(by=sort_by)
    return weather_data
