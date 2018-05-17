import uuid


class User():
    def __init__(self, _id=None):
        if not _id:
            self.id = uuid.uuid4()
        elif isinstance(_id, uuid.UUID):
            self.id = _id
        self.username = ''