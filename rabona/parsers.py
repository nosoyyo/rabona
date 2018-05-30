import logging
from fuzzywuzzy import process
from bson.objectid import ObjectId
from importlib import import_module

from data.leagues import club_league_dict
from utils.pipeline import MongoDBPipeline
from errors import UnrecognizableTextError

# init
logging.basicConfig(
    filename='log/parser.log',
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] \
    %(levelname)s %(message)s')


class RabonaParserA():
    '''

    '''

    def __init__(self, _input):
        self._raw = _input
        all_clubs_oid = ObjectId('5b04fae13c755aa7ea90d98e')
        m = MongoDBPipeline()
        all_clubs = [v for v in m.ls(all_clubs_oid, 'all_clubs').values()]
        logging.debug('{} club names loaded.'.format(len(all_clubs)))

        # parsing ocr.space results
        if isinstance(_input, dict):
            self.divided = _input['ParsedResults'][0]['ParsedText'].replace(
                '\r', '').replace('\n', '').split('-')
            logging.debug('accept input json {}'.format(self.divided))
        # parsing face-recognize & pytesseract results
        elif isinstance(_input, str):
            if _input.count('-') == 1:
                self.divided = _input.replace(
                    '\r', '').replace('\n', '').split('-')
                logging.debug('accept input string {}'.format(self.divided))
            else:
                raise UnrecognizableTextError(self.divided)

        self.home = process.extractOne(self.divided[0], all_clubs)[0]
        logging.debug('retrieved home name {}'.format(self.home))

        self.away = process.extractOne(self.divided[1], all_clubs)[0]
        logging.debug('retrieved away name {}'.format(self.away))

        home_score = self.divided[0].strip().split(' ')[-1]
        if home_score.isdigit():
            self.home_score = home_score
        logging.debug('retrieved home score {}'.format(self.home_score))

        away_score = self.divided[1].strip().split(' ')[0]
        if away_score.isdigit():
            self.away_score = away_score
        else:
            # case0 'src/test.jpg'
            faker = away_score
            tryer = self.divided[1].replace(faker, '').strip()[0]
            if tryer.isdigit():
                self.away_score = tryer
        logging.debug('retrieved away score {}'.format(self.away_score))

        self.match_score = self.home_score + ' : ' + self.away_score

        self.match_result = '{} {} {}'.format(
            self.home, self.match_score, self.away)
        logging.info('match result: {}'.format(self.match_result))


class RabonaParserE():
    '''
        Return an `int` as state code.

        :state `0`: OK, not any problem.
        :state `1`: vague, need user specification manually.
        :state `2`: bad, can't get anything meaningful out
        :state `3`: unknown ~~pleasures~~ error.
    '''

    def __init__(self, _input: str, rpa: RabonaParserA):
        if isinstance(_input, dict):
            self._raw = _input['ParsedResults'][0]['ParsedText']
        elif isinstance(_input, str):
            self._raw = _input

        home_club_name = rpa.home
        home_league = club_league_dict[home_club_name]
        home_club_module = import_module(
            'data.leagues.{0}.{1}.{1}'.format(home_league, home_club_name))
        home_players = home_club_module.players
        home_player_names = list(set(home_players))
        home_process = process.extractOne(self._raw, home_player_names)
        home_retrieval = home_process[0]
        home_weight = home_process[1]

        away_club_name = rpa.away
        away_league = club_league_dict[away_club_name]
        away_club_module = import_module(
            'data.leagues.{0}.{1}.{1}'.format(away_league, away_club_name))
        away_players = away_club_module.players
        away_player_names = list(set(away_players))
        away_process = process.extractOne(self._raw, away_player_names)
        away_retrieval = away_process[0]
        away_weight = away_process[1]

        # comparing
        if home_weight >= 90 and away_weight <= 51:
            self.motm = home_players[home_retrieval]
            self.user_is_home = True
            self.state = 0
        elif away_weight >= 90 and home_weight <= 51:
            self.motm = away_players[away_retrieval]
            self.user_is_home = False
            self.state = 0
        else:
            if home_weight >= 90:
                self.motm = home_retrieval
                self.user_is_home = True
                self.state = 1
            elif away_weight >= 90:
                self.motm = away_retrieval
                self.user_is_home = False
                self.state = 1
            else:
                self.state = 2
