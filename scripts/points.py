"""
Breakdown of how much each round at each type of tournament is worth.

@author: Alex Kaiser (edited Feb 20th, 2017)
"""
import requests
import lxml.html
import re

def points(current_tournament, root_url='http://www.atpworldtour.com'):
    """
    Get the amount of points for each round for a current tournament
    
    Args:
        current_tournament (str): The city of the current tournament
        root_url (str): The base url to use

    Returns:
        points_list (list of ints): List of ints with value of points for each
            round.  Largest points at the end
    """
    page = requests.get(root_url + '/en/tournaments')
    tree = lxml.html.fromstring(page.content)
    all_tournaments = tree.xpath('//li[@class=" has-link no-padding"]/a')
    for tournament in all_tournaments:
        if current_tournament in tournament.text:
            tournament_id = re.search("(\d+)/overview", tournament.get("href")).group(1)
            url = root_url + "/en/content/ajax/tournament/points-and-prize-money?tournamentId=" + tournament_id
            break
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    main_table = tree.xpath('//div[@class="points-and-prize-money-table"]/table/tbody')[0]
    points_list = []
    for row in main_table:
        columns = list(row)
        point_total = int(columns[2].text.strip().replace(",", ""))
        if columns[1].text.strip() == "Qualifier":
            break
        elif point_total == 0:
            points_list.append(0)
            break
        else:
            points_list.append(point_total)
    points_list.reverse()
    return points_list


if __name__ == '__main__':
    print(points("Rio de Janeiro"))