"""
Gets the draw for the current tournament.

@author: Alex Kaiser
"""

import random
import requests
from lxml import html
from tqdm import tqdm


def get_tournament_url(current_tournament, root_url):
    page = requests.get(root_url + '/en/tournaments')
    tree = html.fromstring(page.content)
    all_tournaments = tree.xpath('//li[@class=" has-link no-padding"]/a')
    for tournament in all_tournaments:
        if current_tournament in tournament.text:
            link = tournament.get("href")[15:-9]
            tournament_url = root_url + "/en/scores/current" + link + "/draws"

    return tournament_url + "?matchType=singles"


def create_random_seeds(matches, seeds):
    max_seed = 0
    for key in seeds:
        if seeds[key] > max_seed:
            max_seed = seeds[key]
    max_seed += 1
    bye = False
    for player in random.sample(matches, len(matches)):
        if player == "Bye":
            bye = True
        elif player not in seeds:
            seeds[player] = max_seed
            max_seed += 1
    if bye:
        seeds["Bye"] = max_seed


def draw(current_tournament,
         root_url='http://www.atpworldtour.com'):
    tournament_url = get_tournament_url(current_tournament, root_url)
    page = requests.get(tournament_url)
    tree = html.fromstring(page.content)

    matches = []
    seeds = {}

    for match in tqdm(tree.xpath('//table[@class=' +
                                 '"scores-draw-entry-box-table"]')):
        for player_box in match.xpath('tbody/tr'):
            players = player_box.xpath('td/a')
            if players:
                player = players[0]
                player = player.get("data-ga-label")
                matches.append(player)
            else:
                matches.append("Bye")
            seed_box = player_box.xpath('td/span')
            if seed_box:
                seed = seed_box[0]
                seed = seed.text.strip().strip("()")
                if player:
                    if seed.isdigit():
                        seeds[player] = int(seed)
                else:
                    print("ERROR: Found seed without player")

    create_random_seeds(matches, seeds)

    return matches, seeds

if __name__ == '__main__':
    matches, seeds = draw("Brisbane")
    print(matches)
    print(seeds)
