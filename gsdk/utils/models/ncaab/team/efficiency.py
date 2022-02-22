import abc
from typing import List

class EfficiencyTeamlike(metaclass=abc.ABCMeta):
    """Abstract class. Represents what is needed by Efficiency from a team.
    """
    pts : float
    pts_against : float
    possessions : float
    adjusted_oeff : float
    adjusted_deff : float
    name : str
    id : int

    @abc.abstractmethod
    def next_efficiency_training_set(self)->List['EfficiencyTeamlike']:
        """Gets the next available efficiency training set
        which is a list of opponents.
        """
        pass

class EfficiencyLeaguelike(abc.ABC):
    """Abstract class. Represents what is needed by Efficiency from a league.
    """
    avg_oeff : float
    avg_deff : float


class Efficiency:
    """Class for managing team efficiency properties. Should usually be used to compose a 
    team class.
    """

    team : EfficiencyTeamlike
    league : EfficiencyLeaguelike
    recency : float

    @classmethod
    def eff(cls, pts : float, possesions : float)->float:
        """Computes efficiency, pts/possesions.

        Args:
            pts (float): the points scored by a team.
            possesions (float): the number of possesions.

        Returns:
            float: the efficiency.
        """
        return pts/possesions

    @classmethod
    def adjem(cls, oeff : float, navg: float)->float:
        """Computes adjusted efficiency margin, efficiency - avg.

        Args:
            oeff (float): the offensive efficiency of the team.
            navgo (float): the league average offensive efficiency.

        Returns:
            float: the adjusted efficiency margin.
        """
        return oeff - navg

    @classmethod
    def adjeff(cls, eff : float, navg : float, op_adj : float)->float:
        """Computes the adjusted efficiency.

        KenPom:
        I compute an adjusted offensive efficiency for each game 
        by multiplying the team’s raw offensive efficiency by the 
        national average efficiency and dividing by the opponent’s 
        adjusted defensive efficiency.

        We can use the same formula for adjusted offensive and defensive efficiencies.

        Args:
            eff (float): the efficiency of the team.
            navg (float): the nav.
            op_adj (float): the adjusted efficiency for the opponent for the opposite function (defense | offense).

        Returns:
            float: the adjusted offensive efficiency.
        """
        return (eff * navg)/op_adj



    def __init__(self, team : EfficiencyTeamlike, league : EfficiencyLeaguelike, recency : float):
        """Takes pts and possesions to initialize recency.

        Args:
            pts (float): A team's pts.
            possesions (float): A team's possessions.
            recency (float): The recency to use for a 
        """
        self.team = team
        self.league = league
        self.recency = recency

    def get_oeff(self)->float:
        """Gets the team's offensive efficiency.

        Returns:
            float: the team's offensive efficiency.
        """
        return Efficiency.eff(self.team.pts, self.team.possessions)

    def get_deff(self)->float:
        """Gets the team's deffensive efficiency.

        Returns:
            float: the team's defensive efficiency.
        """
        return Efficiency.eff(self.team.pts_against, self.team.possessions)


    def next_adjusted_oeff(self, opponent : EfficiencyTeamlike)->float:
        """Gets the next adjusted offensive efficiency value.

        Args:
            opponent (EfficiencyTeamlike): is the opponent played in the game used to update the value.

        Returns:
            float: the next adjusted offensive efficiency value.
        """
        return Efficiency.adjeff(self.get_oeff(), self.league.avg_oeff, opponent.adjusted_deff)

    def next_adjusted_deff(self, opponent : EfficiencyTeamlike)->float:
        """Gets the next adjusted defensive efficiency value.

        Args:
            opponent (EfficiencyTeamlike): is the opponent played in the game used to update the value.

        Returns:
            float: the next adjusted deffensive efficiency value.
        """
        return Efficiency.adjeff(self.team.pts_against, self.league.avg_deff, opponent.adjusted_deff)

    