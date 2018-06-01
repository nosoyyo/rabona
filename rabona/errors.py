class InitFailure(Exception):
    def __init__(self, msg, code):
        if code is 0:
            print('unknown error with input {}.'.format(msg))
        elif code is 1:
            print('file {} not found or maybe broken.'.format(msg))
        elif code is 2:
            print('height={}: too short. min width 960'.format(msg))
        elif code is 3:
            print('anchors={}: should be 2'.format(msg))
        elif code is 4:
            print('cannot get anchor! ')


class UnrecognizableTextError(Exception):
    def __init__(self, raw):
        print('unrecognizable raw text: {}'.format(raw))


class HandlerInitError(Exception):
    def __init__(self, nb: int, nf: int):
        print('{} buttons need {} handlers, got {}!'.format(nb, nb, nf))


class User310Error(Exception):
    def __init__(self, home_score: int, away_score: int):
        print('{}:{} is not a valid match score!'.format(home_score,
                                                         away_score))


class AppointOpponentError(Exception):
    def __init__(match):
        print('One or two of "user_310": {}, "user_is_home": {} might\
              be broken!'.format(
            match.user_310, match.user_is_home))


class InvalidURLError(Exception):
    def __init__(self, url):
        print('Url {} is not a valid futbin url. \
        Check it carefully!'.format(url))
