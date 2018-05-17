from apistar import App, Route

from models import Match


def loadUsers():
    with open('users', 'r') as u:
        return u.read().split(' ')


users = loadUsers()


def welcome():
    return {'message': 'Hi this is rabona.'}


def checkUser(username):
    global users
    if username not in users:
        with open('users', 'a') as u:
            u.write(username + ' ')
    users = loadUsers()


def match(arg, _id=None, data=None):
    '''
    Get the match data desired or create a new one.

    :param arg: <str> to choose modes from `new` or `get`.
    :param _id: <str> to fetch a certain match with the _id given.
    :param data: <dict> needed for creating new matches.
    :return: <obj> a Match object with data.
    '''
    if arg == 'new':
        if not data:
            return 'need data to create new match!'
        else:
            match = Match(data)
    elif arg == 'get':
        if not _id:
            return 'need id to get match data!'
        else:
            match = Match(_id)
    return match


def parse(image_file):
    pass


routes = [
    Route('/', method='GET', handler=welcome),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 20185, debug=True)
