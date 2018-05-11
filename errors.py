class RawImageNoGood(Exception):
    def __init__(self, raw, code):
        h, w = raw.shape
        if code is 1:
            message = '{} too narrow. min width 1080'.format(w)
        elif code is 2:
            message = '{} too short. min height 608'.format(h)
        elif code is 3:
            message = ''