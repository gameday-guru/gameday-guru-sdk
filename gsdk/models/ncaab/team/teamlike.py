from . import efficiencylike
import abc
from typing import Protocol

class TeamDivisonlike(Protocol):
    efficiency : efficiencylike.EfficiencyDivisionlike

class TeamControllerlike(Protocol): 
    """Abstract class for team controller.
    We just need get and set methods for the team.
    """

    efficiency_controller : efficiencylike.EfficiencyControllerlike
    
    @abc.abstractmethod
    def get(self, id : int):
        pass

    @abc.abstractmethod
    def serialize(self, id : int, team : 'Teamlike')->None:
        pass

class Teamlike(
    # injection targets
    efficiencylike.EfficiencyTeamlike, 
    Protocol
):
    """Team abstract class with injection targets.
    """
    pts : float
    pts_against : float
    name : str
    id : int