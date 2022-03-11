from gsdk.models.ncaab.division.divisionlike import Teamalog
from gsdk.models.ncaab.team import efficiency
from ... import division
from ... import team
from ..... import integrations
import datetime
from typing import Sequence
from . import models
import redis

class TeamEfficiencyController(team.efficiencylike.Controlleralog):

    r : redis.Redis[bytes] = redis.Redis(host='localhost', port=6379, db=0)
    key : str
    date : datetime.date
    efficiency_meta : models.EfficiencyRedisMeta

    def __init__(self, key : str, date : datetime.date = datetime.date.today()) -> None:
        self.key = key
        self.efficiency_meta = models.EfficiencyRedisMeta(self.key, self.r)
        self.date = date

    def get(self, efficiency : team.efficiencylike.Efficiencylike):
        """Populates an efficiency model.

        Args:
            efficiency (team.efficiencylike.Efficiencylike): _description_
        """
        eff = self.efficiency_meta.get_team_efficiency(str(efficiency.team.id), self.date)
        efficiency.possessions = eff.possessions
        efficiency.kadjoeff = eff.kadjoeff
        efficiency.kadjdeff = eff.kadjdeff
        efficiency.badjoeff = eff.badjoeff
        efficiency.badjdeff = eff.badjdeff
        efficiency.radjoeff = eff.badjdeff

    def serialize(self, efficiency: team.efficiencylike.Efficiencylike) -> None:
        """Serializes the efficiency model.

        Args:
            efficiency (team.efficiencylike.Efficiencylike): _description_
        """
        self.efficiency_meta.commit_efficiency(models.EfficiencyPayload(efficiency.__dict__))



class TeamController(team.teamlike.Controlleralog):

    key : str
    date : datetime.date
    efficiency_controller : team.efficiencylike.Controlleralog

    def __init__(self, key : str, date : datetime.date) -> None:
        self.key = key
        self.date = date
        self.efficiency_controller = TeamEfficiencyController(key, date)

    def get(self, team : team.teamlike.Teamlike):
        pass

    def serialize(self, team: team.teamlike.Teamlike) -> None:
        pass



class Team(division.divisionlike.Teamalog):

    _team : team.team.Team

    def __init__(self, team : team.team.Team) -> None:
        self._team = team

    def biupdate_and_serialize(
        self, 
        opponent: division.divisionlike.Teamalog, 
        pppf: float, 
        pppa: float, 
        recency: float = 0.2
    ) -> None:

        self._team.eff.biupdate_and_serialize(
            opponent.eff, 
            pppf, 
            pppa, 
            recency
        )


class Game(division.divisionlike.Gamealog):

    home : division.divisionlike.Teamalog
    home_pts : int
    away : division.divisionlike.Teamalog
    away_pts : int

    def __init__(
        self, 
        home_id : int, 
        home_pts : int, 
        away_id : int,
        away_pts : int
    ) -> None:
        self.home = team.team.Team(home_id)
        self.home_pts = home_pts
        self.away = team.team.Team(away_id)
        self.away_pts = away_pts

 

class DivisionController(division.divisionlike.Controlleralog):
    
    def get_games_on_date(self, date: datetime.datetime) -> Sequence[division.divisionlike.Gamealog]:
        sports_data_games = integrations.sportsdataio.ncaab.ncaab\
            .Ncaab().games.by_date.get_games(date)
        return [Game(
            home_id=game.home_team_id,
            home_pts=game.home_team_score,
            away_id=game.away_team_id,
            away_pts=game.away_team_score
        ) for game in sports_data_games]


