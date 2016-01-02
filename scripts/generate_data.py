'''
Created on Dec 26, 2015

@author: Alex Kaiser
'''
import argparse
from draw import draw
from points import points, tournament_types
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


def main(args):
    tournament = args.tournament
    points_list = points(args.type)
    if not points_list:
        print("Not a valid tournament type")
        return
    matches, seeds = draw(tournament)
    if args.num_rankings:
        num_rankings = args.num_rankings
    else:
        num_rankings = 300
    rankings = get_current_rankings(num_rankings)
    rankings = subtract_tournament(rankings, tournament)
    print_players(matches)
    print_seeds(seeds)
    print_rankings(rankings)
    print_points([str(p) for p in points_list])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("tournament", help="The current tournament name")
    parser.add_argument("type",
                        help="The tournament type",
                        choices=tournament_types)
    parser.add_argument("-n",
                        "--num_rankings",
                        type=int,
                        help="Number of rankings to download")
    args = parser.parse_args()
    main(args)
