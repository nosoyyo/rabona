import logging
from fuzzywuzzy import process
from bson.objectid import ObjectId

from .base import FIFAModel


# init
logging.basicConfig(
    filename='var/log/databuilder.log',
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')
logging.info('session started.')


class FIFALeague(FIFAModel):
    '''
    '''
    all_leagues = ['3. Liga', 'Alka Superliga', 'Allsvenskan',
                   'Belgium Pro League', 'Bundesliga', 'Bundesliga 2',
                   'Calcio A', 'Calcio B', 'Campeonato Scotiabank',
                   'Ceská Liga', 'Dawry Jameel', 'Domino’s Ligue 2',
                   'EFL Championship', 'EFL League One', 'EFL League Two',
                   'Ekstraklasa', 'Eliteserien', 'Eredivisie', 'Finnliiga',
                   'Hellas Liga', 'Hyundai A-League', 'Icons',
                   'K LEAGUE Classic', 'LaLiga 1 I 2 I 3', 'LaLiga Santander',
                   'LIGA Bancomer MX', 'Liga Dimayor', 'Liga Do Brasil',
                   'Liga NOS', 'Ligue 1 Conforama', 'Major League Soccer',
                   'Meiji Yasuda J1 League',
                   'Österreichische Fußball-Bundesliga', 'Premier League',
                   'Primera División', 'Raiffeisen Super League',
                   'Russian Football Premier League', 'Scottish Premiership',
                   'South African FL', 'SSE Airtricity League', 'Süper Lig',
                   'Ukrayina Liha',
                   ]
    col = 'FIFA_leagues'
    custom_ls_behaviour_col = [col]

    def __init__(self, oid: ObjectId=None, data: dict=None, name: str=None):
        if data:
            probe = self.m.ls({'league_name': data['league_name']}, self.col)
            if len(probe) == 0:
                self.__dict__ = data
                self.save()
            elif len(probe) >= 1:
                self.__dict__ = probe[0]
                self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
        elif name:
            league_name = process.extractOne(name, self.all_leagues)[0]
            try:
                self.__dict__ = self.m.ls(
                    {'league_name': league_name}, self.col)[0]
            except Exception as e:
                logging.error(
                    'name: {}, league_name: {}'.format(name, league_name))
                print('create league by name raises {}'.format(e))

    def custom_ls(self, arg: str=None, col=None):
        if isinstance(arg, str):
            print('FIFALeague custom_ls called!')
            query = process.extractOne(arg, self.all_leagues)[0]
            return self.m.ls({'league_name': query}, self.col)
