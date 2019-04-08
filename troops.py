#represents an amount of troops of the same color
class Troops:
    #team is an index of 0-3 in [YELLOW, BLUE, RED, GREEN]
    def __init__(self, team, num):
        self.team = team
        self.num = num
    
    def setNumTroops(self, num):
        self.num = num
    
    def getNumTroops(self, num):
        return self.num

    def setTeam(self, team):
        self.team = team
    
    def getTeam(self, team)
        return self.team