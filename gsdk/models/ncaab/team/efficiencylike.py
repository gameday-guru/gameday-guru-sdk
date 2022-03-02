import abc
from typing import Tuple, Protocol

class EfficiencyTeamlike(Protocol):
    """Abstract class. Represents what is needed by Efficiency from a team.
    """
    pts : float
    pts_against : float
    name : str
    id : int

class EfficiencyDivisionlike(Protocol):
    """Abstract class. Represents what is needed by Efficiency from a league.
    """
    avg_oeff : float
    avg_deff : float
    ppp : float

class EfficiencyControllerlike(Protocol):
    """Abstract class defining the controller used for serializing the efficiency model.
    """
    @abc.abstractmethod
    def get(self, efficiency : 'Efficiencylike'):
        pass

    @abc.abstractmethod
    def serialize(self, efficiency : 'Efficiencylike'):
        pass

class Efficiencylike(Protocol):
    team : EfficiencyTeamlike
    possessions : float
    kadjoeff : float
    kadjdeff : float
    badjoeff : float
    badjdeff : float
    radjdeff : float
    radjoeff : float

    league : EfficiencyDivisionlike
    controller : EfficiencyControllerlike
    recency : float
    mu : float 

    @classmethod
    @abc.abstractmethod
    def eff(cls, pts : float, possesions : float)->float:
        pass

    @classmethod
    @abc.abstractmethod
    def adjem(cls, oeff : float, navg: float)->float:
        pass

    @classmethod
    @abc.abstractmethod
    def kadjeff(cls, eff : float, navg : float, op_adj : float)->float:
        pass

    @abc.abstractmethod
    def __init__(self, team : EfficiencyTeamlike, league : EfficiencyDivisionlike, controller : EfficiencyControllerlike):
        pass

    @abc.abstractmethod
    def get(self)->None:
        pass

    @abc.abstractmethod
    def get_oeff(self)->float:
        pass

    @abc.abstractmethod
    def get_deff(self)->float:
        pass

    @abc.abstractmethod
    def next_adjusted_koeff(self, opponent : 'Efficiencylike')->float:
        pass

    @abc.abstractmethod
    def next_adjusted_kdeff(self, opponent : 'Efficiencylike')->float:
        pass

    @classmethod
    @abc.abstractmethod
    def badjeff(cls, pppg : float, oe : float, de : float, navg : float)->Tuple[float, float]:
        pass

    @classmethod
    @abc.abstractmethod
    def radjeff(cls, pppg : float, oe : float, de : float, navg : float, recency : float =.2)->Tuple[float, float]:
        pass
    
    @abc.abstractmethod
    def biupdate_kadjeff(self, opponent :'Efficiencylike')->None:
        pass

    @abc.abstractmethod
    def biupdate_badjeff(self, opponent : 'Efficiencylike', pppf : float, pppa : float)->None:
        pass

    @abc.abstractmethod
    def serialize(self)->None:
        pass

    @abc.abstractmethod
    def biupdate_and_serialize(self, opponent : 'Efficiencylike', pppf : float, pppa : float, recency : float = .2)->None:
        pass