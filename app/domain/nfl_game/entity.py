from dataclasses import dataclass
from datetime import date
import strawberry

from ...model.entity import Entity


@strawberry.type
@dataclass
class NflGame(Entity):
    schedule_date: date
    schedule_season: int
    schedule_week: int
    schedule_playoff: bool
    team_home: str
    score_home: int
    score_away: int
    team_away: str
    team_favourite_id: str
    spread_favourite: float
    over_under_line: int
    stadium: str
    stadium_neutral: bool
    weather_temperature: int
    weather_wind_mph: int
    weather_humidity: int
    weather_detail: int

    @classmethod
    def entity_name(cls) -> str:
        return 'NFLGame'
    
    @classmethod
    def table_name(cls) -> str:
        return 'games'


