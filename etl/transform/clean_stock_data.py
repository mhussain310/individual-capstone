import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def clean_stock_data(stock_data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    # Remove duplicates
    stock_data = stock_data.drop_duplicates()

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="cleaned/stock"
    )
    save_dataframe_to_csv(stock_data, processed_file_path)

    # Return the cleaned dataframe
    return stock_data
