__author__ = 'nosoyyo'
__date__ = '2018.5.3'

import os
import csv
import time
import random
import logging
import requests
from bs4 import BeautifulSoup

from exceptions import WorkingDirError

# init
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
logging.info('session started.')

site = 'https://www.futbin.com/'
leagues_page = site + '18/leagues?page='

# get random stuff & proxies
UserAgentCSV = open('ua.csv', 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]
random.shuffle(UserAgentList)


def getUA():
    return random.choice(UserAgentList)


def getReferer():
    base = 'https://www.futbin.com/18/player/'
    return base + str(round(random.random() * 10000))


proxies = {
    'http': '190.123.83.251:8080',
    'https': '190.104.195.210:53281'
}

headers = {}
headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
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
    # set up cwd
    working_dir = '/data/futbin'
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    os.chdir(working_dir)
    # logging.info("working dir ready. we're now in {}".format(os.getcwd()))
    print("working dir ready. we're now in {}".format(os.getcwd()))
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
        # logging.info(league_info['league_name'] + ' soup ready.')
        print(league_info['league_name'] + ' soup ready.')

        # store league info
        if league_info['league_name'] not in os.listdir():
            os.mkdir(league_info['league_name'])
        os.chdir(league_info['league_name'])
        content = 'league_info = ' + league_info.__str__() + '\n'
        saveFile(league_info['league_name']+'.py', content)

        # go inside the league
        time.sleep(10)
        headers['user-agent'] = getUA()
        headers['referer'] = getReferer()
        league_resp = requests.get(
            league_info['league_url'], headers=headers, cookies=cookies, proxies=proxies)
        league_soup = BeautifulSoup(league_resp.text, 'lxml')
        clubs = league_soup.select(
            'ul[class="dropdown-menu dropdown-menu2 general_dd"]')[4]('li')

        # strip
        for club in clubs:
            club_info = {}
            club_info['club_url'] = site + club.a['href']
            club_info['club_logo'] = club.img['src']
            club_info['club_name'] = club.text.strip()

            # store club info
            if club_info['club_name'] not in os.listdir():
                os.mkdir(club_info['club_name'])
            os.chdir(club_info['club_name'])
            content = 'club_info = ' + club_info.__str__() + '\nplayers = {}\n'
            saveFile(club_info['club_name']+'.py', content)

            # record all_clubs
            os.chdir('/data/futbin')
            content = club_info['club_name'] + '\n'
            saveFile('all_clubs', content)
            # logging.info('recorded {} into all_clubs.'.format(content))
            os.chdir(league_info['league_name']+'/'+club_info['club_name'])

            # drill in
            time.sleep(10)
            headers['user-agent'] = getUA()
            headers['referer'] = getReferer()
            club_resp = requests.get(
                club_info['club_url'], headers=headers, cookies=cookies, proxies=proxies)
            club_soup = BeautifulSoup(club_resp.text, 'lxml')
            # logging.info(club_info['club_name'] + ' soup ready.')
            players = club_soup.select('li[class="hvr-shrink"]')

            # break down
            for player in players:
                player_info = {}
                player_info['player_url'] = site + player.a['href']
                player_info['player_name'] = player.a['href'].split('/')[-1]
                player_bio = player.select('div')[0].select('div')
                player_info['player_rating'] = player_bio[0].text.strip()
                player_info['player_shortname'] = player_bio[1].text.strip()
                player_info['player_position'] = player_bio[2].text.strip()
                player_info['player_nation'] = player_bio[3].img['src']
                player_info['player_photo'] = player_bio[5].img['src']

                # store self and register in parent club
                content = "players['{}'] = ".format(
                    player_info['player_shortname']) + player_info.__str__() + '\n'
                saveFile(club_info['club_name']+'.py', content)

            '''
            # don't forget go back up
            if os.getcwd().split('/')[-1] is club_info['club_name']:
                # this indicates nothing wrong.
                os.chdir('..')
            else:
                correct = '{}/{}/{}'.format(
                    working_dir, league_info['league_name'], club_info['club_name'])
                raise WorkingDirError(correct)
            '''
            # temp ops
            print(club_info['club_name'] + ' done.')
            os.chdir('..')

        '''
        # don't forget we're still in league dir!
        if os.getcwd().split('/')[-1] is league_info['league_name']:
            # this indicates nothing wrong.
            os.chdir('..')
        else:
            correct = '{}/{}'.format(
                    working_dir, league_info['league_name'])
            raise WorkingDirError(correct)
        '''
        # temp ops
        print(league_info['league_name'] + ' done.')
        os.chdir('..')


if __name__ == '__main__':
    main()
