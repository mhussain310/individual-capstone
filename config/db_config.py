import os
from typing import Dict


class DatabaseConfigError(Exception):
    pass


def load_db_config() -> Dict[str, Dict[str, str]]:
    config = {
        "source_database": {
            "dbname": os.getenv("SOURCE_DB_NAME", "error"),
            "user": os.getenv("SOURCE_DB_USER", "error"),
            "password": os.getenv("SOURCE_DB_PASSWORD", ""),
            "host": os.getenv("SOURCE_DB_HOST", "error"),
            "port": os.getenv("SOURCE_DB_PORT", "5432"),
        },
        "target_database": {
            "dbname": os.getenv("TARGET_DB_NAME", "error"),
            "user": os.getenv("TARGET_DB_USER", "error"),
            "password": os.getenv("TARGET_DB_PASSWORD", ""),
            "host": os.getenv("TARGET_DB_HOST", "error"),
            "port": os.getenv("TARGET_DB_PORT", "5432"),
        },
    }

    # validate_db_config(config)

    return config


def validate_db_config(config):
    for db_key, db_config in config.items():
        for key, value in db_config.items():
            if value == "error":
                raise DatabaseConfigError(
                    f"Configuration error: {db_key} {key} is set to 'error'"
                )
