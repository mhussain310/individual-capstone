from typing import Dict

import pandas as pd

from config.file_path_config import (
    CURRENT_WEATHER_OUTPUT_FILE_PATH,
    DAILY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH,
    HOURLY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH,
)
from etl.transform.clean_stock_data import clean_stock_data
from etl.transform.clean_weather_data import clean_weather_data
from etl.transform.enrich_stock_data import enrich_stock_data
from etl.transform.enrich_weather_data import enrich_weather_data
from etl.transform.merge_data import merge_data
from utils.file_utils import save_dataframe_to_csv


def transform_data(data: list[pd.DataFrame]) -> list[pd.DataFrame]:
    (
        current_weather_df,
        hourly_historical_weather_df,
        daily_historical_weather_df,
        hourly_stock_df,
        daily_stock_df,
    ) = data

    # Clean all extracted data
    cleaned_data = clean_all_data(
        current_weather_df,
        hourly_historical_weather_df,
        daily_historical_weather_df,
        hourly_stock_df,
        daily_stock_df,
    )

    # Enrich all cleaned data
    enriched_data = enrich_all_data(cleaned_data)

    # Merge all enriched data
    merged_data = merge_all_data(enriched_data)

    current_weather_df = merged_data["current_weather"]
    hourly_stock_and_weather_df = merged_data["hourly_stock_and_weather"]
    daily_stock_and_weather_df = merged_data["daily_stock_and_weather"]

    # Save transformed data as CSV files for logging purposes
    # As this is the final step in the transformation process, we will save the files in the 'output' directory
    save_dataframe_to_csv(current_weather_df, CURRENT_WEATHER_OUTPUT_FILE_PATH)
    save_dataframe_to_csv(
        hourly_stock_and_weather_df, HOURLY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH
    )
    save_dataframe_to_csv(
        daily_stock_and_weather_df, DAILY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH
    )

    # Return list of transformed data
    return [
        current_weather_df,
        hourly_stock_and_weather_df,
        daily_stock_and_weather_df,
    ]


def clean_all_data(
    current_weather_df,
    hourly_weather_df,
    daily_weather_df,
    hourly_stock_df,
    daily_stock_df,
) -> Dict[str, pd.DataFrame]:
    cleaned_data = {
        "current_weather": clean_weather_data(
            current_weather_df,
            file_name="cleaned_current_weather",
            sort_by="local_time",
        ),
        "hourly_weather": clean_weather_data(
            hourly_weather_df, file_name="cleaned_hourly_historical", sort_by="time"
        ),
        "daily_weather": clean_weather_data(
            daily_weather_df, file_name="cleaned_daily_historical", sort_by="date"
        ),
        "hourly_stock": clean_stock_data(
            hourly_stock_df,
            file_name="cleaned_hourly_stock_data",
            sort_by="timestamp",
            has_time=True,
        ),
        "daily_stock": clean_stock_data(
            daily_stock_df, file_name="cleaned_daily_stock_data", sort_by="timestamp"
        ),
    }
    return cleaned_data


def enrich_all_data(cleaned_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    enriched_data = {
        "current_weather": cleaned_data["current_weather"],
        "hourly_weather": enrich_weather_data(
            cleaned_data["hourly_weather"],
            file_name="enriched_hourly_historical",
            column="time",
        ),
        "daily_weather": cleaned_data["daily_weather"],
        "hourly_stock": enrich_stock_data(
            cleaned_data["hourly_stock"],
            file_name="enriched_hourly_stock_data",
            column="timestamp",
        ),
        "daily_stock": cleaned_data["daily_stock"],
    }

    return enriched_data


def merge_all_data(enriched_data: Dict[str, pd.DataFrame]) -> list[pd.DataFrame]:
    merged_data = {
        "current_weather": enriched_data["current_weather"],
        "hourly_stock_and_weather": merge_data(
            df1=enriched_data["hourly_weather"],
            df2=enriched_data["hourly_stock"],
            left_on="time",
            right_on="timestamp",
            file_name="merged_hourly_data",
        ),
        "daily_stock_and_weather": merge_data(
            df1=enriched_data["daily_weather"],
            df2=enriched_data["daily_stock"],
            left_on="date",
            right_on="timestamp",
            file_name="merged_daily_data",
        ),
    }
    return merged_data
