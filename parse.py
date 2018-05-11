from ri import RabonaImage


class RabonaParse():
    def __init__(self, img):
        cropped = RabonaImage(img)
        cropped.crop()
        self.screen_raw = cropped.screen._raw
