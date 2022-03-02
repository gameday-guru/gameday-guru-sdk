from . import teamlike
from . import efficiencylike
from typing import Type
from . import efficiency

class Team(teamlike.Teamlike):
    """An NCAAB team.
    """

    pts : float
    pts_against : float
    name : str
    id : int
    controller : teamlike.TeamControllerlike
    eff : efficiencylike.Efficiencylike

    def __init__(
        self, 
        division : teamlike.TeamDivisonlike, 
        controller : teamlike.TeamControllerlike,
        efficiency_dependency : Type[efficiencylike.Efficiencylike] = efficiency.Efficiency
    ):
        """Initializes a team using a division and a controller.

        Args:
            division (TeamDivisonlike): is the division of which the team is a member.
            controller (TeamControllerlike):  controller is the controller for the team's operations.
        """
        self.eff = efficiency_dependency(self, division.efficiency, controller.efficiency_controller)

    def __hash__(self)->int:
        return self.id