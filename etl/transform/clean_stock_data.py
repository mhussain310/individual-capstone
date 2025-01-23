import pandas as pd
from utils.file_utils import save_dataframe_to_csv


def clean_stock_data(stock_data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    # Remove duplicates
    stock_data = stock_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    output_dir = "data/processed"
    save_dataframe_to_csv(stock_data, output_dir, file_name)

    return stock_data
