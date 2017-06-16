import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date, timedelta, datetime

#get the team with posession after tip
def get_first_team(game_id):
    r = requests.get('http://www.espn.com/nba/playbyplay?gameId={}'.format(game_id))
    soup = BeautifulSoup(r.content, 'lxml')

    #due to ESPN the first img isn't always the team w/ possession after tip so therefore the 2nd img will do
    img = soup.find(id = 'gp-quarter-1')
    if img == None:
        return None
    else:
        img = img.find_all('img', limit = 2)[1]
        return img['src'][57:-16]

#find the winner of game given ESPN's "game" values
def get_winner(game):
    game_dict = game.get('competitions')[0]
    competitors_dict = game_dict.get('competitors')

    if competitors_dict[0].get('winner') == True:
        return competitors_dict[0].get('team').get('logo')[52:-4]
    else:
        return competitors_dict[1].get('team').get('logo')[52:-4]

def main():
    one_day = timedelta(days = 1)
    opening_day = date(2016, 11, 30)
    last_day = date(2016, 11, 30)

    total_games = 0
    wins = 0

    startTime = datetime.now()

    while opening_day <= last_day:
        r = requests.get('http://www.espn.com/nba/scoreboard/_/date/{y}{m}{d}'.format(y = opening_day.year, m = opening_day.strftime('%m'), d = opening_day.strftime('%d')))
        soup = BeautifulSoup(r.content, 'lxml')
        content = soup.find('script', attrs={'src' : 'http://cdn.optimizely.com/js/310987714.js'}).next_sibling.next_sibling.next_sibling.contents[0]
        json_data = content[30:-281]
        main_dict = json.loads(json_data)
        games_dict = main_dict.get('events')

        total_games += len(games_dict)
        print(opening_day)

        for game in games_dict:
            first_team = get_first_team(game.get('id'))
            if first_team == None:
                continue;

            winner = get_winner(game)

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
