# pythonw
import os
import cv2
import uuid
import numpy as np
from PIL import Image
from shutil import copy

from screen import Screen
from errors import InitFailure


class RabonaImage():

    def __init__(self, img_file, threshold=175):
        if not os.path.isfile(img_file):
            raise InitFailure(img_file, 1)
        self._ndarray = cv2.imread(img_file)
        h, w, d = self._ndarray.shape
        if w < 1080:
            raise InitFailure(w, 2)
        elif h < 1440:
            raise InitFailure(h, 3)

        # Rabona deal with only one height of pictures, 1920px.
        if h != 1920:
            self._ndarray = cv2.resize(self._ndarray, (round(1920*w/h), 1920))
            self._raw = Image.open(img_file)
            _raw_dest = (round(1920*self._raw.width/self._raw.height), 1920)
            self._raw = self._raw.resize(_raw_dest, Image.LANCZOS)

        # get binarized with dynamicThreshold
        self._bin, self.avrw = self.dynamicThreshold(self._ndarray, threshold)

        # get the screen and crop
        self.screen = Screen(self._bin)

    def crop(self):
        '''
            temporary
        '''
        region = self.screen.rect
        ow, oh = self._raw.width, self._raw.height
        new_w = round(1920*ow / oh)
        self.screen._raw = self._raw.resize(
            (new_w, 1920), Image.LANCZOS).crop(region)

    @classmethod
    def dynamicThreshold(self, ndarray, threshold):
        print('original threshold is ' + str(threshold))
        _bin = self.binarize(ndarray, threshold)
        avrw = self.getAvrW(_bin)
        print('firstly we got an avrw of ' + str(avrw))
        for t in range(1, 20):
            print('doing loop #' + str(t))
            if avrw > 50:
                print('avrw still > 50')
                threshold += 15
                print('now trying with threshold ' + str(threshold))
                _bin = self.binarize(ndarray, threshold)
                avrw = self.getAvrW(_bin, )
                print('and we get a new avrw of ' + str(avrw))
                if avrw < 50:
                    print('gonna break!')
                    break
            elif avrw < 40:
                print('avrw still < 40')
                threshold -= 15
                print('now trying with threshold ' + str(threshold))
                _bin = self.binarize(ndarray, threshold)
                avrw = self.getAvrW(_bin)
                print('and we get a new avrw of ' + str(avrw))
                if avrw > 40:
                    print('gonna break!')
                    break
            else:
                print('Albatross!')
                break
        return _bin, avrw

    def show(self, arg='bin'):
        if arg is 'bin':
            self.look(self._bin)
        elif arg is 'raw':
            self.look(self._raw)

    @classmethod
    def look(self, img):
        filename = uuid.uuid4().__str__() + '.jpg'
        if isinstance(img, np.ndarray):
            cv2.imwrite(filename, img)
        elif isinstance(img, str) and os.path.isfile(img):
            copy(img, filename)
        elif isinstance(img, Image.Image):
            return img.show()
        tmp_img = Image.open(filename)
        tmp_img.show()
        os.remove(filename)

    @classmethod
    def getAvrW(self, bin_img):
        return bin_img.sum() / (bin_img.shape[0]*bin_img.shape[1])

    @classmethod
    def binarize(self, img, threshold):
        if isinstance(img, np.ndarray):
            cv_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif isinstance(img, str) and os.path.isfile(img):
            cv_gray = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        _, cv_bin = cv2.threshold(cv_gray, threshold, 255, cv2.THRESH_BINARY)

        # EAFP
        self._gray = cv_gray
        return cv_bin

    def getSections(self, img_file, threshold=175):
        try:
            bin_img = self.binarize(img_file, threshold)
            sections = {}
            if 'some condition':
                'this is section A'
                sections['A'] = 'section_A'
            elif 'some condition':
                'this is section BCDEF'
            elif 'some condition':
                'this is section G'
                sections['G'] = 'section_G'
            return sections
        except Exception as e:
            print(e)
