from datetime import datetime, date
from pydantic import BaseModel
from pandas import DataFrame
from typing import Tuple

from ..nfl_game.service import NflGameService, Weather
from ..nfl_game.dto import LastSeasonGamesWonDto, LastSeasonGamesInWeatherDto


class BuildNflSpreadDto(BaseModel):
    team_a: str
    team_b: str
    on_date: str

class BettingService:

    def __init__(self, nfl_game_service: NflGameService):
        self.nfl_game_service = nfl_game_service
    # We're mocking a weather service here
    def get_expected_weather(self, on_date: date) -> Weather:
        return 'cold'
    
    @staticmethod
    def _get_date_from_str(date: str) -> date:
        return datetime.strptime(date, '%d/%m/%Y').date()
    
    @staticmethod
    def _get_total_points_scored_in_games(team: str, df: DataFrame) -> int:
        team_points_home = sum(df[df['team_home'] == team]['score_home'])
        team_points_away = sum(df[df['team_away'] == team]['score_away'])
        return team_points_home + team_points_away
    
    def _get_last_season_wins_and_points_scored_in_weather(self, team: str, weather: Weather) -> Tuple[int, int]:
        wins_last_season = self.nfl_game_service.get_last_season_games_won(LastSeasonGamesWonDto(team=team))
        games_last_season_in_weather = self.nfl_game_service.get_last_season_games_in_weather(
            LastSeasonGamesInWeatherDto(team=team, weather=weather))
        return len(wins_last_season), self._get_total_points_scored_in_games(team, games_last_season_in_weather)
    
    @staticmethod
    def _compare_as_perc(count_a: float, count_b: float):
        total = count_a + count_b
        return count_a / total
    
    @staticmethod
    def _win_probability_as_spread(prob: float) -> int:
        BOUNDS = [-1000, 1000]
        bounds_range = BOUNDS[1] - BOUNDS[0]
        spread = (prob * bounds_range) + BOUNDS[0]
        spread_rounded_to_10 = int(round(spread, -1))
        return spread_rounded_to_10
    
    def build_nfl_spread(self, dto: BuildNflSpreadDto) -> int:
        game_date = self._get_date_from_str(dto.on_date)
        expected_weather = self.get_expected_weather(on_date=game_date)

        team_a_wins, team_a_points_weather = self._get_last_season_wins_and_points_scored_in_weather(
            dto.team_a, expected_weather)
        team_b_wins, team_b_points_weather = self._get_last_season_wins_and_points_scored_in_weather(
            dto.team_b, expected_weather)
        
        comparison_wins = self._compare_as_perc(team_a_wins, team_b_wins)
        comparison_points_scored_in_weather = self._compare_as_perc(team_a_points_weather, team_b_points_weather)
        comparison_aggregate = 0.5 * comparison_wins + 0.5 * comparison_points_scored_in_weather
        return self._win_probability_as_spread(comparison_aggregate)