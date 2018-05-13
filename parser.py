import os
import cv2
import numpy as np
from PIL import Image
import pytesseract as pyt

from ri import RabonaImage as ri
from templates.FIFA18 import Segmentation


class RabonaParser():
    '''
        do parse job on binarized screen img
    '''

    def __init__(self, i, template):
        if isinstance(i, Image.Image):
            self._bin = i
        elif isinstance(i, np.ndarray):
            print('not implemented format converting')
            # self._raw = Image.fromarray(img)
            # self._bin
        elif isinstance(i, ri):
            self._bin = i.screen._bin

        self._bin_w, self._bin_h = len(self._bin[0]), len(self._bin)
        # A_ratio for instance: 0.1723
        self._bin_A = self._bin[0:int(self._bin_h*template.A_ratio)]
        self.A_score_area = self.getScore(self._bin_A, Segmentation)

    def parse(self, img, lang='eng'):
        return pyt.image_to_string(img, lang=lang)

    @classmethod
    def getScore(self, _bin_A, template):
        if isinstance(_bin_A, np.ndarray):
            pass
        elif os.path.isfile(_bin_A):
            _bin_A = cv2.imread(_bin_A)

        w, h = len(_bin_A[0]), len(_bin_A)
        print(w, h)

        # get score_area
        half_A = _bin_A[-(int(h/2)):w]
        print('half_A.shape: ' + str(half_A.shape))
        #
        score_area_w = round(w * 0.1281)
        print('score_area_w: ' + str(score_area_w))
        score_area_start = round(w/2) - round(score_area_w/2) + 1
        print('score_area_start: ' + str(score_area_start))
        score_area = half_A[:,
                            score_area_start:score_area_start + score_area_w]

        # pyt
        img = Image.fromarray(score_areaf)
        return pyt.image_to_string(img, lang='eng')
