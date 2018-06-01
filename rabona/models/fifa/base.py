__name__ = 'Core ODM <=> MongoDB, first use on Rabona.'
__author__ = 'nosoyyo'
__version__ = {'0.1': '2018.05.03',
               '0.2': '2018.6.1',
               }

import pickle
import logging
from bson.objectid import ObjectId

from utils.pipeline import MongoDBPipeline


# init
logging.basicConfig(
    filename='var/log/fifamodel.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class FIFAModel():
    m = MongoDBPipeline()
    col = ''
    field_types = [bool, str, int, list, tuple, set, dict, bytes, ObjectId]
    __FIFAObjects = ['FIFAPlayer', 'FIFAClub', 'FIFALeague']
    __RabonaObjects = ['RabonaUser', 'RabonaMatch', 'RabonaModel',
                       'RabonaCompetition', 'RabonaPerson', 'RabonaPlayer']
    __special_objects = ['active_menu', ]

    def __init__(self, doc: dict=None, **kwargs):
        if not doc:
            _dict = kwargs
        elif doc:
            if isinstance(doc, dict):
                _dict = doc
            elif isinstance(doc, object):
                _dict = doc.__dict__
        ks, vs = [k for k in _dict.keys()], [v for v in _dict.values()]
        for i in range(len(_dict)):
            self.__setattr__(ks[i], vs[i])

    def save(self, oid: ObjectId=None, col: str=None) -> bool:
        '''
        scene 0: init saving for new obj
        scene 1: update for existed obj

        :param oid: `obj` bson.objectid.ObjecdId object

        :param col: `str` to set MongoDB.db.collection, fallback on 'testcol'
        '''

        if not col:
            if self.col:
                col = self.col
            else:
                col = self.m.col

        doc = dict([list(item) for item in self.__dict__.items()])

        pickle_objs = {}

        # pickling
        for k, v in doc.items():
            if v.__repr__() in self.__RabonaObjects:
                pickle_objs[k] = pickle.dumps(doc[k])
            elif v.__repr__() in self.__FIFAObjects:
                pickle_objs[k] = {doc[k].ObjecdId: doc[k].col}
            elif k in self.__special_objects:
                pickle_objs[k] = pickle.dumps(doc[k])
        for k, v in pickle_objs.items():
            doc[k] = v

        if 'ObjectId' in self.__dict__.keys() or oid:
            if 'ObjectId' in self.__dict__.keys():
                oid = self.ObjectId
            elif oid:
                oid = oid
            result = self.m.update(oid, doc, col)

            logging.debug('doc {} updated in {}'.format(doc, col))
            return result
        else:
            logging.debug('input doc is: {}'.format(doc))
            if 'ObjectId' not in doc.keys() and doc != self.m.ls(doc, col):
                result = self.m.insert(doc, col) or False
                logging.debug('get result: {}'.format(result))
                if isinstance(result, ObjectId):
                    self.ObjectId = result
                    logging.debug('doc {} inserted in {}'.format(doc, col))
                return bool(result)
            else:
                return False

    def load(self, some_id=None, col: str=None) -> dict:
        '''

        :param some_id: `None` not quite sure what'll be input yet
        '''

        if not col:
            if self.col:
                col = self.col
            else:
                col = self.m.col

        try:
            if not some_id:
                if 'ObjectId' not in self.__dict__.keys():
                    raise AttributeError
                else:
                    query_key = '_id'
                    query_value = self.ObjectId
            elif isinstance(some_id, ObjectId):
                query_key = '_id'
                query_value = some_id
            elif str(some_id).isdigit():
                query_key = 'tele_id'
                query_value = some_id

            logging.debug('querying key: "{}" & value: "{}"'.format(
                query_key, query_value))
            retrieval = self.m.ls({query_key: query_value}, col)

            if isinstance(retrieval, list):
                __dict__ = retrieval[0]
            else:
                __dict__ = retrieval

            if 'ObjectId' not in self.__dict__.keys():
                if isinstance(__dict__['_id'], ObjectId):
                    self.ObjectId = __dict__['_id']

            # unpickling
            for key in list(__dict__):
                if key in self.__FIFAObjects:
                    # {doc[k].ObjecdId: doc[k].col}
                    __dict__[key] = self.m.ls(list(__dict__)[0], __dict__[key])
                elif key in self.__RabonaObjects:
                    # pickle_objs[k] = pickle.dumps(doc[k])
                    __dict__[key] = pickle.loads(__dict__[key])
                elif key in self.__special_objects:
                    # pickle_objs[k] = pickle.dumps(doc[k])
                    __dict__[key] = pickle.loads(__dict__[key])

            return __dict__

        except AttributeError:
            print('Object without any id cannot be loaded.')
