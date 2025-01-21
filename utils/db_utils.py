from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError


class DatabaseConnectionError(Exception):
    pass


class QueryExecutionError(Exception):
    pass


def get_db_connection(connection_params):
    try:
        engine = create_db_engine(connection_params)
        connection = engine.connect()
        return connection
    except OperationalError as e:
        raise DatabaseConnectionError(
            f"Operational error when connecting to the database: {e}"
        )
    except SQLAlchemyError as e:
        raise DatabaseConnectionError(f"Failed to connect to the database: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def create_db_engine(connection_params):
    try:
        if (
            not connection_params.get("user")
            or not connection_params.get("dbname")
            or not connection_params.get("host")
            or not connection_params.get("port")
        ):
            raise ValueError("User not provided")

        engine = create_engine(
            f"postgresql+psycopg2://{connection_params['user']}"
            f":{connection_params['password']}@{connection_params['host']}"
            f":{connection_params['port']}/{connection_params['dbname']}"
        )
        return engine
    except ValueError as e:
        raise DatabaseConnectionError(f"Invalid Connection Parameters: {e}")
