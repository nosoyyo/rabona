import arrow
import logging

from .base import RabonaModel


# init
logging.basicConfig(
    filename='log/user.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaUser(RabonaModel):
    '''
    for now, an RabonaUser is just a Telegram user.
    in future, RabonaUser will mostly deal with runtime stuff.

    :param tele_user: `obj` telegram effective_user object
    :attr tele_id: `str` user's telegram id
    '''

    def __init__(self, tele_user=None):
        self.m = super(RabonaUser, self).m
        self.col = 'users'

        if tele_user:
            self.tele_user = tele_user
            self.tele_id = self.tele_user.id

        self.is_new = self._is_new()
        self.aloha()

    def _is_new(self):
        query = {'tele_id': self.tele_id}
        result = bool(self.m.ls(query, 'users')) or False
        print(result)
        return result

    def aloha(self):

        if self.is_new:
            self.tele_id = self.tele_user.id
            self.first_name = self.tele_user.first_name
            if self.tele_user.last_name:
                self.last_name = self.tele_user.last_name
            if self.tele_user.username:
                self.username = self.tele_user.username
            self.save()
            logging.info('aloha! new user {}'.format(self.tele_id))
            return True
        else:
            self.__dict__ = self.load()
            logging.info('aloha! user {} seen again.'.format(self.tele_id))
            return False

    def load(self):
        __dict__ = self.m.ls({'tele_id': self.tele_id}, 'users')[0]
        if 'ObjectId' not in self.__dict__.keys():
            self.ObjectId = __dict__['_id']
        return __dict__

    def savePhoto(self, bot, photo_file):
        filename = self.dir + \
            arrow.now().__str__().split('.')[0].replace(
                '/', '-').replace(':', '') + '.jpeg'
        photo_file.download(filename)
        logging.info('user {} uploaded a photo {}.'.format(
            self.tele_id, filename))
        return filename
