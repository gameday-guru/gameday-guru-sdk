from typing import Protocol
from by_date_like import GamesByDatelike
from ...sportsdataio_meta import SportsDataIOMetalike

class Gameslike(Protocol):

    by_date : GamesByDatelike
    meta : SportsDataIOMetalike