from util import *

#represents an amount of troops of the same color
class Troops:
    #team is an index of 0-3 in [YELLOW, BLUE, RED, GREEN]
    def __init__(self, team, num):
        self.team = team
        self.num = num

    def setNumTroops(self, num):
        assert_warn(num >= 0, "setting troops to less than 0")
        self.num = num
        if self.num == 0:
            self.team = -1

    def getNumTroops(self):
        return self.num

    def setTeam(self, team):
        self.team = team

    def getTeam(self):
        return self.team