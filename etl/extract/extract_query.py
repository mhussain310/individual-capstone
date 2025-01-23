import pandas as pd
from utils.db_utils import QueryExecutionError


def execute_extract_query(query, connection):
    try:
        return pd.read_sql_query(query, connection)
    except pd.errors.DatabaseError as e:
        print(f"Failed to execute query: {e}")
        print(f"The query that failed was: {query}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
