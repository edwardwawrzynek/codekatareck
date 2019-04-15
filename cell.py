from troops import Troops
from util import *

#A cell on the board
class Cell:
    #connections is array of cells that this cell is connected to
    def __init__(self, id, x, y, connections):
        self.id = id
        self.x = x
        self.y = y
        self.cons = connections
        #number of troops (only one team can occupy a space at a time)
        self.troops = Troops(-1, 0)

    def connectCell(self, cell):
        self.cons.append(cell)

    def unconnectCell(self, cell):
        self.cons = []

