import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from etl.transform.date_transformations import floor_date_to_hour
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def enrich_stock_data(
    stock_data: pd.DataFrame, file_name: str, column: str
) -> pd.DataFrame:
    # Transform the date column
    stock_data = floor_date_to_hour(stock_data, column=column)

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="enriched/stock"
    )
    save_dataframe_to_csv(stock_data, processed_file_path)

    # Return the enriched dataframe
    return stock_data
