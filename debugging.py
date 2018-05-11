# pythonw
import os
import cv2
import uuid
from shutil import copy
import numpy as np
from PIL import Image

from errors import RawImageNoGood


class RabonaImage():

    def __init__(self, img_file, threshold=175):
        self._raw = img_file
        self._ndarray = cv2.imread(img_file)
        h, w, d = self._ndarray.shape
        if w < 1080:
            raise RawImageNoGood(self._ndarray, 1)
        elif h < 1440:
            raise RawImageNoGood(self._ndarray, 2)
        if h != 1920:
            cv2.resize(self._ndarray, (round(1920*w/h), 1920))
        self._bin = self.binarize(img_file, threshold)
        self._100 = self.binarize(img_file, threshold=100)
        self._100_avrw = self.getAvrW(self._100)
        self._125 = self.binarize(img_file, threshold=125)
        self._125_avrw = self.getAvrW(self._125)
        self._150 = self.binarize(img_file, threshold=150)
        self._150_avrw = self.getAvrW(self._150)
        self._175 = self.binarize(img_file, threshold=175)
        self._175_avrw = self.getAvrW(self._175)
        self._200 = self.binarize(img_file, threshold=200)
        self._200_avrw = self.getAvrW(self._200)

    @classmethod
    def look(self, img):
        filename = uuid.uuid4().__str__() + '.jpg'
        if isinstance(img, np.ndarray):
            cv2.imwrite(filename, img)
        elif isinstance(img, str) and os.path.isfile(img):
            copy(img, filename)
        tmp_img = Image.open(filename)
        tmp_img.show()
        os.remove(filename)

    @classmethod
    def getAvrW(self, bin_img):
        return bin_img.sum() / (bin_img.shape[0]*bin_img.shape[1])

    @classmethod
    def binarize(self, img_file, threshold):

        cv_gray = cv2.cvtColor(self._ndarray, cv2.COLOR_BGR2GRAY)
        _, cv_bin = cv2.threshold(cv_gray, threshold, 255, cv2.THRESH_BINARY)

        return cv_bin

    @classmethod
    def getScreen(self, img_file, threshold):
        '''
            rect = getScreen()
        '''
        try:
            bin_img = self.binarize()(img_file, threshold)
            rect = {}
            # first guess starts from y=960
            if sum(bin_img[960])/1080 > 175:
                # hits a white plate, move downward 480px then upward
                for y in range(480):
                    # downward
                    if sum(bin_img[960+y])/1080 < 1:
                        rect['bottom_y0'] = 960 + y
                    # upward
                    elif sum(bin_img[960 - y])/1080 < 1:
                        rect['head_y0'] = 960 - y
            else:
                # hits black plate, move upward then downward
                for y in range(480):
                    # upward
                    if sum(bin_img[960 - y])/1080 < 1:
                        rect['head_y1'] = 960 - y
                        # downward
                    elif sum(bin_img[960+y])/1080 < 1:
                        rect['bottom_y1'] = 960 + y
            return rect
        except Exception as e:
            print(e)

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
