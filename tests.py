from ri import RabonaImage as RI
from parser import RabonaParser as RP
from templates.FIFA18 import Segmentation
import pytesseract as pyt

i = 'input/1.jpeg'
i = RI(i)
test = RP(i, Segmentation)

text = pyt.image_to_string(test.score_area, lang='eng')
