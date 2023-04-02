from flask import Flask

from ..domain.nfl_game.graphql_router import games_module
from ..domain.betting.controller import betting_module

app = Flask(__name__)
app.register_blueprint(games_module)
app.register_blueprint(betting_module)