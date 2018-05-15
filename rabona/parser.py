import pytesseract as pyt

from ri import Photo
from templates.FIFA18 import Segmentation


class RabonaParser():
    '''
        do parse job on binarized screen img,
        only RI.screen._bin
    '''

    def __init__(self, _input, template):
        # EAFP
        self._bin = Photo.convert(_input, to='np.ndarray')
        self._bin_w, self._bin_h = len(self._bin[0]), len(self._bin)

        # Section A
        self._bin_A = self.slice_A(self._bin, Segmentation)
        self.score_area = self.getScoreArea(self._bin_A, Segmentation)
        self.score = self.getScore(self.score_area)

    @classmethod
    def slice_A(self, _bin, template):
        '''
            # crop Section A out of Screen._bin
            # A_ratio for instance: 0.25
        '''
        h, w = _bin.shape
        y = int(h*template.A_ratio)
        print('y({}) = h({}) * A_ratio({})'.format(y, h, template.A_ratio))

        # get rid of the non-dark bottom rows
        for step in range(1, y):
            print('range: {}'.format((1, y)))
            if sum(_bin[0:y][-1]) / w > 1:
                print('avrw of row[{}] is {}'.format(
                    y-1, sum(_bin[0:y][y-step]) / w))
                y -= 1
                if sum(_bin[0:y][-1]) / w < 1:
                    print('gonna break on y={}'.format(y))
                    break
            else:
                print('Albatross!')
                break
        _bin_A = _bin[0:y]
        print('height {}, width {}'.format(y, len(_bin_A[0])))
        return _bin_A

    @classmethod
    def getScoreArea(self, _bin_A, template):

        h, w = _bin_A.shape
        print('_bin_A height: {}, width: {}'.format(h, w))

        # deal with width
        score_area_w = round(w * template.A_score_ratio) + \
            template.A_score_bleed
        print('score_area_w: ' + str(score_area_w))
        score_area_start = round(w/2) - round(score_area_w/2) + 1
        print('score_area_start: ' + str(score_area_start))

        # remove the bottom black block
        for i in range(2, len(_bin_A)-1):
            y = len(_bin_A) - i
            if sum(sum(_bin_A[y-1:y+1])/len(_bin_A[y])*3) > 1:
                break
        sa = _bin_A[0:y]

        return sa[:, score_area_start:score_area_start + score_area_w]

    @classmethod
    def getScore(self, score_area):
        return pyt.image_to_string(score_area, config='--psm 7', lang='eng')
