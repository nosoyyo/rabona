# pythonw
import logging
import pytesseract as pyt

from screen import Screen
from hub import ImageHub
from utils.ocrspace import ocr_space_file
from parsers import RabonaParserA

# init
logging.basicConfig(
    filename='log/ri.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s \
    %(message)s')


class RabonaImage():
    '''

    :param _input: `str` local file name with relative path.
    '''

    def __init__(self, _input):
        self.filename = _input.replace(_input.split('.')[-1], '')[:-1]
        self.suffix = '.' + _input.split('.')[-1]

        self.screen = Screen(_input)

        # parsing with ocr.space
        # self.A_json = self.send4OCR(self.screen.A)
        # self.A_parsed = RabonaParserA(self.A_json)

        # parsing with local.pyt
        A = ImageHub.convert(self.screen.A, 'np.ndarray')
        A_rough = pyt.image_to_string(A, config='--psm 6', lang='eng')
        self.A_parsed = RabonaParserA(A_rough)


'''
        E = ImageHub.convert(self.screen.E, 'np.ndarray')
        E_rough = pyt.image_to_string(E, config='--psm 6', lang='eng')
        self.E_parsed = RabonaParserE(E_rough)
'''

def send4OCR(self, _input):
    file_full_name = self.filename + '_ocr' + self.suffix
    ImageHub.save(_input, file_full_name)
    ocr_space_file(file_full_name)
