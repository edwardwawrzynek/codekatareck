import requests

from util import *
from troops import Troops

import time

class Api:
    def __init__(self, url, teamPassword, teamColor):
        self.url = url
        self.teamPassword = teamPassword
        self.teamColor = teamColor

        self.logIndex = 0

    def getTeamOrder(self):
        return requests.get(self.url + "/api/teams/order").json()

    def getCurTeam(self):
        return TEAMS.index(requests.get(self.url + "/api/teams/current").text)

    def getTeamTerritory(self, teamColor):
        params = {"teamColor": TEAMS[teamColor]}
        return requests.get(self.url + "/api/teams/territories", params=params).json()

    def getAdjacencies(self, id):
        params = {"id": id}
        return requests.get(self.url + "/api/board/adjacencies", params=params).json()

    def getTroops(self, id):
        params = {"id": id}
        data = requests.get(self.url + "/api/board/troops", params=params)
        if data.text == "null":
            return Troops(-1, 0)
        data = data.json()
        if data["owner"] == "null":
            return Troops(-1, data["amount"])
        return Troops(TEAMS.index(data["owner"]), int(data["amount"]))

    def getNumCards(self, team):
        params = {"teamColor": TEAMS[team]}
        return requests.get(self.url + "/api/cards/amount", params=params).json()

    def getTroopsToCommit(self):
        return requests.get(self.url + "/api/troops/amount").json()

    def getActionLog(self):
        return requests.get(self.url + "/api/actions").json()

    #all action api calls return false on failure
    def commit(self, id, amount):
        params = {"teamPassword": self.teamPassword, "locationId": id, "amount": amount}
        req = requests.post(self.url + "/api/troops/add", params = params)
        if req.text == "null" or req.text == "false":
            return False

        return True

    def move(self, src_id, dst_id, amount):
        params = {"teamPassword": self.teamPassword, "fromId": src_id, "toId": dst_id, "amount": amount}
        req = requests.post(self.url + "/api/troops/move", params = params)
        if req.text == "null" or req.text == "false":
            return False

        return True

    def connect(self, id1, id2):
        params = {"teamPassword": self.teamPassword, "tileId1": id1, "tileId2": id2}
        req = requests.put(self.url + "/api/cards/connect", params = params)
        if req.text == "null" or req.text == "false":
            return False

    def inspireInsurgency(self, id):
        params = {"teamPassword": self.teamPassword, "tileId": id}
        req = requests.post(self.url + "/api/cards/inspireInsurgency", params = params)
        if req.text == "null" or req.text == "false":
            return False

        return True

    def disconnect(self, id):
        params = {"teamPassword": self.teamPassword, "tileId": id}
        req = requests.put(self.url + "/api/cards/disconnect", params = params)
        if req.text == "null" or req.text == "false":
            return False

        return True

    #wait for our turn (and call updateFunc)
    def waitForTurn(self, updateFunc=False):
        team = self.getCurTeam()

        while team != self.teamColor:
            time.sleep(0.2)
            team = self.getCurTeam()
            if updateFunc != False:
                updateFunc()

    #check for changes in the log, and return an array of new elements
    def getNewLog(self):
        log = self.getActionLog()
        if len(log) > self.logIndex:
            res = log[self.logIndex:]
            self.logIndex = len(log)
            return res

        return []