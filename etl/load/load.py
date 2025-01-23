import os

import pandas as pd
from sqlalchemy import MetaData, Table, text
from sqlalchemy.exc import InternalError

from config.db_config import DatabaseConfigError, load_db_config
from utils.db_utils import (
    DatabaseConnectionError,
    QueryExecutionError,
    get_db_connection,
)
from utils.sql_utils import import_sql_query

TARGET_TABLE_NAMES = [
    "mh_current_stock_and_weather",
    "mh_hourly_stock_and_weather",
    "mh_daily_stock_and_weather",
]

SET_PRIMARY_MERGED_CURRENT = os.path.join(
    os.path.dirname(__file__), "../sql/set_primary_key_mc.sql"
)

SET_PRIMARY_MERGED_HOURLY = os.path.join(
    os.path.dirname(__file__), "../sql/set_primary_key_mh.sql"
)

SET_PRIMARY_MERGED_DAILY = os.path.join(
    os.path.dirname(__file__), "../sql/set_primary_key_md.sql"
)

PRIMARY_KEY_FILE_PATHS = [
    SET_PRIMARY_MERGED_CURRENT,
    SET_PRIMARY_MERGED_HOURLY,
    SET_PRIMARY_MERGED_DAILY,
]


def load_data(data):
    create_table(data)

    return None


def create_table(data):
    try:
        connection_details = load_db_config()["target_database"]
        connection = get_db_connection(connection_details)
        for dataframe in data:
            for i, target_table in enumerate(TARGET_TABLE_NAMES):
                dataframe.to_sql(
                    target_table,
                    connection,
                    schema="student",
                    if_exists="replace",
                    index=False,
                )
                set_primary_key(connection, PRIMARY_KEY_FILE_PATHS[i])
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
        connection.close()


def set_primary_key(connection, path):
    create_primary_key_query = import_sql_query(path, remove_newlines=False)
    executable_sql = text(create_primary_key_query)
    try:
        connection.execute(executable_sql)
    except Exception as e:
        print(f"Error setting primary key on target table: {e}")
        raise
