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


from argparse import ArgumentParser
from giraffe import show_logo, Giraffe
from gmath import vec3
from gprimitives import Light, Camera, Sphere, CheckeredSphere, Plane, Disc
from grenderer import render, preview

from gutils import TicToc

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=800)
parser.add_argument('--image-height', default=400)
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




# Point light position
light0 = Light(vec3(5, 5, 3), 1.0)
# Camera position       
camera0 = Camera(vec3(0, 0.3, -1))
# objects in the scene
scene = [
    Sphere(vec3(.75, .1, 1), .6, vec3(0, 0, 1)),
    Sphere(vec3(-.75, .1, 2.25), .6, vec3(.5, .223, .5)),
    Sphere(vec3(-2.75, .1, 3.5), .6, vec3(1, .572, .184)),
    CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(.75, .75, .75), 0.25),
    # Plane(vec3(.75,.1, 5), vec3(1,0,1), vec3(1.,0.,1.), reflection=0.0)  # Point Normal DiffuseColor
    Disc(vec3(0,0.5, 0), vec3(0,1,0), 1.0, vec3(0.,1.,0.), reflection=0.0)  # Point Normal DiffuseColor
    ]


def preview(rgb,factor=10):
    height, width, channels = rgb.shape
    height *= factor
    width *= factor
    zoomed_rgb = np.zeros((height, width, channels), dtype=np.uint8)
    for c in range(channels):
        for i in range(width):
            for j in range(height):
                ii = int(i / factor)
                jj = int(j / factor)
                zoomed_rgb[j,i,c] = rgb[jj, ii, c]
    return zoomed_rgb

factor = 10
size = (width, height)
preview_size = np.divide(size, factor).astype(np.uint8)
rgb = render(preview_size, scene, camera0, light0)

timer = TicToc()
zoomed_rgb = preview(rgb)
print(timer.now)



lab = QLabel()
lab.setWindowTitle("Giraffe")
lab.setPixmap(array2qpixmap(zoomed_rgb))
lab.resize(width, height)
lab.show()




# sys.exit(gui_app.exec_()) TODO check the difference
gui_app.exec_()


'''
TODO 
- realtime preview
- camera interaction (with keys)
- transparency
- refraction
- triangle-ray intersection

'''