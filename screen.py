class Screen():

    def __init__(self, _bin, raw_wh, bleed=50):

        self.size = self.getScreen(_bin)
        bin_w, bin_h = len(_bin[0]), len(_bin)

        if 'bottom' in self.size.keys():
            self.size['head'] = self.size['bottom'] - 480
            self.size['bottom'] += bleed
        elif 'head' in self.size.keys():
            self.size['bottom'] = self.size['head'] + 480 + bleed

        def scalingBack(rect):
            w1, h1, w2, h2 = rect[0], rect[1], rect[2], rect[3]
            print(bin_w, bin_h, raw_wh)
            w1, w2 = round(w1/bin_w*raw_wh[0]), round(w2/bin_w*raw_wh[0])
            h1, h2 = round(h1/bin_h*raw_wh[1]), round(h2/bin_h*raw_wh[1])
            return (w1, h1, w2, h2)

        # ndarray.width * 1920
        rect = self.size
        self.bin_rect = (rect['left'], rect['head'],
                         rect['right'], rect['bottom'])
        self.real_rect = scalingBack(self.bin_rect)
        self._bin = 'not there yet'

    @classmethod
    def getScreen(self, bin_img):
        '''
            bin_img: ndarray
            rect = getScreen()
            all the calculations are based on a x*1920 ndarray
            so the return dict needs to be transformed back to raw size
        '''
        rect = {}
        w, h = len(bin_img[0]), len(bin_img)

        # first guess starts from y=960
        if sum(bin_img[960])/len(bin_img[960]) > 175:
            # hits a white plate, move downward 480px then upward
            for y in range(480):
                # moving downward until dark
                if sum(bin_img[960+y])/len(bin_img[960]) < 10:
                    rect['bottom'] = 960 + y
                    break
                # moving upward until dark
                elif sum(bin_img[960 - y])/len(bin_img[960]) < 10:
                    rect['head'] = 960 - y
                    break
        else:
            # hits black plate, move upward then downward
            for y in range(480):
                # moving upward until light
                if sum(bin_img[960-y])/len(bin_img[960-y]) > 175:
                    rect['bottom'] = 960 - y
                    break
                # moving downward until light
                elif sum(bin_img[960+y])/len(bin_img[960+y]) > 175:
                    rect['head'] = 960 + y
                    break

        # then find right edge starts from 80%
        startpoint = round(w*0.8)
        if bin_img[:, startpoint].sum()/h > 40:
            # hits a white plate
            for x in range(w-startpoint):
                # moving rightward
                if sum(bin_img[:, startpoint+x])/h < 10:
                    rect['right'] = startpoint + x
                    break
                # moving leftward
                pass
        else:
            print('cant find right edge, raw image might be no good')

        # then find left edge starts from x=200
        if bin_img[:, 200].sum()/h > 10:
            # hits a white plate, move downward 480px then upward
            for x in range(200):
                # moving leftward
                if sum(bin_img[:, 200-x])/h < 10:
                    rect['left'] = 200 - x
                    break
                # moving rightward
                pass
        else:
            print('cant find left edge, raw image might be no good')

        return rect
