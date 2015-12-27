'''
Created on Dec 26, 2015

@author: Alex Kaiser
'''
import argparse
from draw import draw
from points import points
from rankings import get_current_rankings


def main(tournament, tourn_type):
    points_list = points(tourn_type)
    if not points_list:
        print "Not a valid tournament type"
        return
    draw, seeds = draw(tournament)
    rankings = get_current_rankings("")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tourn", help="The current tournament.")
    parser.add_argument("--type", help="The tournament type, one of: " +
                        "Grand Slam, Masters 128, Masters 96," +
                        "ATP 500, ATP 250")
    args = parser.parse_args()
    main(args.tourn, args.type)
