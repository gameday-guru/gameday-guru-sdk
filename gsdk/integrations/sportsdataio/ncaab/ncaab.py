from . import ncaablike
from . import game
from .. import sportsdataio_meta



class Ncaab(ncaablike.NCAABlike):

    games : game.gameslike.Gameslike
    
    def __init__(self, meta : sportsdataio_meta.SportsDataIOMetalike=sportsdataio_meta.SportsDataIOmeta()) -> None:
        self.games = game.games.Games(meta)

