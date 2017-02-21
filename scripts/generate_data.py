'''
Created on Dec 26, 2015

@author: Alex Kaiser
'''
import argparse
from draw import draw, extend_seeds
from points import points
from find_current_tournament import find_current_tournament
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
    print("};\n")


def print_old_rankings(rankings):
    sorted(rankings, key=lambda ranking: ranking[1])
    print("var oldRankings = {")
    rank_num = 1
    for ranking in rankings:
        print('    "{}": {},'.format(ranking[0], rank_num))
        rank_num += 1
    print("};\n")


def print_results(results):
    print("var results = {")
    rank_num = 1
    for key in results:
        print('    {}: "{}",'.format(key, results[key]))
        rank_num += 1
    print("};\n")


def print_seeds(seeds):
    print("var seeds = {")
    for key, value in sorted(iter(seeds.items()), key=lambda x: x[1]):
        print('    "{}": {},'.format(key, value))
    print("};\n")


def print_players(matches):
    print("var players =\n[")
    print("    '" + "',\n    '".join(matches), end="")
    print("'\n];\n")


def main(args):
    """
    Gets all the information for the current rankings and tournament and then
    prints them in the correct format to be used in javascript.

    Example run:
        python generate_data.py -n 300 "Brisbane" "ATP 250" > ../static/data.js
    """
    if args.tournament:
        tournament = args.tournament
    else:
        tournament = find_current_tournament()
    points_list = points(tournament)
    matches, seeds, results = draw(tournament)
    num_rankings = args.num_rankings
    current_rankings = get_current_rankings(num_rankings)
    new_rankings = subtract_tournament(current_rankings, tournament)
    seeds = extend_seeds(matches, seeds, current_rankings)
    print_players(matches)
    print_seeds(seeds)
    print_new_rankings(new_rankings)
    print_old_rankings(current_rankings)
    print_results(results)
    print_points([str(p) for p in points_list])
    print("var tournament = '{}';".format(tournament))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tournament", help="The current tournament name")
    parser.add_argument("-n",
                        "--num_rankings",
                        type=int,
                        help="Number of rankings to download",
                        default=300)
    args = parser.parse_args()
    main(args)
