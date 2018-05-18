# pythonw
import logging

from screen import Screen
from hub import ImageHub
from utils.ocrspace import ocr_space_file
from parser import RabonaParserA

# init
logging.basicConfig(
    filename='log/ri.log',
    level=logging.INFO,
    format='%(asctime)s%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class RabonaImage():
    '''

    :param _input: `str` local file name with relative path.
    '''

    def __init__(self, _input):
        self.filename = _input.replace(_input.split('.')[-1], '')[:-1]
        self.suffix = '.' + _input.split('.')[-1]

        self.screen = Screen(_input)

        # parsing
        self.A_json = self.send4OCR(self.screen.A)
        self.A_parsed = RabonaParserA(self.A_json)

    def send4OCR(self, _input):
        file_full_name = self.filename + '_ocr' + self.suffix
        ImageHub.save(_input, file_full_name)
        ocr_space_file(file_full_name)
