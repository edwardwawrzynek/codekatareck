# if condition is false, print warning
def assert_warn(cond, msg):
    if not cond:
        print("Warning: " + msg)

TEAM_YELLOW = 0
TEAM_BLUE = 1
TEAM_RED = 2
TEAM_GREEN = 3

TEAMS = ["YELLOW", "BLUE", "RED", "GREEN"]