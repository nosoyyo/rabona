import os
import time
import logging
from bson.objectid import ObjectId

from .base import RabonaModel
from errors import User310Error


# init
logging.basicConfig(
    filename='log/match.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaMatch(RabonaModel):
    '''

    :method load(oid): load a RabonaMatch obj from ObjectId.
    :method save(): save a RabonaMatch obj into MongoDB.
    :param data: `obj` ri, a RabonaImage object expected with
                       RabonaParserA & RabonaParserE objects.

    :param ru: `obj` a RabonaUser object.
    '''
    col = 'matches'

    def __init__(self, ru, oid: ObjectId=None, ri: object=None):
        self.user = ru
        self.user_oid = ru.ObjectId
        self.created = time.time()
        if not oid and not ri:
            self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
            logging.info('RabonaMatch object #{} set up.'.format(self.id))

        if ri:
            try:
                self.home = ri.A_parsed.home
                self.away = ri.A_parsed.away
                self.home_score = ri.A_parsed.home_score
                self.away_score = ri.A_parsed.away_score
                self.match_result = ri.A_parsed.match_result
                self.match_score = ri.A_parsed.match_score
                self.motm = ri.E_parsed
                self.user_is_home = ri.E_parsed.user_is_home
                self.user_310 = self.user310()
                self.state = ri.E_parsed.state
                self.motm_rating = ''
                self.facts = ''
                self.save()
            except KeyError as e:
                print(e)

    def user310(self):
        if self.home_score > self.away_score:
            if self.user_is_home:
                return 3
            else:
                return 0
        elif self.home_score < self.away_score:
            if self.user_is_home:
                return 0
            else:
                return 3
        elif self.home_score == self.away_score:
            return 1
        else:
            raise User310Error(self.home_score, self.away_score)

    @classmethod
    def getLastMatch(self, user):
        '''
        :param user: `obj` RabonaUser object
        '''
        match_dir = user.dir + 'matches/'
        oid = len(os.listdir(match_dir))
        return RabonaMatch(oid=oid, user=user)
