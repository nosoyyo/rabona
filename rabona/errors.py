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
