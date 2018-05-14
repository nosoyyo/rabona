import os
import cv2
import numpy as np
from PIL import Image
import pytesseract as pyt

from ri import RabonaImage as RI
from templates.FIFA18 import Segmentation


class RabonaParser():
    '''
        do parse job on binarized screen img
    '''

    def __init__(self, i, template):
        if isinstance(i, Image.Image):
            self._bin = i
        elif isinstance(i, np.ndarray):
            self._bin = Image.fromarray(img)
        elif isinstance(i, RI):
            self._bin = i.screen._bin

        self._bin_w, self._bin_h = len(self._bin[0]), len(self._bin)

        self.score_area = self.getScoreArea(self._bin_A, Segmentation)
        self.score = self.getScore(self.score_area)

    def slice_A(self, template):
        '''
            # District A
            # A_ratio for instance: 0.1723
        '''
        y = int(self._bin_h*template.A_ratio)
        _bin_A = self._bin[0:y]
        return _bin_A

    @classmethod
    def getScoreArea(self, _bin_A, template):
        if isinstance(_bin_A, np.ndarray):
            pass
        elif os.path.isfile(_bin_A):
            _bin_A = cv2.imread(_bin_A)
        elif isinstance(_bin_A, Image.Image):
            _bin_A = np.asarray(_bin_A)

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
        return half_A[:, score_area_start:score_area_start + score_area_w]

    @classmethod
    def getScore(self, score_area):
        score_area = RI.invert(score_area)
        img = Image.fromarray(score_area)
        return pyt.image_to_string(img, lang='eng')
