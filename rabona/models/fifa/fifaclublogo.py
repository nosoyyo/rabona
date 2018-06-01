from bson.objectid import ObjectId

from .base import FIFAModel


class FIFAClubLogo(FIFAModel):
    '''
    '''
    col = 'FIFA_club_logos'

    def __init__(self, oid: ObjectId=None, data: dict=None):
        if data:
            self.__dict__ = data
            self.save()
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)