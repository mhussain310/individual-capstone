from typing import List

import os
import pandas as pd

from config.api_config import get_stock_api_key
from config.file_path_config import (
    DAILY_STOCK_DATA_FILE_PATH,
    HOURLY_STOCK_DATA_FILE_PATH,
)
from utils.request_utils import get_url

# Uncomment the below 2 for testing purposes and not to overwhelm API.

# hourly_stock_data_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv"
# daily_stock_data_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv"

# Comment the above 2 and Uncomment the below 2 for production

hourly_stock_data_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=60min&outputsize=full&apikey={get_stock_api_key()}&datatype=csv"
daily_stock_data_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv"


def extract_stock_data() -> List[pd.DataFrame]:
    try:
        hourly_stock_data_df = fetch_stock_data(
            hourly_stock_data_url, HOURLY_STOCK_DATA_FILE_PATH
        )
        daily_stock_data_df = fetch_stock_data(
            daily_stock_data_url, DAILY_STOCK_DATA_FILE_PATH
        )

        return [hourly_stock_data_df, daily_stock_data_df]
    except Exception as e:
        raise Exception(f"Failed to extract data: {e}")


def fetch_stock_data(url: str, file_path: str) -> pd.DataFrame:
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    response = get_url(url)
    with open(file_path, "wb") as file:
        file.write(response.content)
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    extract_stock_data()
