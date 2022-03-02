import abc
import datetime
from typing import List, Protocol

class EfficiencyTeamlike(Protocol):
    @abc.abstractmethod
    def biupdate_and_serialize(self, opponent : 'EfficiencyTeamlike', pppf : float, pppa : float, recency : float = .2)->None:
        pass

class EfficiencyGamelike(Protocol):
    home : EfficiencyTeamlike
    home_pts : float
    away : EfficiencyTeamlike
    away_pts : float

class EfficiencyDivisionlike(Protocol):
    @abc.abstractmethod
    def get_games_on_date(self, date : datetime.datetime)->List[EfficiencyGamelike]:
        pass

class Efficiencylike(Protocol):

    division : EfficiencyDivisionlike
    
    @abc.abstractmethod
    def __init__(self, division : EfficiencyDivisionlike):
        pass

    @abc.abstractmethod
    def update_by_date(self, date : datetime.datetime)->None:
        pass