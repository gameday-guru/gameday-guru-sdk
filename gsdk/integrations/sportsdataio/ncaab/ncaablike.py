from typing import Protocol
from . import game

class NCAABlike(Protocol):

    games : game.gameslike.Gameslike