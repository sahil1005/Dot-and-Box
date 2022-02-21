import re
import os

def get_games(filename):
    """
    Looks at a results file and turns it into a list of games.
    Games are a list of all associated moves and the final score.
    args:
        filename(str): filename for results file
    returns:
        list[][str]
    """
    with open(filename, "r") as infile:
        lines = infile.readlines()
    fnList = filename.split("_")
    p1name = fnList[1]
    p2name = fnList[3]
    width = int(fnList[4][0])
    height = int(fnList[4][2])
    no_moves = ((width-1)*height + (height-1)*width)+2
    games = []
    start = 0
    end = no_moves
    while end <= len(lines):
        game = lines[start:end]
        games.append(game)
        start, end = end, end+no_moves
    games.append([p1name, p2name])
    return games

def count_winners(games):
    """
    Takes a list of list of games, provided by get_games, and prints the number of
    wins each player got.
    Args:
        games(list[][str]): List of games
    """
    names = games.pop(-1)
    p1wins = 0
    p2wins = 0
    draws = 0
    for game in games:
        scores = [int(s) for s in re.findall(r'\d+', game[-1])]
        if len(scores) > 2:
            print("Too many values in list {}".format(scores))
        if scores[0] > scores[1]:
            p1wins += 1
        elif scores[1] > scores[0]:
            p2wins += 1
        else:
            draws += 1
    if p1wins == 1:
        p1s = ""
    else:
        p1s = "s"
    if p2wins == 1:
        p2s = ""
    else:
        p2s = "s"
    print("{} player won {} time{} and {} player won {} time{} out of {}.".format(names[0], p1wins, p1s, names[1], p2wins, p2s, p1wins+p2wins+draws))
    if draws > 0:
        if draws == 1:
            was = "was"
            draw = "draw"
        else:
            was = "were"
            draw = "draws"
        print("There {} {} {}.".format(was, draws, draw))
    if p1wins+p2wins+draws > 0:
        print("{} player winrate: {}%".format(names[0], 100*p1wins/(p1wins+p2wins+draws)))
        print("{} player winrate: {}%".format(names[1], 100*p2wins/(p1wins+p2wins+draws)))
    return [p1wins, p2wins, draws]

def get_scores(filename):
    games = get_games(filename)
    count_winners(games)


def get_filenames(dirname):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(dirname):
        f.extend(filenames)
        break
    filenames = [dirname+"\\"+x for x in f]
    return filenames

def compare_folder(dirname):
    filenames = get_filenames(dirname)
    compare(filenames)


def compare(filenames):
    gameset = [get_games(fn) for fn in filenames]
    results = []
    for games in gameset:
        [p1wins, p2wins, draws] = count_winners(games)
        p1winrate = 100*p1wins/(p1wins+p2wins+draws)
        p2winrate = 100*p2wins/(p1wins+p2wins+draws)
        results.append([p1wins, p2wins, draws, p1winrate, p2winrate])
    p1bestwinrate = 0
    p1bestwinrateindex = -1
    p2bestwinrate = 0
    p2bestwinrateindex = -1
    for i, result in enumerate(results):
        if result[3] >= p1bestwinrate:
            p1bestwinrate = result[3]
            p1bestwinrateindex = i
        if result[4] >= p2bestwinrate:
            p2bestwinrate = result[4]
            p2bestwinrateindex = i

    print("Best Winrate achieved by p1: {}%\n In results file {}".format(p1bestwinrate, filenames[p1bestwinrateindex]))
    print("Best Winrate achieved by p2: {}%\n In results file {}".format(p2bestwinrate, filenames[p2bestwinrateindex]))
