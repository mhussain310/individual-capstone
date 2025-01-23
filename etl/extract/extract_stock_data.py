import os

import pandas as pd

from utils.request_utils import get_url

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

hourly_stock_data_file_path = os.path.join(
    ROOT_PATH, "data", "raw", "hourly_stock_data.csv"
)
daily_stock_data_file_path = os.path.join(
    ROOT_PATH, "data", "raw", "daily_stock_data.csv"
)

hourly_stock_data_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv"
daily_stock_data_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv"


def extract_stock_data():
    try:
        hourly_stock_data_df = extract_stock_data_execution(
            hourly_stock_data_url, hourly_stock_data_file_path
        )
        daily_stock_data_df = extract_stock_data_execution(
            daily_stock_data_url, daily_stock_data_file_path
        )

        return [hourly_stock_data_df, daily_stock_data_df]
    except Exception as e:
        raise Exception(f"Failed to extract data: {e}")


def extract_stock_data_execution(url, file_path):
    response = get_url(url)
    with open(file_path, "wb") as file:
        file.write(response.content)
    df = pd.read_csv(file_path)
    return df
