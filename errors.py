class InitFailure(Exception):
    def __init__(self, msg, code):
        if code is 1:
            print('file {} not found or maybe broken.'.format(msg))
        elif code is 2:
            print('width={}: too narrow. min width 1080'.format(msg))
        elif code is 3:
            print('height={}: too short. min height 608'.format(msg))
