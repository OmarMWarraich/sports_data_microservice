from pydantic import BaseModel
from typing import Literal, Optional

Weather = Literal["hot", "mild", "cold", "any"]

class LastMatchupsDto(BaseModel):
    team_a: str
    team_b: str
    weather: Optional[Weather] = 'any'
    limit: Optional[int] = 20

class LastPlayoffGamesDto(BaseModel):
    team: str
    limit: Optional[int] = 20

class LastSeasonGamesWonDto(BaseModel):
    team: str
    limit: Optional[int] = 20

class LastSeasonGamesInWeatherDto(BaseModel):
    team: str
    weather: Optional[Weather] = 'any'
    limit: Optional[int] = 20