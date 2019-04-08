from troops import Troops
from main import *

#A cell on the board
class Cell:
    #connections is array of cells that this cell is connected to
    def __init__(self, id, x, y, connections):
        self.id = id
        self.x = x
        self.y = y
        self.cons = connections
        #number of troops 
        self.troops = [Troops(TEAM_YELLOW, 0), Troops(TEAM_BLUE,0), Troops(TEAM_RED,0), Troops(TEAM_GREEN,0)]
    
    def connectCell(self, cell):
        self.cons.append(cell)
    
    def unconnectCell(self, cell):
        try:
            self.cons.remove(cell)
            return True
        except ValueError:
            return False
    
