__author__ = 'nosoyyo'
__date__ = '2018.5.3'

import os
import csv
import time
import random
import logging
import requests
from bs4 import BeautifulSoup
from importlib import import_module

from utils.pipeline import MongoDBPipeline
from models import (FIFAClub, FIFAPlayer, FIFAPlayerPhoto,
                    FIFAClubLogo, FIFALeague)

# init
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')
logging.info('session started.')

site = 'https://www.futbin.com/'
leagues_page = site + '18/leagues?page='

# get random stuff & proxies
UserAgentCSV = open('ua.csv', 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]
random.shuffle(UserAgentList)


def getdir(): return list(
    filter(os.path.isdir, [item for item in os.listdir()]))


def make_an_one_time_dict():
    club_league_dict = {}

    os.chdir('data/leagues')
    leagues = getdir()

    for league in leagues:
        os.chdir(league)
        clubs = getdir()
        for club in clubs:
            club_league_dict[club] = league
        os.chdir('..')
    return club_league_dict


def getUA():
    return random.choice(UserAgentList)


def getReferer():
    base = 'https://www.futbin.com/18/player/'
    return base + str(round(random.random() * 10000))


proxies = {
    'http': '190.123.83.251:8080',
    #    'http': '190.104.195.210:8080'
}

headers = {}
headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,\
image/webp,image/apng,*/*;q=0.8'
headers['accept-encoding'] = 'gzip, deflate, br'
headers['accept-language'] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
headers['cache-control'] = 'max-age=0'
headers['upgrade-insecure-requests'] = '1'

cookies = {}
cookies['PHPSESSID'] = '2194d5b7ddb29938c503c0a30e72a227'
cookies['__cfduid'] = 'da8b2177c5f16dd03280acd933d2e6b6f1525333552'
cookies['platform'] = 'ps4'
# cookies['sc_is_visitor_unique'] = 'rx9767571.1525333742'


def saveFile(filename, content, mode='r+'):
    if filename not in os.listdir():
        flag = 'w+'
    else:
        flag = 'r+'
    with open(filename, flag) as f:
        if content not in f.read():
            f.write(content)
    # logging.info('saved {} in {}.'.format(content, filename))


def main():

    print('gonna sleep 10 sec. RAmen.')
    time.sleep(10)
    headers['user-agent'] = getUA()
    headers['referer'] = getReferer()
    resp = requests.get(leagues_page, headers=headers,
                        cookies=cookies, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'lxml')
    print('soup ready.')
    leagues = soup.select('tr[class="player_tr"]')

    # grab meta
    for league_raw in leagues:
        league_info = {}
        league_info['league_url'] = site + league_raw.a['href']
        league_info['league_name'] = league_raw.a.text
        league_info['league_logo'] = league_raw.img['src']
        league_model = FIFALeague(data=league_info)
        league_model.clubs = []
        league_model.save()

        # go inside the league
        time.sleep(10)
        headers['user-agent'] = getUA()
        headers['referer'] = getReferer()
        league_resp = requests.get(
            league_info['league_url'], headers=headers, cookies=cookies,
            proxies=proxies)
        league_soup = BeautifulSoup(league_resp.text, 'lxml')
        clubs = league_soup.select(
            'ul[class="dropdown-menu dropdown-menu2 general_dd"]')[4]('li')

        # strip
        for club in clubs:
            club_info = {}
            club_info['club_url'] = site + club.a['href']
            club_info['club_logo'] = club.img['src']
            club_info['club_name'] = club.text.strip()
            club_model = FIFAClub(data=club_info)
            club_model.players = []
            club_model.save()

            club_logo_resp = requests.get(
                club_info['club_logo'], headers=headers,
                cookies=cookies, proxies=proxies)
            logo_doc = {'club_name': club_model.club_name,
                        'club_oid': club_model.ObjectId,
                        'logo_bytes': club_logo_resp.content}
            FIFAClubLogo(data=logo_doc)

            # drill in
            time.sleep(10)
            headers['user-agent'] = getUA()
            headers['referer'] = getReferer()
            for page in range(1, 5):
                club_resp = requests.get(
                    club_info['club_url'] + '?page=' + page, headers=headers,
                    cookies=cookies, proxies=proxies)
                club_soup = BeautifulSoup(club_resp.text, 'lxml')
                # logging.info(club_info['club_name'] + ' soup ready.')
                players = club_soup.select('li[class="hvr-shrink"]')

                # break down
                for player in players:
                    player_info = {}
                    player_info['player_url'] = site + player.a['href']
                    player_info['player_name'] = player.a['href'].split(
                        '/')[-1]
                    player_bio = player.select('div')[0].select('div')
                    player_info['player_rating'] = player_bio[0].text.strip()
                    player_info['player_shortname'] = player_bio[1].text.strip()
                    player_info['player_position'] = player_bio[2].text.strip()
                    player_info['player_nation'] = player_bio[3].img['src']
                    player_info['player_photo'] = player_bio[5].img['src']

                    player_model = FIFAPlayer(data=player_info)
                    player_photo_resp = requests.get(
                        player_info['player_photo'], headers=headers,
                        cookies=cookies, proxies=proxies)
                    photo_doc = {'player_name': player_model.player_name,
                                 'player_oid': player_model.ObjectId,
                                 'photo_bytes': player_photo_resp.content}
                    FIFAPlayerPhoto(data=photo_doc)

                    # append, temporary approach
                    club_model.players.append(player_model.__dict__)
                    club_model.save()

                if len(players) < 30:
                    break
            # append, temporary approach
            league_model.clubs.append(club_model.__dict__)
            league_model.save()
            # temp ops
            print(club_info['club_name'] + ' done.')

        # temp ops
        print(league_info['league_name'] + ' done.')


if __name__ == '__main__':
    main()
