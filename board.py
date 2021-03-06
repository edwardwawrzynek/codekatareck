from cell import Cell
from util import *
#represents a board of cells

class Board:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.board = []
        #construct the board
        for x in range(self.w):
            self.board.append([])
            for y in range(self.w):
                cell = Cell(x + y*self.w, x, y, [])
                self.board[x].append(cell)

        #create connections between cells
        for x in range(self.w):
            for y in range(self.h):
                if x > 0:
                    self.board[x][y].connectCell(self.board[x-1][y])
                if y > 0:
                    self.board[x][y].connectCell(self.board[x][y-1])
                if x < self.w-1:
                    self.board[x][y].connectCell(self.board[x+1][y])
                if y < self.h-1:
                    self.board[x][y].connectCell(self.board[x][y+1])

    #get cell with specified id
    def getCellById(self, id):
        return self.board[int(id % self.w)][int(id / self.w)]

    #update the given cells, including connection info (used to get info from log)
    def updateCellCons(self, id, api):
        cell = self.getCellById(id)
        cell.troops = api.getTroops(id)
        #handle adjacencies
        adjacencies = api.getAdjacencies(id)
        #remove ourselves from all current connections
        for a in cell.cons:
            if cell in a.cons:
                a.cons.remove(cell)

        cell.cons = []
        for a in adjacencies:
            a_cell = self.getCellById(a)
            cell.cons.append(a_cell)
            #add ourselves to other cell
            if not cell in a_cell.cons:
                a_cell.cons.append(cell)

    #just update cell's troop amount info
    def updateCellAmount(self, id, api):
        cell = self.getCellById(id)
        cell.troops = api.getTroops(id)


