"""
Breakdown of how much each round at each type of tournament is worth.

@author: Alex Kaiser
"""


def points(tournament_level):
    if tournament_level == "Grand Slam":
        return [10, 45, 90, 180, 360, 720, 1200, 2000]
    elif tournament_level == "Masters 128":
        return [10, 25, 45, 90, 180, 360, 600, 1000]
    elif tournament_level == "Masters 96":
        return [10, 45, 90, 180, 360, 600, 1000]
    elif tournament_level == "ATP 500":
        return [20, 45, 90, 180, 300, 500]
    elif tournament_level == "ATP 250":
        return [5, 20, 45, 90, 150, 250]


tournament_types = ["Grand Slam",
                    "Masters 128",
                    "Masters 96",
                    "ATP 500",
                    "ATP 250"]
