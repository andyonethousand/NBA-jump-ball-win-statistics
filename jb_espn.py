import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date, timedelta, datetime

#get the player with posession after tip
def get_first_player(pbp_url):
    r = requests.get('http://www.basketball-reference.com{}'.format(pbp_url))
    strainer = SoupStrainer(id = 'div_pbp')
    soup = BeautifulSoup(r.content, 'lxml', parse_only = strainer)
    first_player = soup.find_all('a', limit = 3)[2]
    return first_player['href']

#get the team with posession after tip
def get_team(player_url):
    r = requests.get('http://www.basketball-reference.com{}'.format(player_url))
    strainer = SoupStrainer('div', attrs={"itemtype" : "http://schema.org/Person"})
    soup = BeautifulSoup(r.content, 'lxml', parse_only = strainer)
    first_team = soup.find_all('a', limit = 3)[2]
    return first_team['href']


def main():
    one_day = timedelta(days = 1)
    opening_day = date(2016, 10, 25)
    last_day = date(2017, 4, 12)

    total_games = 0
    jb_winners = 0

    startTime = datetime.now()

    r = requests.get('http://www.basketball-reference.com/boxscores/?month={m}&day={d}&year={y}'.format(m = opening_day.month, d = opening_day.day, y = opening_day.year))

    r = requests.get('http://www.espn.com/nba/scoreboard/_/date/20170507')
    soup = BeautifulSoup(r.content, 'lxml')
    content = soup.find('script', attrs={'src' : 'http://cdn.optimizely.com/js/310987714.js'}).next_sibling.next_sibling.next_sibling.contents[0]
    json_data = content[len('window.espn.scoreboardData 	= '):-len(';window.espn.scoreboardSettings = {"useStatic":false,"initialTopic":"scoreboard-basketball-nba","isCollege":false,"scoDate":"20170507","isWeekOriented":false,"league":"nba","useReplay":false,"sport":"basketball"};if(!window.espn_ui.device.isMobile){window.espn.loadType = "ready"};')]
    main_dict = json.loads(json_data)
    events_dict = main_dict.get('events')

    for game in events_dict:
        print(game.get('id'))

if __name__ == '__main__':
    main()
