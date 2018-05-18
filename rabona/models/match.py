import uuid


class Match():
    def __init__(self, _id=None, data=None):
        if not _id:
            self.id = uuid.uuid4()
        elif isinstance(_id, uuid.UUID):
            self.id = _id
        self.home = data['home']
        self.away = data['']
        self.result = data['']
        self.goals = data['']
        self.conceded = data['']
        self.motm = data['']
        self.motm_rating = data['']
        self.fact = data['']
