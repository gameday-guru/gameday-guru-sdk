from . import ncaablike
from . import game
from .. import sportsdataio_meta



class NCAAB(ncaablike.NCAABlike):

    games : game.gameslike.Gameslike
    
    def __init__(self, meta : sportsdataio_meta.SportsDataIOMetalike) -> None:
        self.games = game.games.Games( meta)

