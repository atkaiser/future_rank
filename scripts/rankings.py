"""
Methods in this script deal with getting ranking points for players.

@author: Alex Kaiser
"""

from datetime import date, timedelta
import requests
from lxml import html
from tqdm import tqdm

# current_tournament = "Australian Open"
# root_url = 'http://www.atpworldtour.com'


def get_current_rankings(num_rankings,
                         root_url="http://www.atpworldtour.com"):
    """
    Gets the current rankings from the base url

    Args:
        num_rankings (int): The number of rankings to return
            (i.e. 1-num-rankings)
        root_url: The base url to use

    Returns:
        list: List of rankings where each element is a list of
            [player (str), points (int), link_to_detailed_rankings (str)]
    """
    last_monday = date.today()
    while last_monday.weekday() != 0:
        last_monday -= timedelta(days=1)
    current_rankings = []
    while (not current_rankings):
        page = requests.get(root_url +
                            '/en/rankings/singles?rankDate=' +
                            str(last_monday) +
                            '&rankRange=1-' +
                            str(num_rankings))
        tree = html.fromstring(page.content)

        all_players = tree.xpath('//table[@class="mega-table"]/tbody')[0]

        for player_row in tqdm(all_players):
            name = player_row.xpath('td[@class="player-cell"]/a/text()')[0]
            points_cell = player_row.xpath('td[@class="points-cell"]/a')[0]
            points = int(points_cell.text.replace(",", ""))
            link = points_cell.get("href")
            current_rankings.append([name, points, link])

        last_monday -= timedelta(days=7)

    return current_rankings


def subtract_tournament(current_rankings,
                        current_tournament,
                        root_url="http://www.atpworldtour.com"):
    """
    Takes the current rankings and for each player subtracts the amount they
    got from the current_tournament

    Args:
        current_rankings (list): Rankings list of elements of the form
            [player (str), points (int), link_to_detailed_rankings (str)]
        current_tournament (str): Name of the current tournament
        root_url (str): The base url to use

    Returns:
        list: Where each element is [player, score]
    """
    final_rankings = []

    for player in tqdm(current_rankings):
        score = player[1]
        url = root_url + player[2]
        page = requests.get(url)
        tree = html.fromstring(page.content)
        tournaments = tree.xpath('//div[@id="playerRankBreakdownContainer"]')
        if tournaments:
            for tourn_class in tournaments[0].xpath('h2'):
                if "Non-Countable Tournaments" not in tourn_class.text:
                    tourn_table = tourn_class.getnext()
                    rows = tourn_table.xpath('tbody/tr')
                    for row in rows:
                        name = row.xpath('td/a/text()')
                        if name:
                            name = name[0]
                            if current_tournament in name:
                                points = int(row[3]
                                             .text
                                             .strip()
                                             .replace(",", ""))
                                score = score - points
        final_rankings.append([player[0], score])

    return final_rankings
