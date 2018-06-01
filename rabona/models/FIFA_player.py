from bson.objectid import ObjectId

from .base import RabonaModel


class FIFAPlayer(RabonaModel):
    '''
    Full attributes of a FIFA player.
    Always create FIFAPlayer obj with `common_name`!

    :param oid: `obj` bson.objectid.ObjectId object
    :param data: `dict` some kv pairs like {'common_name':'Gabriel Jesus'}
    :param name: `str` anything close to the full or common name of the player
    '''
    col = 'FIFA_players'

    def __init__(self,
                 oid: ObjectId=None,
                 data: dict=None,
                 common_name: str=None):
        if data:
            try:
                probe = self.m.ls(
                    {'common_name': data['common_name']}, self.col)
                if len(probe) == 0:
                    self.__dict__ = data
                    self.save()
                elif len(probe) >= 1:
                    self.__dict__ = probe[0]
                    self.save()
            except Exception as e:
                print(e)
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
        elif common_name:
            try:
                self.__dict__ = self.m.ls(
                    {'common_name': common_name}, self.col)[0]
            except Exception as e:
                print(e)
