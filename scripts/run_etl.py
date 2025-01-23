import os

from etl.extract.extract import extract_data
from etl.transform.transform import transform_data
from etl.load.load import load_data


def main():
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
