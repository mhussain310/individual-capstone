import pandas as pd
from utils.file_utils import save_dataframe_to_csv

df1 = pd.read_csv("../../data/raw/hourly_stock_data.csv")
df2 = pd.read_csv("../../data/raw/daily_stock_data.csv")


def clean_stock_data(stock_data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    # Fill rows with missing values with previous day values
    # Remove duplicates
    columns_to_fill = ["open", "high", "low", "close"]
    stock_data[columns_to_fill] = stock_data[columns_to_fill].fillna(method="ffill")
    stock_data = stock_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    output_dir = "data/processed"
    save_dataframe_to_csv(stock_data, output_dir, file_name)

    return stock_data
