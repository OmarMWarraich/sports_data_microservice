from typing import Any, List
from flask import Blueprint
import strawberry

from .controller import NflGameController, get_request_body_values
from .repository import NflGameRepository
from .service import NflGameService
from .entity import NflGame

games_module = Blueprint('games', __name__, url_prefix='/games')


@strawberry.type
class Query:
    recentMatchups: List[NflGame] = strawberry.field(resolver=NflGameController.get_last_matchups)
    recentPlayoffGames: List[NflGame] = strawberry.field(resolver=NflGameController.get_last_playoff_games)



games_schema = strawberry.Schema(query=Query)


def feed_query(controller_fn):

    def verify_query():
        [query] = get_request_body_values(['query'])
        if not query:
            return {'error': 'Bad data'}, 400
        return controller_fn(query)
    
    return verify_query


class NflGameGraphqlRouter:

    @games_module.route('/graphql', methods=['POST'])
    @staticmethod
    @feed_query
    def query(query: str) -> Any:
        games = games_schema.execute_sync(query).data
        return games
    
    