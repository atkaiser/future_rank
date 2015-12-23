"""
Gets the draw for the current tournament
"""

import requests
from lxml import html

current_tournament = "Australian Open"
root_url = 'http://www.atpworldtour.com'
page = requests.get(root_url + '/en/scores/current/')
tree = html.fromstring(page.content)

all_tournaments = tree.xpath('//ul[@id="archiveTournamentDropdown"]')[0]

tournament_url = ""

for tournament in all_tournaments:
    if current_tournament in tournament.text:
        value = tournament.get("data-value")
        descriptor = tournament.get("data-descriptor")
        tournament_url = root_url + \
            "/en/scores/archive/" + \
            descriptor + \
            "/" + value + \
            "/2015/draws"

page = requests.get(tournament_url)
tree = html.fromstring(page.content)

matches = []

for match in tree.xpath('//table[@class="scores-draw-entry-box-table"]'):
    players = match.xpath('tbody/tr/td/a')
    for player in players:
        matches.append(player.get("data-ga-label"))
    if len(players) == 1:
        matches.append("Bye")
