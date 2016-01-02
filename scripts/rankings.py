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
    last_monday = date.today()
    while last_monday.weekday() != 0:
        last_monday -= timedelta(days=1)
    page = requests.get(root_url +
                        '/en/rankings/singles?rankDate=' +
                        str(last_monday) +
                        '&rankRange=1-' +
                        str(num_rankings))
    tree = html.fromstring(page.content)

    all_players = tree.xpath('//table[@class="mega-table"]/tbody')[0]

    current_rankings = []

    for player_row in tqdm(all_players):
        name = player_row.xpath('td[@class="player-cell"]/a/text()')[0]
        points_cell = player_row.xpath('td[@class="points-cell"]/a')[0]
        points = int(points_cell.text.replace(",", ""))
        link = points_cell.get("href")
        current_rankings.append([name, points, link])

    return current_rankings


def subtract_tournament(current_rankings,
                        current_tournament,
                        root_url="http://www.atpworldtour.com"):
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
