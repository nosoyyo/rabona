import os
import pickle
import logging

# init
logging.basicConfig(
    filename='log/match.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaMatch():
    '''

    :param data: `obj` ri.A_parsed, a RabonaParserA object
    :param user: `obj` a RabonaUser object.
    '''

    def __init__(self, _id='', user=None, data=None):
        self.dir = user.dir + 'matches/'
        if not _id:
            self.id = len(os.listdir(self.dir)) + 1
            self.id_str = str(self.id)
        elif str(_id).isdigit():
            self.id = int(_id)
            self.id_str = str(_id)
            with open(self.dir + self.id_str, 'r') as f:
                m = pickle.load(f)
            self.__dict__ = m.__dict__
            logging.info('RabonaMatch object #{} set up.'.format(self.id))

        if data:
            self.home = data.home
            self.away = data.away
            self.match_result = data.match_result
            self.match_score = data.match_score
            self.motm = ''
            self.motm_rating = ''
            self.facts = ''

    def persistize(self):
        with open(self.dir + self.id_str, 'wb') as f:
            pickle.dump(self, f)
        logging.info('RabonaMatch object #{} pesistized'.format(self.id))

    @classmethod
    def getLastMatch(self, user):
        '''
        :param user: `obj` RabonaUser object
        '''
        match_dir = user.dir + 'matches/'
        _id = len(os.listdir(match_dir))
        return RabonaMatch(_id=_id, user=user)
