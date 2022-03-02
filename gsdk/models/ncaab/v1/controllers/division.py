from ... import division
import datetime
from typing import List

class DivisionController(division.divisionlike.DivisionControllerlike):
    

    def get_games_on_date(self, date: datetime.datetime) -> List[division.divisionlike.DivisionGamelike]:
        return super().get_games_on_date(date)


