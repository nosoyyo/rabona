import os
import logging

from .base import RabonaModel


# init
logging.basicConfig(
    filename='log/match.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaMatch(RabonaModel):
    '''

    :param data: `obj` ri.A_parsed, a RabonaParserA object
    :param user: `obj` a RabonaUser object.
    '''
    col = 'matches'

    def __init__(self, user, oid=None, data=None):
        self.user = user
        self.user_oid = user.ObjectId
        if not oid and not data:
            self.save()
        elif str(oid).isdigit():
            self.__dict__ = self.load(oid)
            logging.info('RabonaMatch object #{} set up.'.format(self.id))

        if data:
            self.home = data.home
            self.away = data.away
            self.match_result = data.match_result
            self.match_score = data.match_score
            self.motm = ''
            self.motm_rating = ''
            self.facts = ''

    @classmethod
    def getLastMatch(self, user):
        '''
        :param user: `obj` RabonaUser object
        '''
        match_dir = user.dir + 'matches/'
        oid = len(os.listdir(match_dir))
        return RabonaMatch(oid=oid, user=user)
