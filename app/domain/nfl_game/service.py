from typing import Optional

from ...model.query import FindQuery
from .dto import LastMatchupsDto, LastPlayoffGamesDto, LastSeasonGamesInWeatherDto, LastSeasonGamesWonDto, Weather
from .repository import NflGameRepository
from .entity import NflGame

game = NflGame.table()

class NflGameService:

    def __init__(self, repository: NflGameRepository):
        self.repository = repository

    @staticmethod
    def _build_query_for_weather(weather: Optional[Weather] = None):
        if weather == 'hot':
            return game.weather_temperature > 85
        if weather == 'mild':
            return (game.weather_temperature > 50) & (game.weather_temperature <= 85)
        if weather == 'cold':
            return game.weather_temperature <= 50
        return game.weather_temperature
    
    def _build_last_matchups_expression(self, team_a: str, team_b: str, weather: Optional[Weather] = 'any'):
        home_team_matches_either = (game.team_home == team_a) | (game.team_home == team_b)
        away_team_matches_either = (game.team_away == team_a) | (game.team_away == team_b)
        game_has_been_played = game.score_home != ''
        weather_matches = self._build_query_for_weather(weather)

        return home_team_matches_either & away_team_matches_either & game_has_been_played & weather_matches
    
    def get_last_matchups(self,dto: LastMatchupsDto):
        query_expression = self._build_last_matchups_expression(dto.team_a, dto.team_b, dto.weather)
        query = FindQuery(NflGame, where_expression=query_expression, limit=dto.limit)
        return self.repository.find(query)

    def _build_last_playoff_games_expression(self, team: str):
        team_is_in_game = (game.team_home == team) | (game.team_away == team)
        game_has_been_played = game.score_home != ''
        is_playoffs = (game.schedule_week == 'Division') | (game.schedule_week == 'Conference') | \
            (game.schedule_week == 'Superbowl')
        
        return team_is_in_game & game_has_been_played & is_playoffs
    
    def get_last_playoff_games(self, dto: LastPlayoffGamesDto):
        query_expression = self._build_last_playoff_games_expression(dto.team)
        query = FindQuery(NflGame, where_expression=query_expression, limit=dto.limit)
        return self.repository.find(query)
    
    def _build_team_won_query(self, team: str):
        home_team_won = game.score_home > game.score_away
        away_team_won = game.score_away > game.score_home

        return (home_team_won & game.team_home == team) | (away_team_won & game.team_away == team)
    
    def _build_last_season_wins_expression(self, team: str):
        last_season_query = game.schedule_season == 2021
        team_won_query = self._build_team_won_query(team)

        last_season_wins_query = team_won_query & last_season_query
        return last_season_wins_query
    
    def get_last_season_games_won(self, dto: LastSeasonGamesWonDto):
        query = self._build_last_season_wins_expression(dto.team)
        return self.repository.find(FindQuery(NflGame, query, limit=dto.limit))
    
    def _build_team_played_query(self, team: str):
        return (game.team_home == team) | (game.team_away == team)
    
    def _build_recent_games_in_weather_query(self, team: str, weather: Optional[Weather] = 'any'):
        last_season_query = game.schedule_season == 2021
        team_played_query = self._build_team_played_query(team)
        weather_query = self._build_query_for_weather(weather)

        return last_season_query & weather_query & team_played_query
    
    def get_last_season_games_in_weather(self, dto: LastSeasonGamesInWeatherDto):
        query = self._build_recent_games_in_weather_query(dto.team, dto.weather)
        return self.repository.find(FindQuery(NflGame, query, limit=dto.limit))

