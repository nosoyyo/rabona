__author__ = 'nosoyyo'
__version__ = {'0.1': '2017.4.5',
               '1.0': '2018.5.3',
               '1.1': '2018.5.31',
               }

import time
import random
import logging
import requests
from functools import reduce
from bs4 import BeautifulSoup

from errors import InvalidURLError
from .FIFA_club import FIFAClub
from .FIFA_league import FIFALeague
from .FIFA_player import FIFAPlayer
from utils.pipeline import MongoDBPipeline


sleep = 10
magic_number = '16acaf9de83cf16'


def magic(str: str) -> str:
    pass


def readMagic(magic_number: str)->str:
    '''
    Not serious magic at all.
    Just to avoid literal material.
    '''
    tm = '{:d}'.format(int(eval('0x'+magic_number)))
    result = []
    for i in range(0, len(tm), 3):
        a, b = i, i+3
        result.append(int(tm[a:b]))
    return reduce(lambda x, y: x+y, map(chr, result))


# init
logging.basicConfig(
    filename='var/log/dataminer.log',
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')
logging.info('session started.')

site = 'https://www.{}.com/'.format(readMagic(magic_number))


def getReferer():
    base = 'https://www.{}.com/18/player/'
    return base + str(round(random.random() * 10000))


def getLeagues(get_clubs=False, sleep=sleep):
    '''
    Base method of datamining.
    '''
    url = 'https://www.{}.com/18/leagues?page='.format(readMagic(magic_number))

    for page in range(1, 3):
        logging.debug('gonna sleep {} sec for resp. RAmen.'.format(sleep))
        time.sleep(sleep)
        page_url = url + str(page)
        print('grabbing {}'.format(page_url))
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        logging.debug('big soup ready. len: {}'.format(len(soup)))
        leagues = soup.select('tr[class="player_tr"]')
        logging.debug('{} leagues get.'.format(len(leagues)))

        # grab meta
        for league_raw in leagues:
            league_info = {}
            league_info['league_name'] = league_raw.a.text
            league_info['league_url'] = 'https://www.{}.com/18/leagues/'\
                .format(readMagic(magic_number)) + league_raw.a.text
            league_info['league_logo'] = league_raw.img['src']
            league_model = FIFALeague(data=league_info)
            league_model.clubs = []
            league_model.save()

            if get_clubs:
                league_model.clubs = getClubs(league_model.league_name)
                league_model.save()


def getClubs(league_name) -> list:
    '''
    Only for get league.clubs `list`, not for any further details
    Use
    `getPlayers(<club_name>)`
    for player list of a club, or use
    `getPlayer(<player_name>)`
    for player full attributes

    Return a list of `club_dict`s

    :param club_name: `str` must be common full club_name
    :param url: `str` better use url for more accuracy
    '''
    league_url = 'https://www.{}.com/18/leagues/'.format(
        readMagic(magic_number)) + league_name

    time.sleep(sleep)
    logging.debug('grabbing {}'.format(league_url))
    league_resp = requests.get(league_url)
    league_soup = BeautifulSoup(league_resp.text, 'lxml')
    logging.debug('league soup ready')
    clubs = league_soup.select(
        'ul[class="dropdown-menu dropdown-menu2 general_dd"]')[4]('li')
    logging.debug('get {} clubs.'.format(len(clubs)))
    logging.debug('{} clubs grabbed.'.format(len(clubs)))

    clubs_list = []
    # strip
    for club in clubs:
        club_info = {}
        club_info['league'] = league_name
        club_info['club_name'] = club.text.strip()
        club_info['club_url'] = site + club.a['href']
        club_info['club_logo'] = club.img['src']
        clubs_list.append(club_info)
        logging.debug('{} appended to clubs.'.format(club_info['club_name']))
    return clubs_list


def getPlayers(club_name: str=None, url: str=None) -> None:
    '''
    Only for get club.players `list`, not for get player full attributions.

    :param club_name: `str` must be common full club_name
    :param url: `str` valid {} url
    '''
    if club_name:
        club_url = 'https://www.{}.com/18/clubs/'.format(
            readMagic(magic_number)) + club_name
    else:
        club_url = url

    club_model = FIFAClub(name=club_name)
    club_model.players = {}

    for page in range(1, 5):
        logging.debug('gonna sleep {} sec for club_resp. RAmen.'.format(sleep))
        time.sleep(sleep)
        club_resp = requests.get(club_url + '?page=' + str(page))
        club_soup = BeautifulSoup(club_resp.text, 'lxml')

        club_name = club_soup.select('div[class="player_header header_top"]')[
            0].text.strip().replace('FIFA 18 ', '')

        logging.debug('{} page {} soup ready'.format(club_name, page))
        players = club_soup.select('li[class="hvr-shrink"]')
        logging.debug('{} players seen.'.format(len(players)))

        if len(players) == 0:
            logging.debug('players == 0, break!')
            break

        # break down
        for player in players:
            # `common_name` here
            common_name = player.a['href'].split('/')[-1]
            short_name = player.select('div[class="pcdisplay-name"]')[0].text
            club_model.players[common_name] = short_name
            club_model.save()
            print('{} done.'.format(common_name))
        print('{} done.'.format(club_model.club_name))


def isValidURL(url):
    # TODO
    return True


def getPlayer(common_name: str=None,
              url: str=None,
              ver: str='Normal',
              ) -> FIFAPlayer:
    '''
    common name like `Cristiano Ronaldo`, `Neymar`
    '''
    if common_name is not None:
        try:
            return FIFAPlayer(common_name=common_name)
        except Exception as e:
            logging.error('`getPlayer` raises "{}"'.format(e))

    if not url:
        query = 'https://www.{}.com/18/players?search=' + common_name
        r = requests.get(query)
        soup = BeautifulSoup(r.text, 'lxml')
        player_trs = soup.select('tr[class*="player_tr"]')
        for player_tds in player_trs:
            if ver in list(player_tds)[7]:
                player_name = list(player_tds)[1].select(
                    'a[class="player_name_players_table"]')[0].text
                player_url = site + list(player_tds)[1].select(
                    'a[class="player_name_players_table"]')[0]['href']
    else:
        if isValidURL(url):
            player_url = url
        else:
            raise InvalidURLError(url)

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


def main():
    m = MongoDBPipeline()
    try:
        for league in m.ls('FIFA_leagues'):
            for club in league['clubs']:
                if 'players' not in club.keys():
                    getPlayers(club['club_name'])
                else:
                    continue
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
