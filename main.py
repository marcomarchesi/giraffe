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


from argparse import ArgumentParser
from giraffe import show_logo, Giraffe
from gmath import vec3
from gprimitives import Light, Camera, Sphere, CheckeredSphere
from grenderer import render, preview

from gutils import TicToc

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=800)
parser.add_argument('--image-height', default=400)
parser.add_argument('--focal-length', default=0.5)
args = parser.parse_args()


# size of the image to render
(width, height) = (args.image_width, args.image_height)

# start with this
# increment the build number
app = Giraffe()
show_logo(app.build, app.version)

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

'''
format of each scene:
camera: [px,py,pz,f]
light: [px,py,pz,i]
sphere: [px,py,pz, r, cr,cg,cb, rf]
rt_array: (w,h,3)
'''
def generate_scene():
    cam_x = random.uniform(-5.,5.)
    cam_y = random.uniform(-.1, 5.)
    cam_z = random.uniform(-5.,0.)
    f = random.uniform(0.35, 0.7)
    lx = random.uniform(-5.,5.)
    ly = random.uniform(1.,15.)
    lz = random.uniform(-5.,5.)
    i = random.uniform(0.6,1.2)
    radius = [random.uniform(0.1,2.) for _ in range(3)]
    xs = [random.uniform(-5.,5.) for _ in range(3)]
    ys = [random.uniform(.1, 3.) for _ in range(3)]
    zs = [random.uniform(0.1,5.) for _ in range(3)]
    cs = [random.uniform(0.0, 1.0) for _ in range(9)]

    camera = Camera(vec3(cam_x, cam_y, cam_z), f)
    light = Light(vec3(lx, ly, lz), i)
    scene = [
        Sphere(vec3(xs[0], ys[0], zs[0]), radius[0], vec3(cs[0], cs[1], cs[2])),
        Sphere(vec3(xs[1], ys[1], zs[1]), radius[1], vec3(cs[3], cs[4], cs[5])),
        Sphere(vec3(xs[2], ys[2], zs[2]), radius[2], vec3(cs[6], cs[7], cs[8])),
        CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(1.,1.,1.), 0.25),
    ]
    return scene, camera, light


size = (width, height)


class MainWindow(QLabel):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.label = QLabel(self)
        
        self.scene, self.camera0, self.light0 = generate_scene()
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
        # print([s.c for s in self.scene])
        # print(self.camera0.position)
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
            self.scene, self.camera0, self.light0 = generate_scene()
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