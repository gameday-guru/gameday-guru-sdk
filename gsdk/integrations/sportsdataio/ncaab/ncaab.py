import requests
"https://api.sportsdata.io/v3/cbb/scores/json/GamesByDate/2018-FEB-27?key=7f63ca312eab45d19be1574b93cc369d"


class NCAAB:
    pass

print(requests.get("https://api.sportsdata.io/v3/cbb/scores/json/GamesByDate/2018-FEB-27?key=7f63ca312eab45d19be1574b93cc369d").json())