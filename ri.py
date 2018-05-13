# pythonw
import os
import cv2
import uuid
import numpy as np
from PIL import Image

from screen import Screen
from errors import InitFailure
from dynamic import dynamicThreshold
from templates.FIFA18 import DetectScreen, Segmentation


class RabonaImage():

    def __init__(self, img_file):
        if not os.path.isfile(img_file):
            raise InitFailure(img_file, 1)
        self._ndarray = cv2.imread(img_file)
        h, w, d = self._ndarray.shape
        if w < 1080:
            raise InitFailure(w, 2)
        elif h < 1440:
            raise InitFailure(h, 3)

        # get the raw image obj
        self._raw = Image.open(img_file)
        self._raw_w, self._raw_h = self._raw.width, self._raw.height

        # Rabona deal with only one height of pictures, 1920px.
        if h != 1920:
            self._ndarray = cv2.resize(self._ndarray, (round(1920*w/h), 1920))

        # get binarized with dynamicThreshold
        self._bin, self.avrw = dynamicThreshold(self._ndarray, DetectScreen)

        # get the screen and go on dealing
        self.screen = Screen(
            self._bin, (self._raw_w, self._raw_h), DetectScreen.bleed)
        self.crop()
        self.screen._bin, self.screen._bin_avrw = dynamicThreshold(
            self.screen._raw, Segmentation)

    def crop(self):
        region = self.screen.real_rect
        self.screen._raw = self._raw.crop(region)

    def show(self, arg='bin'):
        if arg is 'bin':
            self.look(self._bin)
        elif arg is 'raw':
            self.look(self._raw)

    def makeFilename(self, format='jpeg'):
        if format in ['jpg', 'jpeg']:
            suffix = '.jpg'
        elif format is 'png':
            suffix = '.png'
        return uuid.uuid4().__str__() + suffix

    @classmethod
    def look(self, img):

        filename = None
        if isinstance(img, np.ndarray):
            filename = uuid.uuid4().__str__() + '.jpg'
            cv2.imwrite(filename, img)
            tmp_img = Image.open(filename)
        elif isinstance(img, str) and os.path.isfile(img):
            tmp_img = Image.open(img)
        elif isinstance(img, Image.Image):
            tmp_img = img
        tmp_img.show()

        if filename:
            os.remove(filename)

    @classmethod
    def save(self, img, filename=None, format='jpg'):
        if not filename:
            filename = self.makeFilename(format=format)
        if isinstance(img, np.ndarray):
            cv2.imwrite(filename, img)