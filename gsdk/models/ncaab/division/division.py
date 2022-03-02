from . import divisionlike
from . import efficiencylike
from . import efficiency
from typing import Type, List, cast
import datetime

class Division(divisionlike.Divisionlike):
    
    controller : divisionlike.DivisionControllerlike
    efficiency : efficiencylike.Efficiencylike

    def __init__(self, 
        controller : divisionlike.DivisionControllerlike,
        efficiency : Type[efficiencylike.Efficiencylike] = efficiency.Efficiency
    ):
        self.controller = controller
        self.efficiency = efficiency(cast(efficiencylike.EfficiencyDivisionlike, self))

    def get_games_on_date(self, date: datetime.datetime) -> List[divisionlike.DivisionGamelike]:
        return self.controller.get_games_on_date(date)
