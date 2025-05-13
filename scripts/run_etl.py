import os
import sys

from config.env_config import setup_env
from etl.extract.extract import extract_data
from etl.load.load import load_data
from etl.transform.transform import transform_data
from utils.file_utils import clear_data_folders


def main():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")

    print("Removing temp files from previous run...")
    clear_data_folders()
    print("Removal of temp files complete.")

    print("Extracting data...")
    extracted_data = extract_data()
    print("Data extraction complete.")

    print("Transforming data...")
    transformed_data = transform_data(extracted_data)
    print("Data transformation complete.")

    print("Loading data...")
    load_data(transformed_data)
    print("Data loading complete.")

    print(
        f"ETL pipeline ran successfully in " f'{os.getenv("ENV", "error")} environment!'
    )


if __name__ == "__main__":
    main()
