from ...sportsdataio_meta import SportsDataIOMetalike
from by_date import GamesByDate
from by_date_like import GamesByDatelike
from gameslike import Gameslike
from typing import Type


class Games(Gameslike):

    def __init__(
        self, 
        meta : SportsDataIOMetalike, 
        by_date : Type[GamesByDatelike] = GamesByDate
    ):
        self.meta = meta
        self.by_date = by_date(self.meta)
