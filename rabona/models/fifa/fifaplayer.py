import time
import logging
import requests
from functools import reduce
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

from .base import FIFAModel


# init
logging.basicConfig(
    filename='var/log/fifaplayer.log',
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')
logging.info('session started.')

sleep = 10
magic_number = '0x241c061a5b58abcf16'


def magic(s: str) -> str:
    return '0x{:x}'.format(
        int(str(ord('ʚ'))+reduce(lambda x,
                                 y: '{:0>3}'.format(x)+'{:0>3}'
                                 .format(y), map(ord, s))))


def readMagic(magic_number: str)->str:
    '''
    Not serious magic at all.
    Just to avoid literal material.
    '''
    tm = '{:d}'.format(int(eval(magic_number)))
    result = []
    for i in range(0, len(tm), 3):
        a, b = i, i+3
        result.append(int(tm[a:b]))
    return reduce(lambda x, y: x+y, map(chr, result))[1:]


site = 'https://www.{}.com/'.format(readMagic(magic_number))


class FIFAPlayer(FIFAModel):
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
            common_name = data['common_name']
            try:
                probe = self.probe(common_name)
                if len(probe) == 0:
                    self.__dict__ = data
                    self.save()
                elif len(probe) >= 1:
                    # TODO merge with data handed in here
                    self.__dict__ = probe[0]
                    self.save()
            except Exception as e:
                print(e)
        elif isinstance(oid, ObjectId):
            self.__dict__ = self.load(oid)
        elif common_name:
            try:
                probe = self.probe(common_name)
                if len(probe) == 0:
                    self.__dict__ = self.getPlayer(common_name).__dict__
                    self.save()
                elif len(probe) >= 1:
                    self.__dict__ = probe[0]
                    self.save()
            except Exception as e:
                print(e)

    def probe(self, common_name: str) -> dict:
        return self.m.ls({'common_name': common_name}, self.col)

    def getPlayer(self, common_name, ver='Normal', sleep=sleep):

        query = 'https://www.{}.com/18/players?search='.format(
            readMagic(magic_number)) + common_name
        r = requests.get(query)
        soup = BeautifulSoup(r.text, 'lxml')
        player_trs = soup.select('tr[class*="player_tr"]')
        for player_tds in player_trs:
            if ver in list(player_tds)[7]:
                player_name = list(player_tds)[1].select(
                    'a[class="player_name_players_table"]')[0].text
                player_url = site + list(player_tds)[1].select(
                    'a[class="player_name_players_table"]')[0]['href']

        logging.debug('gonna sleep {} secs for player [{}]{}. ramen!'.format(
            sleep, ver, player_name))

        time.sleep(sleep)
        player_resp = requests.get(player_url)
        soup = BeautifulSoup(player_resp.text, 'lxml')
        player_dict = {}
        player_dict['common_name'] = soup.select('span.header_name')[0].text
        player_dict['photo'] = soup.select(
            'div[class="pcdisplay-picture"]')[0].img['src']
        player_dict['full_name'] = soup.title.string.split(" - ")[1][:-9]
        player_dict['rating'] = soup.find_all(
            attrs={"class": "pcdisplay-rat"})[0].string

        z = list(soup.find_all('td', 'table-row-text'))

        player_dict['club'] = z[1].a.string
        player_dict['position'] = soup.find_all(
            attrs={"class": "pcdisplay-pos"})[0].string.strip()
        player_dict['nation'] = z[2].a.string
        player_dict['league'] = z[3].a.string
        player_dict['skills'] = z[4].next_element
        player_dict['weak_foot'] = z[5].next_element
        player_dict['intl_rep'] = z[6].text.strip()
        player_dict['foot'] = z[7].string.strip()
        player_dict['height'] = z[8].string[:3]
        player_dict['weight'] = z[9].string.strip()
        player_dict['revision'] = z[10].string
        player_dict['d_workrate'] = z[11].string
        player_dict['a_workrate'] = z[12].string
        player_dict['added_on'] = z[13].string
        if len(list(z[14])) > 2:
            player_dict['origin'] = z[14].a.string.strip()
        else:
            player_dict['origin'] = z[14].string.strip()
        player_dict['dob'] = str(z[15])[138:148]
        player_model = FIFAPlayer(data=player_dict)
        player_model.save()

        # TODO photo stuff

        return player_model
