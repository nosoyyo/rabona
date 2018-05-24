import os


class WorkingDirError(BaseException):
    def __init__(self, correct_dir):
        print('\rShould be in {}, but now in {}\r'.format(
            correct_dir, os.getcwd()))


class PipelineError(BaseException):
    pass


class InvalidCollectionError(PipelineError):
    def __init__(self, msg):
        print('{} is not a valid collection!'.format(msg))
