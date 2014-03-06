from __future__ import division, absolute_import, print_function
import numpy


class GeistFileBackend(object):
    def __init__(self, image):
        self._image = numpy.load(image)

    def create_process(self, command):
        pass

    def actions_transaction(self):
        pass

    @property
    def rect(self):
        return self._image.shape

    def capture(self):
        return self._image

    def key_down(self, name):
        pass

    def key_up(self, name):
        pass

    def button_down(self, button_num):
        pass

    def button_up(self, button_num):
        pass

    def move(self, point):
        pass

    def close(self):
        pass

    def __del__(self):
        pass
