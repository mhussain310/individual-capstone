import pandas as pd

from config.file_path_config import BASE_PROCESSED_DIR
from utils.file_utils import generate_data_file_path, save_dataframe_to_csv


def merge_data(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    left_on: str,
    right_on: str,
    file_name: str,
    how="inner",
) -> pd.DataFrame:
    # Merge the DataFrames
    merged_df = pd.merge(
        df1,
        df2,
        left_on=left_on,
        right_on=right_on,
        how=how,
    )

    # Drop one of the duplicate datetime columns
    merged_df.drop(columns=[right_on], inplace=True)

    # Save the dataframe as a CSV for logging purposes
    processed_file_path = generate_data_file_path(
        prefix=file_name, base_dir=BASE_PROCESSED_DIR, subdir="merged"
    )
    save_dataframe_to_csv(merged_df, processed_file_path)

    # Return the merged dataframe
    return merged_df
