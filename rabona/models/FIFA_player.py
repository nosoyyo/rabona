from bson.objectid import ObjectId

from .base import RabonaModel


class FIFAPlayer(RabonaModel):
    '''
    '''
    col = 'FIFA_players'

    def __init__(self, oid: ObjectId=None, data: dict=None):
        if data:
            self.__dict__ = data
            self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
