import abc
import team

class Gamelike(metaclass=abc.ABCMeta):
    home : team.Teamlike
    away : team.Teamlike

    @abc.abstractmethod
    def __init__(self, home : team.Teamlike, away : team.Teamlike) -> None:
        self.home = home
        self.away = away

    @abc.abstractmethod
    def update_efficiency():
        pass
