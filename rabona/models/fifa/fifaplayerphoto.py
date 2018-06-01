from bson.objectid import ObjectId

from .rabona import RabonaModel


class FIFAPlayerPhoto(RabonaModel):
    '''
    '''
    col = 'FIFA_player_photos'

    def __init__(self, oid: ObjectId=None, data: dict=None):
        if data:
            self.__dict__ = data
            self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
