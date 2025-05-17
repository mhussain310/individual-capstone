from utils.file_utils import get_absolute_path, generate_data_file_path

BASE_RAW_DIR = "data/raw"
BASE_PROCESSED_DIR = "data/processed"
BASE_OUTPUT_DIR = "data/output"

# Extracted data file paths
HOURLY_STOCK_DATA_FILE_PATH = get_absolute_path(
    f"{BASE_RAW_DIR}/stock/hourly_stock_data.csv"
)
DAILY_STOCK_DATA_FILE_PATH = get_absolute_path(
    f"{BASE_RAW_DIR}/stock/daily_stock_data.csv"
)

# Output file paths of final transformed data
CURRENT_WEATHER_OUTPUT_FILE_PATH = generate_data_file_path(
    prefix="current_weather", base_dir=BASE_OUTPUT_DIR
)
HOURLY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH = generate_data_file_path(
    prefix="hourly_stock_and_weather", base_dir=BASE_OUTPUT_DIR
)
DAILY_STOCK_AND_WEATHER_OUTPUT_FILE_PATH = generate_data_file_path(
    prefix="daily_stock_and_weather", base_dir=BASE_OUTPUT_DIR
)
