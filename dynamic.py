import os
import cv2
import numpy as np
from PIL import Image


def getAvrW(_bin):
    return _bin.sum() / (_bin.shape[0]*_bin.shape[1])


def binarize(img, threshold):
    if isinstance(img, np.ndarray):
        cv_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif isinstance(img, str) and os.path.isfile(img):
        cv_gray = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
    elif isinstance(img, Image.Image):
        cv_gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    _, cv_bin = cv2.threshold(cv_gray, threshold, 255, cv2.THRESH_BINARY)

    return cv_bin


def dynamicThreshold(ndarray, template):
    '''
        returns _bin & avrw
    '''
    guess = template.guess
    lower_bound = template.bounds[0]
    upper_bound = template.bounds[1]
    step = template.step

    print('guess from template is ' + str(guess))
    _bin = binarize(ndarray, guess)
    avrw = getAvrW(_bin)
    print('firstly we got an avrw of ' + str(avrw))
    for t in range(1, 20):
        print('doing loop #' + str(t))
        if avrw > upper_bound:
            print('avrw still > {}'.format(upper_bound))
            guess += step
            print('now trying with guess ' + str(guess))
            _bin = binarize(ndarray, guess)
            avrw = getAvrW(_bin)
            print('and we get a new avrw of ' + str(avrw))
            if avrw < upper_bound:
                print('gonna break!')
                break
        elif avrw < lower_bound:
            print('avrw still < {}'.format(lower_bound))
            guess -= step
            print('now trying with guess ' + str(guess))
            _bin = binarize(ndarray, guess)
            avrw = getAvrW(_bin)
            print('and we get a new avrw of ' + str(avrw))
            if avrw > lower_bound:
                print('gonna break!')
                guess -= step
                _bin = binarize(ndarray, guess)
                avrw = getAvrW(_bin)
                print('and we get a new avrw of ' +
                      str(avrw) + 'just before break')
                break
        else:
            print('Albatross!')
            break
    return _bin, avrw
