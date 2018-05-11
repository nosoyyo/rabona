# pythonw
import os
import cv2
import uuid
from shutil import copy
import numpy as np
from PIL import Image

from errors import *


def look(img):
    filename = uuid.uuid4().__str__() + '.jpg'
    if isinstance(img, np.ndarray):
        cv2.imwrite(filename, img)
    elif isinstance(img, str) and os.path.isfile(img):
        copy(img, filename)
    tmp_img = Image.open(filename)
    tmp_img.show()
    os.remove(filename)


def prepare(img_file, threshold=175):
    raw = cv2.imread(img_file)
    h, w, d = raw.shape
    if w < 1080:
        raise errors.RawImageNoGood(raw, 1)
    elif h < 1440:
        raise errors.RawImageNoGood(raw, 2)

    if h > 1920:
        cv2.resize(raw, (1920*w/h, 1920))

    cv_gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    _, cv_bin = cv2.threshold(cv_gray, threshold, 255, cv2.THRESH_BINARY)

    return cv_bin


def detectScreen(img_file):
    try:
        bin_img = prepare(img_file)
    except Exception as e:
        print(e)
    rect = {}
    if sum(bin_img[960])/1080 > 180:
        # here's white plate, move downward 480px then upward
        for y in range(480):
            # downward
            if sum(bin_img[960+y])/1080 < 1:
                rect['bottom_y'] = 960 + y
            # upward
            elif sum(bin_img[960 - y])/1080 < 1:
                rect['head_y'] = 960 - y
    else:
        # black plate, move upward then downward
        for y in range(480):
            # upward
            if sum(bin_img[960 - y])/1080 < 1:
                rect['bottom_y'] = 960 - y
                # downward
            elif sum(bin_img[960+y])/1080 < 1:
                rect['head_y'] = 960 + y
    return rect
