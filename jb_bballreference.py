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
    curr_day = date(2016, 10, 25)
    last_day = date(2016, 11, 12)

    total_games = 0
    wins = 0

    startTime = datetime.now()

    while curr_day <= last_day:
        r = requests.get('http://www.basketball-reference.com/boxscores/?month={m}&day={d}&year={y}'.format(m = curr_day.month, d = curr_day.day, y = curr_day.year))

        strainer = SoupStrainer('div', class_ = 'game_summary expanded nohover')
        soup = BeautifulSoup(r.content, 'lxml', parse_only = strainer)
        games = soup.contents[1:]

        total_games += len(games)
        print(curr_day)

        for game in games:
            pbp_url = game.find(class_ = 'links').find_all('a', limit = 2)[1]['href']

            first_team = get_team(get_first_player(pbp_url))
            winner = game.find(class_ = 'winner').find('a')['href']

            print(first_team + ' : ' + winner)

            if first_team == winner:
                wins += 1

        curr_day += one_day

    print('')
    print('Total games calculated: {}'.format(total_games))
    print('Teams that win the jumpball were {} - {}.'.format(wins, total_games-wins))
    print('A winning % of: {}'.format(wins/total_games))

    print(datetime.now() - startTime)

if __name__ == '__main__':
    main()
