from typing import Optional, Tuple
import pandas as pd
import sqlite3

from ..model.query import FindQuery


class SqliteRepository:

    def __init__(self, local_db_path: str):
        self._db_connection: sqlite3.Connection = sqlite3.connect(local_db_path)
        self._db_cursor: sqlite3.Cursor = self._db_connection.cursor()

    @staticmethod
    def _get_column_names_from_query_cursor(cursor: sqlite3.Cursor) -> list[str]:
        return list(map(lambda x: x[0], cursor.description))
    
    def _query_data_and_column_names(self, str_query: str, limit: Optional[int] = 20) -> Tuple[list, list[str]]:
        query_cursor = self._db_cursor.execute(str_query)
        columns = self._get_column_names_from_query_cursor(query_cursor)
        data = query_cursor.fetchmany(size=limit)
        return data, columns
    
    def find(self, query: FindQuery) -> pd.DataFrame:
        str_query = query.get_sql_querystring()
        data, columns = self._query_data_and_column_names(str_query, limit=query.limit)
        return pd.DataFrame(data, columns=columns)