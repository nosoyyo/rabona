import logging
from fuzzywuzzy import process
from errors import UnknownRawTextError

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

    def __init__(self, _input):
        if isinstance(_input, dict):
            self.raw = _input['ParsedResults'][0]['ParsedText'].replace(
                '\r', '').replace('\n', '').split('-')
            logging.info('accept input json {}'.format(self.raw))
        elif isinstance(_input, str):
            if self.raw.count('-') == 1:
                self.raw = _input.replace('\r', '').replace('\n', '').split('-')
                logging.info('accept input string {}'.format(self.raw))
            else:
                raise UnknownRawTextError

        self.home = process.extractOne(self.raw[0], all_clubs)[0]
        logging.info('retrieved home name {}'.format(self.home))

        self.away = process.extractOne(self.raw[1], all_clubs)[0]
        logging.info('retrieved away name {}'.format(self.away))

        self.home_score = self.raw[0].strip().split(' ')[-1]
        logging.info('retrieved home score {}'.format(self.home_score))

        self.away_score = self.raw[1].strip().split(' ')[0]
        logging.info('retrieved away score {}'.format(self.away_score))

        self.match_score = self.home_score + ' : ' + self.away_score

        self.match_result = '{} {} {}'.format(
            self.home, self.match_score, self.away)
        logging.info('match result: {}'.format(self.match_result))
