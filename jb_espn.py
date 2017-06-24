import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
from datetime import date, timedelta, datetime

#Get the abbreviation of the team that won jumpball
def get_first_team(game_id):
    #Make a request to the playbyplay page
    r = requests.get('http://www.espn.com/nba/playbyplay?gameId={}'.format(game_id))

    #Initialize BeautifulSoup
    soup = BeautifulSoup(r.content, 'lxml')

    #Get the 2nd image
    img = soup.find(id = 'gp-quarter-1').find_all('img', limit = 2)[1]

    #Splice the img src to get team abbreviation
    #ex. 'http://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/bos.png&h=100&w=100'
    #len('http://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/') = 57
    #len('.png&h=100&w=100') = 16
    return img['src'][57:-16]

#Get the abbreviation of the winning team
def get_winner(event):
    #Get the two competitors of the event
    competitors_dict = event.get('competitions')[0].get('competitors')

    if competitors_dict[0].get('winner') == True:
        return competitors_dict[0].get('team').get('abbreviation').lower()
    else:
        return competitors_dict[1].get('team').get('abbreviation').lower()

def main():
    #Initialize datetime objects
    one_day = timedelta(days = 1)
    curr_day = date(2016, 10, 25)
    last_day = date(2017, 4, 12)

    #Initialize variables holding our final data
    #1. total games calculated
    #2. total wins for teams that win the jumpball
    total_games = 0
    wins = 0

    #Start timer to calculate time for function to complete
    startTime = datetime.now()

    while curr_day <= last_day:
        #Make request on curr_day's scoreboard page
        r = requests.get('http://www.espn.com/nba/scoreboard/_/date/{y}{m}{d}'.format(y = curr_day.year, m = curr_day.strftime('%m'), d = curr_day.strftime('%d')))

        #Initialize BeautifulSoup
        soup = BeautifulSoup(r.content, 'lxml')

        #Get the content of the script with JSON data
        #When looking at HTML, the json script is 2nd sibling
        #of the one w/ special src but for some reason it's
        #the 3rd sibling when scraping
        content = soup.find('script', attrs={'src' : 'http://cdn.optimizely.com/js/310987714.js'}).next_sibling.next_sibling.next_sibling.contents[0]

        #Remove the variable name and useless things at the end
        #of the content
        #len('window.espn.scoreboardData 	= {') = 30
        #len of useless things at the end = 281
        json_data = content[30:-281]

        #Decode the json into a dictionary and get the events
        main_dict = json.loads(json_data)
        events_dict = main_dict.get('events')

        total_games += len(events_dict)
        print(curr_day)

        for event in events_dict:
            #Skip instances where a game wasn't played
            if not event.get('status').get('type').get('completed'):
                total_games -= 1
                continue;

            first_team = get_first_team(event.get('id'))
            winner = get_winner(event)

            if first_team == winner:
                wins += 1

        curr_day += one_day

    print('')
    print('Total games calculated: {}.'.format(total_games))
    print('Teams that win the jumpball were {} - {}.'.format(wins, total_games-wins))
    print('A winning % of: {:.5%}.'.format(wins/total_games))

    print(datetime.now() - startTime)

if __name__ == '__main__':
    main()
