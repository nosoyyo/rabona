# pythonw
from hub import ImageHub
from screen import Screen
from errors import InitFailure


class RabonaImage():

    def __init__(self, _input):
        self._ndarray = ImageHub.convert(_input, 'np.ndarray')
        h, w = self._ndarray.shape[:2]

        # get the raw image obj
        self._raw = ImageHub.convert(_input, 'PIL.Image')
        self._raw_w, self._raw_h = self._raw.width, self._raw.height
        self.screen = Screen(self._raw)


