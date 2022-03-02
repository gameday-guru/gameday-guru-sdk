import abc
import datetime
from typing import List, Protocol
from . import efficiencylike

class DivisionTeamlike(
    # dependency targets
    efficiencylike.EfficiencyTeamlike,
    Protocol
):
    pass

class DivisionGamelike(
    # dependency targets
    efficiencylike.EfficiencyTeamlike,
    Protocol
):
    pass

class DivisionControllerlike(Protocol):
    @abc.abstractmethod
    def get_games_on_date(self, date : datetime.datetime)->List[DivisionGamelike]:   
        pass

class Divisionlike(
    efficiencylike.EfficiencyTeamlike,
    Protocol
):

    efficiency : efficiencylike.Efficiencylike
    controller : DivisionControllerlike
    
    @abc.abstractmethod
    def get_games_on_date(self, date : datetime.datetime)->List[DivisionGamelike]:   
        # todo fix type linting here
        pass