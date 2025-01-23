from etl.extract.extract_current_weather import extract_current_weather_data
from etl.extract.extract_historical_weather import extract_historical_weather_data
from etl.extract.extract_stock_data import extract_stock_data


def extract_data():
    current_weather = extract_current_weather_data()
    historical_weather = extract_historical_weather_data()
    stock_data = extract_stock_data()

    extracted_data = current_weather + historical_weather + stock_data
    return extracted_data
