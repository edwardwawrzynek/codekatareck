#! /usr/bin/env python3

import sys
from api import Api
from util import *
from board import Board

#commit to an initial corner
def commitToCorner(api, board):
	amount = api.getTroopsToCommit()

	corners = [0, 24, 600, 624]
	for p in corners:
		if board.getCellById(p).troops.getNumTroops() != 0 and board.getCellById(p).troops.getTeam() != api.teamColor:
			continue
		if api.commit(p, amount):
			return p

	print("Couldn't choose a corner to commit to")
	return -1

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

#find the square with minimum troops
#if borders_only, only choose squares on the border
def findMinCell(territories, borders_only, board, api):
	min_a = 100000
	minCell = 0
	for t in territories:
		t_troops = board.getCellById(t).troops.getNumTroops()
		#only consider square if it has a bordering cell that we don't own (borders of boundry)
		cons = board.getCellById(t).cons
		is_border = False
		for con in cons:
			if con.troops.getTeam() != api.teamColor:
				is_border = True
		if t_troops < min_a and (is_border or (not borders_only)):
			min_a = t_troops
			minCell = board.getCellById(t)

	if minCell != 0:
		return minCell
	else:
		return None

#choose spots to commit troops to
def commitTroops(api, board):
	if api.getCurTeam() != api.teamColor:
		print("Warning: not our turn")

	troops = api.getTroopsToCommit()
	territories = api.getTeamTerritory(api.teamColor)

	#list of commits to each cell
	commits = [0] * 625

	#find min, commit 1 troops to that, and repeat (slow but works)
	while troops > 0:
		minCell = findMinCell(territories, True, board, api)

		if minCell != None:
			commits[minCell.id] += 1
			minCell.troops.setNumTroops(minCell.troops.getNumTroops() + 1)
			troops -= 1
		else:
			minCell = findMinCell(territories, False, board, api)
			if minCell != None:
				commits[minCell.id] += 1
				minCell.troops.setNumTroops(minCell.troops.getNumTroops() + 1)
				troops -= 1
			else:
				print("Warning: couldn't find territory to commit to")
				break

	#do the commits now (creates less to handle in logs, as successive commits to same square are combined)
	for i in range(625):
		if commits[i] == 0:
			continue
		api.commit(i, commits[i])


#do all of the troops moving
def moveTroops(api, board):
	#basic algorithm:
	#attack if we can, else
	#for each of our territories, give out one troop to each until they have more than us
	territories = api.getTeamTerritory(api.teamColor)

	for t in territories:
		cell = board.getCellById(t)
		adjs = cell.cons

		#check if we need to attack
		doAttack = False
		for a in adjs:
			#if owned by other, attack with all troops
			if a.troops.getTeam() != api.teamColor and a.troops.getNumTroops() > 0:
				api.move(cell.id, a.id, cell.troops.getNumTroops())
				doAttack = True
				break

		#else, try to even out distribution
		if not doAttack:
			#number of cells, including us, we need to distribute to
			num_to_dist = 1
			#sum of all troops currently in cells we are going to distribute to
			sum_to_dist = cell.troops.getNumTroops()
			for a in adjs:
				#don't move troops to those with more
				if a.troops.getNumTroops() >= cell.troops.getNumTroops() - 2:
					continue
				num_to_dist += 1
				sum_to_dist += a.troops.getNumTroops()

			target_amount = int(sum_to_dist / num_to_dist)

			#actually move
			for a in adjs:
				#don't move troops to those with more
				if a.troops.getNumTroops() >= cell.troops.getNumTroops() - 2:
					continue

				api.move(cell.id, a.id, target_amount - a.troops.getNumTroops())

#play our cash cards if we can (for now, just disconnect enemy tiles)
def playCards(api, board):
	while api.getNumCards(api.teamColor) >= 8:
		max_troops = 0
		max_cell = 0
		#find cell with most troops
		for i in range(625):
			cell = board.getCellById(i)
			if cell.troops.getTeam() != api.teamColor and cell.troops.getNumTroops() > max_troops and len(cell.cons) > 0:
				max_troops = cell.troops.getNumTroops()
				max_cell = cell

		if max_cell != 0:
			#figure out how many insurgencies we will need to remove the troops there
			num_insurgencies = int(max_cell.troops.getNumTroops() / 7) + 1
			if api.getNumCards(api.teamColor) < 4 + 4*num_insurgencies:
				return
			#inspire an incergency as many times as we need
			for i in range(num_insurgencies):
				if not api.inspireInsurgency(max_cell.id):
					print("failed to inspire insurgency")

			if api.getTroops(max_cell.id).getTeam() != -1:
				print("failed to inspire insurgency")
			else:
				#disconnect
				if not api.disconnect(max_cell.id):
					return

			board.updateCellCons(max_cell.id, api)

#main game loop after we have choosen a corner
def mainLoop(api, board, corner):
	while 1:
		# wait
		api.waitForTurn(updateFunc=lambda: handleLog(api, board))
		print("team " + TEAMS[api.teamColor] + " starting turn")
		print("playing cards")
		playCards(api, board)
		print("moving")
		moveTroops(api, board)
		print("committting")
		commitTroops(api, board)

		# if we have uncommited troops left for some reason, commit to our corner
		if api.getCurTeam() == api.teamColor and api.getTroopsToCommit() != 0:
			print("Warning: for some reason, not all of our troops were committed. Comitting to our first owned territory")
			territory = api.getTeamTerritory(api.teamColor)
			api.commit(territory[0], api.getTroopsToCommit())

def main(team, password, url):
	api = Api(url, password, team)
	board = Board(25, 25)

	#Choose initial corner
	api.waitForTurn()
	handleLog(api, board)
	corner = commitToCorner(api, board)
	print("Team " + TEAMS[team] + " got corner " + str(corner) + "\nStarting main game logic\n------------------------\n")

	mainLoop(api, board, corner)
	exit()



if len(sys.argv) != 4:
	print("Usage: main.py TEAM_NAME team_password url")
	exit(1)

team = TEAMS.index(sys.argv[1])
main(team, sys.argv[2], "http://" + sys.argv[3])