import copy
import logging
from bson.objectid import ObjectId

from utils.pipeline import MongoDBPipeline


# init
logging.basicConfig(
    filename='log/base.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaModel():
    m = MongoDBPipeline()
    col = ''
    field_types = [bool, str, int, list, tuple, set, dict, bytes, ObjectId]

    def __init__(self, doc=None, **kwargs):
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

    def save(self, oid=None, col=None):
        '''
        scene 0: init saving for new obj
        scene 1: update for existed obj

        :param oid: 'obj' bson.objectid.ObjecdId object.
        '''

        if not col:
            if self.col:
                col = self.col
            else:
                col = self.m.col

        doc_original = [list(item) for item in self.__dict__.items()]
        doc = dict(copy.deepcopy(doc_original))
        for key in list(doc):
            if type(doc[key]) not in self.field_types:
                doc.pop(key)

        if 'ObjectId' in self.__dict__.keys() or oid:
            if 'ObjectId' in self.__dict__.keys():
                oid = self.ObjectId
            elif oid:
                oid = oid
            result = self.m.update(oid, doc, col)
            logging.info('doc {} updated in {}'.format(doc, col))
            return result
        else:
            if 'ObjectId' not in doc.keys() and doc != self.m.ls(doc):
                self.ObjectId = self.m.insert(doc, col)
                logging.info('doc {} inserted in {}'.format(doc, col))

    def load(self, some_id=None):
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

            logging.info('querying key: {}, value: {}'.format(
                query_key, query_value))
            retrieval = self.m.ls({query_key: query_value}, self.col)

            if isinstance(retrieval, list):
                __dict__ = retrieval[0]
            else:
                __dict__ = retrieval

            if 'ObjectId' not in self.__dict__.keys():
                self.ObjectId = __dict__['_id']
            return __dict__

        except AttributeError:
            print('Object without any id cannot be loaded.')
