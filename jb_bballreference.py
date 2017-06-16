import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date, timedelta, datetime

#get the player with posession after tip
def get_first_player(pbp_url):
    r = requests.get('http://www.basketball-reference.com{}'.format(pbp_url))
    strainer = SoupStrainer(id = 'div_pbp')
    soup = BeautifulSoup(r.content, 'lxml', parse_only = strainer)
    first_player = soup.find_all('a', limit = 3)[2]
    return first_player['href']

#get a player's team
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
    wins = 0

    startTime = datetime.now()

    while opening_day <= last_day:
        r = requests.get('http://www.basketball-reference.com/boxscores/?month={m}&day={d}&year={y}'.format(m = opening_day.month, d = opening_day.day, y = opening_day.year))

        strainer = SoupStrainer('div', class_ = 'game_summary expanded nohover')
        soup = BeautifulSoup(r.content, 'lxml', parse_only = strainer)
        games = soup.contents[1:]

        total_games += len(games)
        print(opening_day)

        for game in games:
            pbp_url = game.find(class_ = 'links').find_all('a', limit = 2)[1]['href']

            first_team = get_team(get_first_player(pbp_url))
            winner = game.find(class_ = 'winner').find('a')['href']

            if first_team == winner:
                wins += 1

        opening_day += one_day

    print('')
    print('Total games calculated: {}'.format(total_games))
    print('Teams that win the jumpball were {} - {}.'.format(wins, total_games-wins))
    print('A winning % of: {}'.format(wins/total_games))

    print(datetime.now() - startTime)

if __name__ == '__main__':
    main()
