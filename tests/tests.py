from face_recognition import face_locations
import numpy as np
import cv2
import pytesseract as pyt
from ri import RabonaImage as RI
from parser import RabonaParser as RP
from templates.FIFA18 import Segmentation


i = 'input/0.jpeg'
i = RI(i)
test = RP(i.screen._bin, Segmentation)

text = pyt.image_to_string(test.score_area, lang='eng')


def anchors(self):
    image = self._raw
    cv_pattern = cv2.CascadeClassifier(
        'src/haarcascades/haarcascade_profileface.xml')
    try:
        anchors_cv = cv_pattern.detectMultiScale(
            image, scaleFactor=1.1, minNeighbors=1, minSize=(30, 30))
        anchors_fr = face_locations(image)
    except Exception as e:
        print(e)

    def makeRect(points, arg):
        if arg is 'cv':
            rect_cv = []
            for i in range(len(points)):
                rect_cv.append((anchors_cv[i][0], anchors_cv[i][1], anchors_cv[i]
                                [0]+anchors_cv[i][2], anchors_cv[i][1]+anchors_cv[i][3],))
            return np.array(rect_cv)
        elif arg is 'fr':
            rect_fr = []
            for i in range(len(points)):
                rect_fr.append(
                    (anchors_fr[i][3], anchors_fr[i][0], anchors_fr[i][1], anchors_fr[i][2]))
            return np.array(rect_fr)

    if anchors_cv and anchors_fr:
        rect_cv, rect_fr = makeRect(
            anchors_cv, 'cv'), makeRect(anchors_fr, 'fr')
