'''
Created on Dec 26, 2015

@author: Alex Kaiser
'''
import argparse
from draw import draw
from points import points
from rankings import get_current_rankings, subtract_tournament


def print_points(points):
    print("var points = [", end=' ')
    points_list = ", ".join(points)
    print(points_list, end=' ')
    print("];")


def print_rankings(rankings):
    sorted(rankings, key=lambda ranking: ranking[1])
    print("var rankings = {")
    for ranking in rankings:
        print('    "{}": {},'.format(ranking[0], ranking[1]))
    print("}\n")


def print_seeds(seeds):
    print("var seeds = {")
    for key, value in sorted(iter(seeds.items()), key=lambda x: x[1]):
        print('    "{}": {},'.format(key, value))
    print("}\n")


def print_players(matches):
    print("var players =\n[")
    print("    '" + "',\n    '".join(matches), end="")
    print("'\n]\n")


def main(tournament, tourn_type):
    points_list = points(tourn_type)
    if not points_list:
        print("Not a valid tournament type")
        return
    matches, seeds = draw(tournament)
    rankings = get_current_rankings(300)
    rankings = subtract_tournament(rankings, tournament)
    print_players(matches)
    print_seeds(seeds)
    print_rankings(rankings)
    print_points([str(p) for p in points_list])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tourn", help="The current tournament.")
    parser.add_argument("--type", help="The tournament type, one of: " +
                        "Grand Slam, Masters 128, Masters 96," +
                        "ATP 500, ATP 250")
    args = parser.parse_args()
    main(args.tourn, args.type)
