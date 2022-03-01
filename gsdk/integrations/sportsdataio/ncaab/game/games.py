import abc
from gsdk.utils.integrations.sportsdataio.sportsdataio_meta import SportsDataIOMetalike
from . import by_date
import sportsdataio_meta

class Gameslike(metaclass=abc.ABCMeta):

    by_date : by_date.GamesByDatelike
    meta : sportsdataio_meta.SportsDataIOMetalike



class Games(Gameslike):

    def __init__(self, meta : SportsDataIOMetalike):
        self.meta = meta
        self.by_date = by_date.GamesByDate(self.meta)
