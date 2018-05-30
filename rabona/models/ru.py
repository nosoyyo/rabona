import uuid
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
    :attr tele_id: `int` user's telegram id
    '''

    col = 'users'

    def __init__(self, tele_user=None):
        self.m = super(RabonaUser, self).m

        if tele_user:
            self.tele_user = tele_user
            self.tele_id = self.tele_user.id
            self.appellation = self.tele_user.full_name

        self.aloha()

    def aloha(self):
        query = {'tele_id': self.tele_id}
        is_new = not bool(self.m.ls(query, 'users'))
        print('is new: {}'.format(is_new))

        if is_new is True:
            self.tele_id = self.tele_user.id
            self.first_name = self.tele_user.first_name
            if self.tele_user.last_name:
                self.last_name = self.tele_user.last_name
            if self.tele_user.username:
                self.username = self.tele_user.username

            self.save(self.tele_id)
            logging.info('aloha! new user {}'.format(self.tele_id))
        else:
            retrieval = self.load(self.tele_id)
            self.__dict__ = retrieval
            self.ObjectId = retrieval['_id']
            logging.info('aloha! user {} seen again.'.format(self.tele_id))

    def savePhoto(self, bot, photo_file):
        filename = 'var/tmp/'+uuid.uuid4().__str__()+'.jpeg'
        photo_file.download(filename)
        logging.info('user {} uploaded a photo {}.'.format(
            self.tele_id, filename))
        return filename
