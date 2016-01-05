'''
Created on Dec 26, 2015

@author: Alex Kaiser
'''
import argparse
from draw import draw, extend_seeds
from points import points, tournament_types
from rankings import get_current_rankings, subtract_tournament


def print_points(points):
    print("var points = [", end=' ')
    points_list = ", ".join(points)
    print(points_list, end=' ')
    print("];")


def print_new_rankings(rankings):
    sorted(rankings, key=lambda ranking: ranking[1])
    print("var rankings = {")
    for ranking in rankings:
        print('    "{}": {},'.format(ranking[0], ranking[1]))
    print("}\n")


def print_old_rankings(rankings):
    sorted(rankings, key=lambda ranking: ranking[1])
    print("var oldRankings = {")
    rank_num = 1
    for ranking in rankings:
        print('    "{}": {},'.format(ranking[0], rank_num))
        rank_num += 1
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
    """
    Gets all the information for the current rankings and tournament and then
    prints them in the correct format to be used in javascript.

    Example run:
        python generate_data.py -n 300 "Brisbane" "ATP 250" > ../static/data.js
    """
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
    current_rankings = get_current_rankings(num_rankings)
    new_rankings = subtract_tournament(current_rankings, tournament)
    seeds = extend_seeds(matches, seeds, current_rankings)
    print_players(matches)
    print_seeds(seeds)
    print_new_rankings(new_rankings)
    print_old_rankings(current_rankings)
    print_points([str(p) for p in points_list])
    print("var tournament = '{}';".format(tournament))


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
