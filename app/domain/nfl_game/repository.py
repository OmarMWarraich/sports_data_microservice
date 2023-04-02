import pandas as pd
from ...model.repository import SqliteRepository

local_db_path = './data/nfl.db'

class NflGameRepository(SqliteRepository):

    def __init__(self):
        super().__init__(local_db_path)

    def _modify_dataframe(self, df: pd.DataFrame):
        df["schedule_date"] = pd.to_datetime(df["schedule_date"])
        df['spread_favourite'].replace('', 0, inplace=True)

    def find(self, *args) -> pd.DataFrame:
        fetched_records = super().find(*args)
        self._modiify_dataframe(fetched_records)
        return fetched_records

