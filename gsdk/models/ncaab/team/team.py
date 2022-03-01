import efficiency
import abc

class TeamDivisonlike(metaclass=abc.ABCMeta):
    pass

class TeamControllerlike(metaclass=abc.ABCMeta): 
    """Abstract class for team controller.
    We just need get and set methods for the team.
    """
    
    @abc.abstractmethod
    def get_team(self, id : int):
        pass

    @abc.abstractmethod
    def set_team(self, id : int, team : 'Teamlike')->None:
        pass

class Teamlike(
    # injection targets
    efficiency.EfficiencyTeamlike, 
    metaclass=abc.ABCMeta
):
    """Team asbract class with injection targets.
    """
    pass

class Team(Teamlike):
    """An NCAAB team.
    """

    controller : TeamControllerlike
    efficiency : efficiency.Efficiency

    def __init__(self):
        pass

    def __hash__(self)->int:
        return self.id

    
