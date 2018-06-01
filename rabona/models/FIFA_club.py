from bson.objectid import ObjectId
from fuzzywuzzy import process

from .base import RabonaModel


class FIFAClub(RabonaModel):
    '''
    FIFAClub.players only store a list of player common_names.
    Note that the combination between clubs and players in this section
    might NOT be as concrete as you may expect.

    :param oid: `obj` bson.objectid.ObjectId object
    :param data: `dict` some kv pairs like {'club_name':'FC Hansa Rostock'}
    :param name: `str` anything close to the official name of the club
    '''
    col = 'FIFA_clubs'

    def __init__(self, oid: ObjectId=None, data: dict=None, name: str=None):
        if data:
            probe = self.m.ls({'club_name': data['club_name']}, 'FIFA_clubs')
            if len(probe) == 0:
                self.__dict__ = data
                self.save()
            elif len(probe) >= 1:
                self.__dict__ = probe[0]
                self.save()

        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
        elif name:
            club_name = process.extractOne(
                name, self.m.ls('all_clubs')[0].values())[0]
            try:
                self.__dict__ = self.m.ls(
                    {'club_name': club_name}, 'FIFA_clubs')[0]
            except Exception as e:
                print(e)
