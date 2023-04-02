from typing import Any, List, Optional
from pandas import DataFrame
from flask import request

from .dto import LastMatchupsDto, LastPlayoffGamesDto
from .repository import NflGameRepository
from .service import NflGameService
from .entity import NflGame


def get_request_body_values(keys: list[str]) -> list[Any]:
    request_body = request.get_json() or {}
    return [request_body.get(key) for key in keys]


class NflGameController:

    @staticmethod
    def _service():
        return NflGameService(NflGameRepository())
    
    @staticmethod
    def _df_to_list(games_df: DataFrame):
        return [NflGame(**kwargs) for kwargs in games_df.to_dict(orient='records')]
    
    @classmethod
    def get_last_matchups(cls, team_a: str, team_b: str, limit: Optional[int] = 20) -> List[NflGame]:
        dto = LastMatchupsDto(team_a=team_a, team_b=team_b, limit=limit)
        games_df= cls._service().get_last_matchups(dto)
        games = cls._df_to_list(games_df)
        return games

    @classmethod
    def get_last_playoff_games(cls, team: str, limit: Optional[int] = 20) -> List[NflGame]:
        dto = LastPlayoffGamesDto(team=team, limit=limit)
        games_df = cls._service().get_last_playoff_games(dto)
        games = cls._df_to_list(games_df)
        return games
    
