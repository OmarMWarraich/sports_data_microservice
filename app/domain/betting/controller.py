from typing import Any, Tuple
from flask import Blueprint
from pydantic.error_wrappers import ValidationError

from ..nfl_game.controller import get_request_body_values
from ..nfl_game.repository import NflGameRepository
from ..nfl_game.service import NflGameService
from .service import BettingService, BuildNflSpreadDto

betting_module = Blueprint('betting', __name__, url_prefix='/betting')


def feed_spread_dto(controller_fn):

    def form_dto_with_request_body():
        try:
            team, opponent, date = get_request_body_values(['team', 'opponent', 'date'])
            dto = BuildNflSpreadDto(team_a=team, team_b=opponent, on_date=date)
            return controller_fn(dto)
        except ValidationError as err:
            return {'error': 'Bad data: %s' % str(err)}, 400
        
    return form_dto_with_request_body


class BettingController:

    @staticmethod
    def _service():
        return BettingService(NflGameService(NflGameRepository()))
    

    @betting_module.route('/buildSpread')
    @staticmethod
    @feed_spread_dto
    def build_spread(dto: BuildNflSpreadDto) -> Tuple[Any, int]:
        spread = BettingController._service().build_nfl_spread(dto)
        return {'data': spread}, 200
