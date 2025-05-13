import pandas as pd
from sqlalchemy.exc import InternalError

from config.db_config import DatabaseConfigError, load_db_config
from utils.db_utils import (
    DatabaseConnectionError,
    QueryExecutionError,
    get_db_connection,
)

TARGET_TABLE_NAMES = [
    "current_stock_and_weather",
    "hourly_stock_and_weather",
    "daily_stock_and_weather",
]


def load_data(data: list[str]):
    create_table(data)

    return None


def create_table(data: list[str]):
    connection = None
    try:
        connection_details = load_db_config()
        connection = get_db_connection(connection_details)
        for dataframe in data:
            for target_table in TARGET_TABLE_NAMES:
                dataframe["id"] = range(1, len(dataframe) + 1)
                dataframe.set_index("id", inplace=True)
                dataframe.to_sql(
                    target_table,
                    connection,
                    if_exists="replace",
                    index=True,
                )
        connection.commit()
    except InternalError:
        print("Target table exists")
        raise
    except DatabaseConfigError as e:
        print(f"Target database not configured correctly: {e}")
        raise
    except DatabaseConnectionError as e:
        print(f"Failed to connect to the database when creating table:" f" {e}")
        raise
    except pd.errors.DatabaseError as e:
        print(f"Failed to create table: {e}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
    finally:
        if connection is not None:
            connection.close()
