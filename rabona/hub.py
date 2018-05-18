import os
import uuid
import numpy as np
from PIL import Image


class ImageHub():

    def __init__(self, _input):
        self.image = self.convert(_input, to='PIL.Image')
        self._ndarray = self.convert(_input, to='np.ndarray')

    @classmethod
    def convert(self, _input, to='PIL.Image'):
        try:
            output = 'not ready yet'
            if isinstance(_input, np.ndarray):
                hub = Image.fromarray(_input)
            elif isinstance(_input, str) and os.path.isfile(_input):
                hub = Image.open(_input)
            elif isinstance(_input, Image.Image):
                hub = _input
            elif isinstance(_input, tuple):
                hub = Image.fromarray(_input)

            if not hub:
                return '_input not converted'
            elif to == 'PIL.Image':
                output = hub
            elif to == 'np.ndarray':
                output = np.array(hub)
            return output
        except Exception as e:
            print(e)

    @classmethod
    def look(self, _input):
        self.convert(_input, to='PIL.Image').show()

    @classmethod
    def invert(self, _input):
        _input = self.convert(_input, 'np.ndarray')
        for y in range(len(_input)):
            for x in range(len(_input[0])):
                _input[y][x] = abs(255-_input[y][x])
        return _input

    @classmethod
    def save(self, _input, filename=None, format='jpeg'):
        _input = self.convert(_input, to='PIL.Image')

        def makeFilename(format='jpeg'):
            if format in ['jpg', 'jpeg']:
                suffix = '.jpeg'
            elif format is 'png':
                suffix = '.png'
            return uuid.uuid4().__str__() + suffix

        if not filename:
            filename = makeFilename(format=format)

        _input.save(filename)
