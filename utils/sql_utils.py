from utils.db_utils import QueryExecutionError


def import_sql_query(filename, remove_newlines=True):
    try:
        with open(filename, "r") as file:
            if remove_newlines:
                imported_query = file.read().replace("\n", " ").strip()
            else:
                imported_query = file.read().strip()
            return imported_query
    except FileNotFoundError as e:
        raise QueryExecutionError(f"Failed to import query: {e}")
