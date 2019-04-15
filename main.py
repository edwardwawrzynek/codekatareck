#! /usr/bin/env python3

import sys
from api import Api
from util import *
from board import Board

#commit to an initial corner
def commitToCorner(api):
        amount = api.getTroopsToCommit()

        corners = [0, 24, 600, 624]
        for p in corners:
                if api.commit(p, amount):
                        return p

        print("Couldn't choose a corner to commit to")
        return -1

def main(team, password, url):
        api = Api(url, password, team)
        board = Board(25, 25)

        #Choose initial corner
        api.waitForTurn()
        corner = commitToCorner(api)
        print("Team " + TEAMS[team] + " got corner " + str(corner))



if len(sys.argv) != 4:
        print("Usage: main.py TEAM_NAME team_password url")
        exit(1)

team = TEAMS.index(sys.argv[1])
main(team, sys.argv[2], "http://" + sys.argv[3])