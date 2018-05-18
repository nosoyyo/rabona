import logging
from fuzzywuzzy import process

# init
logging.basicConfig(
    filename='log/parser.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


with open('data/leagues/all_clubs', 'r') as f:
    all_clubs = f.readlines()
all_clubs = [club.replace('\n', '') for club in all_clubs]
logging.info('{} club names loaded.'.format(len(all_clubs)))


class RabonaParserA():
    '''

    '''

    def __init__(self, j):
        print(j)
        raw = j['ParsedResults'][0]['ParsedText'].replace(
            '\r', '').replace('\n', '').split('-')
        logging.info('accept input json {}'.format(raw))

        self.home = process.extractOne(raw[0], all_clubs)[0]
        logging.info('retrieved home name {}'.format(self.home))

        self.away = process.extractOne(raw[1], all_clubs)[0]
        logging.info('retrieved away name {}'.format(self.away))

        self.home_score = raw[0].strip().split(' ')[-1]
        logging.info('retrieved home score {}'.format(self.home_score))

        self.away_score = raw[1].strip().split(' ')[0]
        logging.info('retrieved away score {}'.format(self.away_score))

        self.match_score = self.home_score + ' : ' + self.away_score

        self.match_result = '{} {} {}'.format(
            self.home, self.match_result, self.away)
        logging.info('match result: {}'.format(self.match_result))
