import os


class WorkingDirError(BaseException):
    def __init__(self, correct_dir):
        print('\rShould be in {}, but now in {}\r'.format(
            correct_dir, os.getcwd()))
