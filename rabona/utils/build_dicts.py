import os


club_league_dict = {}


def getdir(): return list(
    filter(os.path.isdir, [item for item in os.listdir()]))


os.chdir('data/leagues')
leagues = getdir()

for league in leagues:
    os.chdir(league)
    clubs = getdir()
    for club in clubs:
        club_league_dict[club] = league
    os.chdir('..')
