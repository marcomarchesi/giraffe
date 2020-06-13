'''
Giraffe

Some starting points:
https://github.com/jamesbowman/raytrace/blob/master/rt3.py
https://www.scratchapixel.com/index.php


'''

from PIL import Image
from functools import reduce
import numpy as np
import time
from PySide2 import QtGui,QtCore
from PySide2.QtWidgets import QApplication, QLabel
import sys
import random
import h5py
from tqdm import tqdm


from argparse import ArgumentParser
from giraffe import show_logo, Giraffe, show_build, TODO
from gmath import vec3
from gprimitives import Light, Camera, Sphere, CheckeredSphere
from grenderer import render, preview
from gdataset import generate_scene

from gutils import TicToc

from PIL import Image

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=256)
parser.add_argument('--image-height', default=256)
parser.add_argument('--focal-length', default=1.0)
args = parser.parse_args()


# size of the image to render
(width, height) = (args.image_width, args.image_height)
size = (width, height)

# start with this
# increment the build number
app = Giraffe()

# Visualisation on PySide
gui_app = QApplication(sys.argv)

def array2qpixmap(img_array):
    height, width, channels = img_array.shape
    bytesPerLine, _, _ = img_array.strides
    image = QtGui.QImage(
        img_array.data.tobytes(),
        width,
        height,
        bytesPerLine,
        QtGui.QImage.Format_RGB888,
    )
    return QtGui.QPixmap.fromImage(image)


'''
DEFAULT:
Point light position
light0 = Light(vec3(-5, 3, -10), 0.1)
Camera position       
camera0 = Camera(vec3(0, 0, 0), args.focal_length)
objects in the scene
scene = [
    Sphere(vec3(.75, .1, 1), .6, vec3(0, 1, 1)),
    Sphere(vec3(-.75, .1, 2.25), .6, vec3(0, 1, .6)),
    Sphere(vec3(-2.75, .1, 3.5), .6, vec3(0, 1, .2)),
    CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(1.,1.,1.), 0.25),
    ]
'''

class MainWindow(QLabel):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.label = QLabel(self)
        
        _, self.scene, self.camera0, self.light0 = generate_scene()
        self.initUI()
        
    def initUI(self):      
        
        self.setWindowTitle("Giraffe")
        rgb = render(size, self.scene, self.camera0, self.light0)
        self.setPixmap(array2qpixmap(rgb))
        self.resize(width, height)

        # render time
        self.label.setGeometry(width - 100, height - 100, 250, 150)
        self.label.setStyleSheet("QLabel {color:yellow;}")
        self.label.show()

        self.show()
    
    def _render(self):
        timer = TicToc()
        rgb = render(size, self.scene, self.camera0, self.light0)
        self.setPixmap(array2qpixmap(rgb))
        self.label.setText(str(timer.now) + "s")
        return self.scene, self.light0, self.camera0
        
    def keyPressEvent(self, e):
        
        # TODO any other way to do this elegantly?
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        if e.key() == QtCore.Qt.Key.Key_W:
            self.camera0.position.z += .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_S:
            self.camera0.position.z -= .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_Left:
            self.camera0.position.x -= .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_Right:
            self.camera0.position.x += .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_Up:
            self.camera0.position.y += .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_Down:
            self.camera0.position.y -= .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_J:
            self.light0.intensity -= .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_K:
            self.light0.intensity += .25
            self._render()
        if e.key() == QtCore.Qt.Key.Key_G:
            _, self.scene, self.camera0, self.light0 = generate_scene()
            self._render()
        

lab = MainWindow()

# sys.exit(gui_app.exec_()) TODO check the difference
gui_app.exec_()


'''
TODO 
- create dataset
- neural raytracer
- train
- test

'''