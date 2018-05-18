import os
import arrow
import logging


# init
logging.basicConfig(
    filename='log/user.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def loadUID():
    with open('uid', 'r') as u:
        return u.read().split(' ')


uid = loadUID()
logging.info('{} users loaded.'.format(len(uid)))


class RabonaUser():
    '''
    for now, an RabonaUser is just a Telegram user.

    :param tele_user: `obj` telegram effective_user object
    :attr tele_id: `str` user's telegram id
    '''

    def __init__(self, tele_user):
        u = tele_user
        self.tele_id = str(u.id)
        self.dir = 'data/users/' + self.tele_id + '/'
        if 'username' in u.__dict__.keys():
            self.tele_username = u.username
        self.tele_lang = u.language_code
        self.first_name = u.first_name
        self.last_name = u.last_name
        if self.last_name:
            self.title = self.last_name + '师'
        else:
            self.title = self.first_name + '师'
        self.is_new = self.aloha()

    def aloha(self):
        global uid
        if self.tele_id not in uid:
            with open('uid', 'a') as u:
                u.write(self.tele_id + ' ')
            uid = loadUID()
            os.makedirs('data/users/' + self.tele_id)
            os.makedirs(self.dir + 'matches')
            logging.info('aloha! new user {}'.format(self.tele_id))
            return True
        else:
            logging.info('aloha! user {} seen again.'.format(self.tele_id))
            return False

    def savePhoto(self, bot, photo_file):
        filename = self.dir + \
            arrow.now().__str__().split('.')[0].replace(
                '/', '-').replace(':', '') + '.jpeg'
        photo_file.download(filename)
        logging.info('user {} uploaded a photo {}.'.format(
            self.tele_id, filename))
        return filename
