import logging
import numpy as np
from face_recognition import face_locations

from hub import ImageHub
from errors import InitFailure
from src.FIFA18 import Anchoring

DEBUG = True

# init
logging.basicConfig(
    filename='log/screen.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class Screen():

    def __init__(self, _input):
        try:
            self.filename = _input
            self._raw = ImageHub.convert(_input, 'np.ndarray')
        except Exception as e:
            print(e)

        # meta
        self._raw_w, self._raw_h = len(self._raw[0]), len(self._raw)
        logging.info('Screen get the raw image w{} x h{}.'.format(
            self._raw_w, self._raw_h))

        # crop
        self.readFaces()
        self.crop()

    def readFaces(self):
        self.faces = None

        faces = face_locations(self._raw)
        if faces[0][1] > faces[1][1]:
            faces[0], faces[1] = faces[1], faces[0]
        self.faces = faces
        logging.info('{} faces detected'.format(len(self.faces)))

        def makeFaces(faces):
            rects = []
            for i in range(len(faces)):
                rects.append(
                    (faces[i][3], faces[i][0], faces[i][1], faces[i][2]))
            return np.array(rects)

        self.faces = makeFaces(self.faces)

    def crop(self):
        if len(self.faces) == 2:
            face_l, face_r = self.faces[0], self.faces[1]
            face_width = int(
                ((face_l[2] - face_l[0]) + (face_r[2] - face_r[0])) / 2)
            logging.info('face width: {}'.format(face_width))
            E_width = abs(face_r[0] - face_l[0])
            logging.info('E_width: {}'.format(E_width))

            # Section E
            E_x0 = face_l[2] + Anchoring.E_x0_bleed
            E_x1 = face_r[0] - Anchoring.E_x1_bleed
            E_y0 = min(face_l[1], face_l[3], face_r[1],
                       face_r[3]) - Anchoring.E_y_bleed
            E_y1 = max(face_l[1], face_l[3], face_r[1],
                       face_r[3]) + Anchoring.E_y_bleed
            self.E = self._raw[E_y0:E_y1, E_x0:E_x1]
            logging.info('E: {}'.format((E_x0, E_y0, E_x1, E_y1)))
            if DEBUG:
                ImageHub.save(self.E, self.filename + '_E')

            # Section A
            A_x0 = int(E_x0 + face_width)
            A_y0 = int(E_y0 - round(E_width*1.5) + Anchoring.A_y0_bleed)
            A_x1 = int(E_x1 + E_width*2 + face_width*3)
            A_y1 = int(A_y0 + face_width*2)
            self.A = self._raw[A_y0:A_y1, A_x0:A_x1]
            logging.info('A: {}'.format((A_x0, A_y0, A_x1, A_y1)))
            if DEBUG:
                ImageHub.save(self.A, self.filename + '_A')

            # score_area
            sa_x0 = int(E_x1 + E_width*0.75)
            sa_y0 = int(A_y0)
            # meimaobing, biedong sa_x1
            sa_x1 = int(sa_x0 + E_width/2) + Anchoring.sa_x_bleed
            # meimaobing, biedong sa_y1
            sa_y1 = int(sa_y0 + face_width + Anchoring.sa_y_bleed)
            self.sa = self._raw[sa_y0:sa_y1, sa_x0:sa_x1]
            logging.info('sa: {}'.format((sa_x0, sa_y0, sa_x1, sa_y1)))
            if DEBUG:
                ImageHub.save(self.sa, self.filename + '_sa')

            # home name

        else:
            raise InitFailure(self, 4)
