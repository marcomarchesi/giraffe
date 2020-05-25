'''
gprimitives
'''

import numpy as np
from gmath import FARAWAY

class Camera:
    def __init__(self, position):
        self.position = position

class Light:
    def __init__(self, position, intensity):
        self.position = position
