import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def clean_stock_data(stock_data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    # Convert dictionary columns to strings (if any)
    for column in stock_data.columns:
        if isinstance(
            stock_data[column].iloc[0], dict
        ):  # Check if the column contains dictionaries
            stock_data[column] = stock_data[column].apply(str)  # Convert to string

    # Remove duplicates
    stock_data = stock_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="cleaned/stock"
    )
    save_dataframe_to_csv(stock_data, processed_file_path)

    # Return the cleaned dataframe
    return stock_data
