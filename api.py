import requests

from main import TEAMS

class api:
    def __init__(self, url, teamPassword, teamColor):
        self.url = url
        self.teamPassword = teamPassword
        self.teamColor = teamColor

    def getTeamOrder(self):
        return requests.get(self.url + "/api/teams/order").json()

    def getTeamTerritory(self, teamColor):
        params = {"teamColor": TEAMS[teamColor]}
        return requests.get(self.url + "/api/teams/territories", params=params).json()

api = api("http://localhost:8080", 0, 0)

print(api.getTeamTerritory(0))