import logging
from bson.objectid import ObjectId

from .base import RabonaModel

# init
logging.basicConfig(
    filename='log/comp.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaCompetition(RabonaModel):
    '''
    Competition data model.

    :field 'mode': `str` one of ['cup', 'league', 'mix'].
    :field 'teams': `int` number of participants.
    :field :
    '''
    col = 'competitions'

    def __init__(self, user, oid: ObjectId=None, data: object=None):
        self.user = user
        self.user_oid = user.ObjectId

        if not oid and not data:
            self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
            logging.info('RabonaMatch object #{} set up.'.format(self.id))

        if data:
            self.n_participants = ''
            self.mode = ''
            self.save()
