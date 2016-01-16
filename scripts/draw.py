"""
Gets the draw for the current tournament.

@author: Alex Kaiser
"""

import html
import random
import requests
import lxml.html
from tqdm import tqdm


def get_tournament_url(current_tournament, root_url):
    """
    Gets the url where the draw can be found for the current tournament

    Args:
        current_tournament (str): The city of the current tournament
        root_url (str): The base url to use

    Returns:
        str: The url where the draw can be found
    """
    page = requests.get(root_url + '/en/tournaments')
    tree = lxml.html.fromstring(page.content)
    all_tournaments = tree.xpath('//li[@class=" has-link no-padding"]/a')
    for tournament in all_tournaments:
        if current_tournament in tournament.text:
            link = tournament.get("href")[15:-9]
            tournament_url = root_url + "/en/scores/current" + link + "/draws"

    return tournament_url + "?matchType=singles"


def _create_random_seeds(matches, seeds):
    """
    For players that are in matches, but not in seeds, assign a random seed
    that is greater than the rest of the seeds, and then assign the "Bye"
    player the last seed

    Args:
        matches (list of str): All the players in the first round
        seeds (dict str->int):
            Dictionary of already assigned seeds player->seed

    Returns:
        None (Adds to the seeds dictionary the new seeds)
    """
    max_seed = _find_max_seed(seeds)
    bye = False
    for player in random.sample(matches, len(matches)):
        if player == "Bye":
            bye = True
        elif player not in seeds:
            seeds[player] = max_seed
            max_seed += 1
    if bye:
        seeds["Bye"] = max_seed


def extend_seeds(matches, seeds, rankings):
    """
    Add to the seeds players who are not seeded, but are in the rankings, in
    the order that they are in the rankings

    Args:
        matches (list of str): All the players in the first round
        seeds (dict str->int):
            Dictionary of already assigned seeds player->seed
        rankings (list): Current rankings in form [player, points, link]

    Returns:
        dict: Dictionary same as seeds, but with the new rankings added
    """
    sorted(rankings, key=lambda ranking: ranking[1])
    max_seed = _find_max_seed(seeds)
    for ranking in rankings:
        player = ranking[0]
        if player in matches and player not in seeds:
            seeds[player] = max_seed
            max_seed += 1
    _create_random_seeds(matches, seeds)
    return seeds


def _find_max_seed(seeds):
    """Finds one plus the max seed in the seeds dictionary"""
    max_seed = 0
    for key in seeds:
        if seeds[key] > max_seed:
            max_seed = seeds[key]
    max_seed += 1
    return max_seed


def draw(current_tournament,
         root_url='http://www.atpworldtour.com'):
    """
    Return the draw and seeds for the current tournament.

    Args:
        current_tournament (str):
            The name of the city of the current tournament
        root_url (str): The root url to use

    Returns:
        matches (list): List of players in the first round in order
        seeds (dict str->int): Order that the players are expected to win, this
            goes by seeds first and then world ranking, and then random
    """
    # The grand slams aren't on the atp website for draws, so they have to be parsed differently
    if current_tournament == "Australian Open":
        matches, seeds = parse_australian_open_draw()
    else:
        matches, seeds = parse_atp_draw(current_tournament, root_url)
    return matches, seeds


def draw_for_grand_slam(url):
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    
    matches = [];
    seeds = {};
    
    for player_link in tree.xpath('//a[@class="sc"]'):
        if not player_link.text:
            text = player_link.getparent().text_content()
            for line in text.split("\n"):
                player_line = line.strip()
                if player_line:
                    if not "(" in player_line:
                        matches.append("Bye")
                    else:
                        player = player_line[0:player_line.index("(")-1]
                        matches.append(player)
                        if "[" in player_line:
                            start = player_line.index("[") + 1
                            end = player_line.index("]")
                            seed = player_line[start:end]
                            seeds[player] = int(seed)
        
    return matches, seeds


def parse_australian_open_draw():
    """
    Return the draw and seeds for the australian open
    """
    base_url = "http://www.ausopen.com/en_AU/scores/draws/ms/"
    
    matches = [];
    seeds = {};
    
    for section in range(1,5):
        url = base_url + "r1s" + str(section) + ".html"
        section_matches, section_seeds = draw_for_grand_slam(url)
        for match in section_matches:
            matches.append(match)
        for key in section_seeds:
            seeds[key] = section_seeds[key]
        
    return matches, seeds


def parse_atp_draw(current_tournament, root_url):
    """
    Args:
        current_tournament (str):
            The name of the city of the current tournament
        root_url (str): The root url to use

    Returns:
        matches (list): List of players in the first round in order
        seeds (dict str->int): Order that the players are expected to win, this
    """
    tournament_url = get_tournament_url(current_tournament, root_url)
    page = requests.get(tournament_url)
    tree = lxml.html.fromstring(page.content)

    matches = []
    seeds = {}

    for match in tqdm(tree.xpath('//table[@class=' +
                                 '"scores-draw-entry-box-table"]')):
        for player_box in match.xpath('tbody/tr'):
            players = player_box.xpath('td/a')
            if players:
                player = players[0]
                player = html.unescape(player.get("data-ga-label"))
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

    return matches, seeds

# To be used for testing
if __name__ == '__main__':
    matches, seeds = draw("Australian Open")
    print(matches)
    print(seeds)
