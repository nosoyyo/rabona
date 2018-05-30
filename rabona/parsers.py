import logging
from bson.objectid import ObjectId
from fuzzywuzzy import process

from utils.pipeline import MongoDBPipeline
from errors import UnrecognizableTextError

# init
logging.basicConfig(
    filename='log/parser.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] \
    %(levelname)s %(message)s')

'''
with open('data/leagues/all_clubs', 'r') as f:
    all_clubs = f.readlines()
all_clubs = [club.replace('\n', '') for club in all_clubs]
'''


class RabonaParserA():
    '''

    '''

    def __init__(self, _input):
        self._raw = _input
        oid = ObjectId('5b04fae13c755aa7ea90d98e')
        m = MongoDBPipeline()
        self.all_clubs = [v for v in m.ls(oid, 'all_clubs').values()]
        logging.info('{} club names loaded.'.format(len(self.all_clubs)))

        # parsing ocr.space results
        if isinstance(_input, dict):
            self.divided = _input['ParsedResults'][0]['ParsedText'].replace(
                '\r', '').replace('\n', '').split('-')
            logging.info('accept input json {}'.format(self.divided))
        # parsing face-recognize & pytesseract results
        elif isinstance(_input, str):
            if _input.count('-') == 1:
                self.divided = _input.replace(
                    '\r', '').replace('\n', '').split('-')
                logging.info('accept input string {}'.format(self.divided))
            else:
                raise UnrecognizableTextError(self.divided)

        self.home = process.extractOne(self.divided[0], self.all_clubs)[0]
        logging.info('retrieved home name {}'.format(self.home))

        self.away = process.extractOne(self.divided[1], self.all_clubs)[0]
        logging.info('retrieved away name {}'.format(self.away))

        home_score = self.divided[0].strip().split(' ')[-1]
        if home_score.isdigit():
            self.home_score = home_score
        logging.info('retrieved home score {}'.format(self.home_score))

        away_score = self.divided[1].strip().split(' ')[0]
        if away_score.isdigit():
            self.away_score = away_score
        else:
            # case0 'src/test.jpg'
            faker = away_score
            tryer = self.divided[1].replace(faker, '').strip()[0]
            if tryer.isdigit():
                self.away_score = tryer
        logging.info('retrieved away score {}'.format(self.away_score))

        self.match_score = self.home_score + ' : ' + self.away_score

        self.match_result = '{} {} {}'.format(
            self.home, self.match_score, self.away)
        logging.info('match result: {}'.format(self.match_result))


class RabonaParserE():
    '''

    '''

    def __init__(self, _input):
        self._raw = _input
        oid = ObjectId('5b04fae13c755aa7ea90d98e')
        m = MongoDBPipeline()
        self.all_clubs = [v for v in m.ls(oid, 'all_clubs').values()]
        logging.info('{} club names loaded.'.format(len(self.all_clubs)))

        # parsing ocr.space results
        if isinstance(_input, dict):
            self.divided = _input['ParsedResults'][0]['ParsedText'].replace(
                '\r', '').replace('\n', '').split('-')
            logging.info('accept input json {}'.format(self.divided))
        # parsing face-recognize & pytesseract results
        elif isinstance(_input, str):
            if _input.count('-') == 1:
                self.divided = _input.replace(
                    '\r', '').replace('\n', '').split('-')
                logging.info('accept input string {}'.format(self.divided))
            else:
                raise UnrecognizableTextError(self.divided)

        self.home = process.extractOne(self.divided[0], self.all_clubs)[0]
        logging.info('retrieved home name {}'.format(self.home))

        self.away = process.extractOne(self.divided[1], self.all_clubs)[0]
        logging.info('retrieved away name {}'.format(self.away))

        home_score = self.divided[0].strip().split(' ')[-1]
        if home_score.isdigit():
            self.home_score = home_score
        logging.info('retrieved home score {}'.format(self.home_score))

        away_score = self.divided[1].strip().split(' ')[0]
        if away_score.isdigit():
            self.away_score = away_score
        else:
            # case0 'src/test.jpg'
            faker = away_score
            tryer = self.divided[1].replace(faker, '').strip()[0]
            if tryer.isdigit():
                self.away_score = tryer
        logging.info('retrieved away score {}'.format(self.away_score))

        self.match_score = self.home_score + ' : ' + self.away_score

        self.match_result = '{} {} {}'.format(
            self.home, self.match_score, self.away)
        logging.info('match result: {}'.format(self.match_result))
