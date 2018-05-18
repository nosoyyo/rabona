import os
import pickle


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
        elif _id.isdigit():
            self.id = int(_id)
            self.id_str = str(_id)

        if data:
            self.home = data.home
            self.away = data.away
            self.match_result = data.match_result
            self.match_score = data.match_score
            self.motm = ''
            self.motm_rating = ''
            self.facts = ''

    def persistize(self):
        with open(self.dir + self.id, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def getLastMatch(self, user):
        '''
        :param user: `obj` RabonaUser object
        '''
        _id = len(os.listdir(self.dir))
        return RabonaMatch(_id=_id)
