# pythonw
import os
import cv2
import uuid
import numpy as np
from PIL import Image

from screen import Screen
from errors import InitFailure
from dynamic import dynamicThreshold
from templates.FIFA18 import Preparation, RectifyScreen, Segmentation


class Photo():
    def __init__(self, _input):
        self.photo = self.convert(_input, to='PIL.Image')
        self._ndarray = self.convert(_input, to='np.ndarray')

    @classmethod
    def convert(self, _input, to='PIL.Image'):
        if to == 'PIL.Image':
            if isinstance(_input, np.ndarray):
                output = Image.fromarray(_input)
            elif isinstance(_input, str) and os.path.isfile(_input):
                output = Image.open(_input)
            elif isinstance(_input, Image.Image):
                output = _input
            elif isinstance(_input, tuple):
                output = Image.fromarray(_input)
            elif isinstance(_input, RabonaImage):
                output = _input._raw

        elif to == 'np.ndarray':
            if isinstance(_input, np.ndarray):
                output = _input
            elif isinstance(_input, str) and os.path.isfile(_input):
                output = cv2.imread(_input)
            elif isinstance(_input, Image.Image):
                output = np.asarray(_input)
            elif isinstance(_input, tuple):
                output = np.asarray(_input)
            elif isinstance(_input, RabonaImage):
                output = _input._ndarray

        if output:
            return output
        else:
            raise InitFailure(_input, 0)


class RabonaImage():

    def __init__(self, _input):
        self._ndarray = Photo.convert(_input, 'np.ndarray')
        h, w, d = self._ndarray.shape
        if min(w, h) < 1080:
            raise InitFailure(w, 2)
        elif h < 1440:
            raise InitFailure(h, 3)

        # get the raw image obj
        self._raw = Photo.convert(_input, 'PIL.Image')
        self._raw_w, self._raw_h = self._raw.width, self._raw.height

        # Rabona deal with only one height of pictures, 1920px.
        if h != 1920:
            self._ndarray = cv2.resize(self._ndarray, (round(1920*w/h), 1920))

        # get binarized with dynamicThreshold
        self._bin, self.avrw = dynamicThreshold(self._ndarray, Preparation)

        # get the screen and go on dealing
        self.buildScreen()

    def buildScreen(self):
        self.screen = Screen(
            self._bin, (self._raw_w, self._raw_h), RectifyScreen)
        self.screen._raw = self._raw.crop(self.screen.real_rect)
        self.screen._bin, self.screen._bin_avrw = dynamicThreshold(
            self.screen._raw, Segmentation)

        bin_h, bin_w = self.screen._bin.shape
        if 1.7 < bin_w/bin_h < 2.1:
            self.aspect_ratio = bin_w/bin_h
            print('aspect ratio {} probabily good'.format(self.aspect_ratio))

    def show(self, arg='bin'):
        if arg is 'bin':
            self.look(self._bin)
        elif arg is 'raw':
            self.look(self._raw)

    @classmethod
    def invert(self, _bin):
        for y in range(len(_bin)):
            for x in range(len(_bin[0])):
                _bin[y][x] = abs(255-_bin[y][x])
        return _bin

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
        elif isinstance(img, tuple):
            tmp_img = Image.fromarray(img)
        tmp_img.show()

        if filename:
            os.remove(filename)

    @classmethod
    def save(self, img, filename=None, format='jpg'):
        def makeFilename(format='jpeg'):
            if format in ['jpg', 'jpeg']:
                suffix = '.jpg'
            elif format is 'png':
                suffix = '.png'
            return uuid.uuid4().__str__() + suffix

        if not filename:
            filename = makeFilename(format=format)
        if isinstance(img, np.ndarray):
            cv2.imwrite(filename, img)
