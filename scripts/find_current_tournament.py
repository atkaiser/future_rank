'''
Finds the tournament with the most points that is currently running.

Created on Feb 20, 2017

@author: Alex Kaiser
'''
import requests
import lxml.html
from datetime import datetime
from points import points

def find_current_tournament(root_url='http://www.atpworldtour.com'):
    """
    Find the tournament with the most points that is currently running.
    
    Args:
        root_url (str): The base url to use

    Returns:
        str: The name of the city of the currently running tournament
    """
    page = requests.get(root_url + '/en/tournaments')
    tree = lxml.html.fromstring(page.content)
    all_tournaments = tree.xpath('//tr[@class="tourney-result"]')
    tournament_hash = get_tournament_url_to_city_hash(root_url)
    possible_tournaments = []
    for tournament in all_tournaments:
        for child in tournament:
            if child.get("class") =="title-content":
                elems = list(child)
                tournament_link = elems[0].get("href")
                tournament_dates = elems[2].text
                tournament_dates = tournament_dates.split("-")
                start, end = [datetime.strptime(x.strip(), "%Y.%m.%d") for x in tournament_dates]
                current_tournament = start <= datetime.today() <= end
                if current_tournament:
                    possible_tournaments.append(tournament_hash[tournament_link])
    return sorted(possible_tournaments, key=lambda x: -(points(x)[0]))[0]


def get_tournament_url_to_city_hash(root_url):
    tournament_hash = {}
    page = requests.get(root_url + '/en/tournaments')
    tree = lxml.html.fromstring(page.content)
    all_tournaments = tree.xpath('//li[@class=" has-link no-padding"]/a')
    for tournament in all_tournaments:
        tournament_name = tournament.text.strip()
        tournament_url = tournament.get("href")
        tournament_hash[tournament_url] = tournament_name

    return tournament_hash


if __name__ == '__main__':
    print(find_current_tournament())
#     print(get_tournament_hash("http://www.atpworldtour.com"))