from bson.objectid import ObjectId

from utils.pipeline import MongoDBPipeline


class RabonaModel():
    m = MongoDBPipeline()
    col = ''
    field_types = [str, int, list, tuple, set, dict, ObjectId, ]

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
        if not col:
            col = self.col

        doc = dict([item for item in self.__dict__.items()])
        for key in doc.keys():
            if type(doc[key]) not in self.field_types:
                doc.pop(key)

        if oid:
            self.m.update(oid, doc, col)
        else:
            if 'ObjectId' not in self.__dict__.keys():
                self.ObjectId = self.m.insert(doc, col)

        # verify
        __dict__ = self.load()
        __dict__.pop('_id')
        if __dict__ == doc:
            return True
        else:
            return False

    def load(self):
        __dict__ = self.m.ls({'_id': self.ObjectId}, self.col)[0]
        if 'ObjectId' not in self.__dict__.keys():
            self.ObjectId = __dict__['_id']
        return __dict__
