import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import (match_descriptors, ORB, plot_matches)

from ri import Photo
from templates.FIFA18 import Matching


class Matcher():
    def __init__(self, _input, n_k=100):
        self.dest_img = Photo.convert(_input, 'PIL.Image')
        self.dest_array = np.array(self.dest_img.convert('L'))
        self.source_k = np.loadtxt('source_k_100')
        self.source_d = np.loadtxt('source_d_100')
        self.extract(_input)
        self.match()

    def extract(self, n_k=100):
        o = ORB(n_keypoints=100)
        o.detect_and_extract(self.dest_array)

        self.dest_k = o.keypoints
        self.dest_d = o.descriptors

    def reGenTemplate(self, n_k):
        self.source_img = Photo.convert('templates/feature0.png', 'PIL.Image')
        self.source_array = np.array(self.source_img.convert('L'))
        o = ORB(n_keypoints=n_k)
        o.detect_and_extract(self.source_array)
        return o.keypoints, o.descriptors

    def match(self):
        self.matches = match_descriptors(
            self.source_d, self.dest_d, cross_check=True, max_distance=0.5)

    def debug(self):
        self.source_img = Photo.convert('templates/standard.png', 'PIL.Image')
        plot_matches(plt, self.source_img, self.dest_img,
                     self.source_k, self.dest_k, self.matches)
        plt.axis('off')
        plt.ion()
        plt.show()

    def debug_off(self):
        plt.cla()  # clear axis
        plt.clf()  # clear figure
        plt.ioff()
