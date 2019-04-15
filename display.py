#! /usr/bin/env python3

import sys
from api import Api
from util import *
from board import Board
import time
from termcolor import colored, cprint

#handle changes in log
def handleLog(api, board):
	log = api.getNewLog()
	for entry in log:
		entry = entry.split()
		action = entry[1]
		args = entry[2:]
		if action == "commit":
			board.updateCellAmount(int(args[0]), api)
		elif action == "move":
			board.updateCellAmount(int(args[0]), api)
			board.updateCellAmount(int(args[1]), api)
		elif action == "connect":
			board.updateCellCons(int(args[0]), api)
			board.updateCellCons(int(args[1]), api)
		elif action == "insurgency":
			board.updateCellAmount(int(args[0]), api)
		elif action == "disconnect":
			board.updateCellCons(int(args[0]), api)
		elif action == "end":
			pass
		else:
			print("unknown verb in action log: " + str(action))

#print state of game
def printState(api, board):
	print("\033[%d;%dH" % (0, 0))
	print("-" * (25*3))
	#don't show connections, just squares and amounts
	for y in range(25):
		for x in range(25):
			#check if tile is disconnected
			amount = board.board[x][y].troops.getNumTroops()
			disconnected = len(board.board[x][y].cons) == 0
			if amount == 0:
				if disconnected:
					print(colored(" . ", "white", "on_white"), end="")
				else:
					print(colored(" . ", "white"), end="")
			else:
				if disconnected:
					print(colored(str(board.board[x][y].troops.getNumTroops()).rjust(2, " "), colors[board.board[x][y].troops.getTeam()], "on_white"), end=" ")
				else:
					print(colored(str(board.board[x][y].troops.getNumTroops()).rjust(2, " "), colors[board.board[x][y].troops.getTeam()]), end=" ")

		print()

	print("-" * (25*3))

	team = api.getCurTeam()
	print("Current Team: " + colored(TEAMS[team], colors[team]) + " " * 10)

	print("Cells Controlled:")
	for i in range(len(TEAMS)):
		territories = api.getTeamTerritory(i)
		print("  " + colored(TEAMS[i], colors[i]) + ": " + str(len(territories)) + " " * 3 + "\t", end="")

	print("\nCards:")
	for i in range(len(TEAMS)):
		cards = api.getNumCards(i)
		print("  " + colored(TEAMS[i], colors[i]) + ": " + str(cards) + " " * 3 + "\t", end="")

	print()

#update all cells (only on program start)
def initState(api, board):
	for i in range(625):
		print("\033[%d;%dH" % (0, 0))
		print("cell " + str(i) + " of 625")
		board.updateCellCons(i, api)

	api.logIndex = len(api.getActionLog())

#main game loop after we have choosen a corner
def mainLoop(api, board):
	while 1:
		# wait
		time.sleep(0.2)
		handleLog(api, board)

		printState(api, board)


def main(team, password, url):
	api = Api(url, password, team)
	board = Board(25, 25)

	print("Loading Initial Board State...")
	initState(api, board)

	mainLoop(api, board)
	exit()



if len(sys.argv) != 2:
	print("Usage: display.py url")
	exit(1)

main("test", "test", "http://" + sys.argv[1])