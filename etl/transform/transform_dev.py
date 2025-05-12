import pandas as pd

from etl.transform.clean_stock_data import clean_stock_data
from etl.transform.clean_weather_data import clean_weather_data
from utils.file_utils import save_dataframe_to_csv


def transform_data(data):
    cleaned_current_weather = clean_weather_data(
        data[0], "cleaned_current_weather.csv", "local_time"
    )
    cleaned_hourly_historical_weather = clean_weather_data(
        data[1], "cleaned_hourly_historical.csv", "date"
    )
    cleaned_daily_historical_weather = clean_weather_data(
        data[2], "cleaned_daily_historical.csv", "date"
    )
    cleaned_hourly_stock_data = clean_stock_data(
        data[-2], "cleaned_hourly_stock_data.csv"
    )
    cleaned_daily_stock_data = clean_stock_data(
        data[-1], "cleaned_daily_stock_data.csv"
    )

    merged_current_data = merge_current_stock_and_weather(
        cleaned_current_weather, cleaned_hourly_stock_data, "merged_current_data.csv"
    )

    merged_hourly_data = merge_hourly_stock_and_weather(
        cleaned_hourly_historical_weather,
        cleaned_hourly_stock_data,
        "merged_hourly_data.csv",
    )

    merged_daily_data = merge_daily_stock_and_weather(
        cleaned_daily_historical_weather,
        cleaned_daily_stock_data,
        "merged_daily_data.csv",
    )

    return [merged_current_data, merged_hourly_data, merged_daily_data]


def merge_current_stock_and_weather(weather, stock, file_name):
    formatted_weather = floor_date_to_hour(
        format_date(weather, column="local_time"), column="local_time"
    )
    formatted_stock = floor_date_to_hour(stock)

    # Merge the DataFrames on local_time and timestamp
    merged_df = pd.merge(
        formatted_weather,
        formatted_stock,
        left_on="local_time",
        right_on="timestamp",
        how="inner",
    )

    # Drop one of the duplicate datetime columns
    merged_df.drop(columns=["timestamp"], inplace=True)

    output_dir = "data/processed"
    save_dataframe_to_csv(merged_df, output_dir, file_name)

    return merged_df


def merge_hourly_stock_and_weather(weather, stock, file_name):
    date_formatted_weather = format_date(weather)
    floored_to_hour_stock = floor_date_to_hour(stock)

    # Merge the DataFrames on time and timestamp
    merged_df = pd.merge(
        date_formatted_weather,
        floored_to_hour_stock,
        left_on="time",
        right_on="timestamp",
        how="inner",
    )

    # Drop one of the duplicate datetime columns
    merged_df.drop(columns=["timestamp"], inplace=True)

    output_dir = "data/processed"
    save_dataframe_to_csv(merged_df, output_dir, file_name)

    return merged_df


def merge_daily_stock_and_weather(weather, stock, file_name):
    # Merge the DataFrames on date and timestamp
    merged_df = pd.merge(
        weather,
        stock,
        left_on="date",
        right_on="timestamp",
        how="inner",
    )

    # Drop one of the duplicate datetime columns
    merged_df.drop(columns=["timestamp"], inplace=True)

    output_dir = "data/processed"
    save_dataframe_to_csv(merged_df, output_dir, file_name)

    return merged_df


def format_date(df, column="time"):
    # Convert 'time' column to datetime format
    df[column] = pd.to_datetime(df[column])

    # Format it to 'YYYY-MM-DD HH:MM:SS'
    df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Convert back to object(string)
    df[column] = df[column].astype(str)

    return df


def floor_date_to_hour(df, column="timestamp"):
    # Convert 'timestamp' column to datetime format
    df[column] = pd.to_datetime(df[column])

    # Floor to nearest hour
    df[column] = df[column].dt.floor("H")

    # Drop duplicates, keeping the first occurrence
    df.drop_duplicates(subset=[column], keep="first", inplace=True, ignore_index=True)

    # Convert back to object(string)
    df[column] = df[column].astype(str)

    return df
