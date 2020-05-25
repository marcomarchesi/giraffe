'''
Giraffe

Some starting points:
https://github.com/jamesbowman/raytrace/blob/master/rt3.py

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
from gmath import vec3, extract, FARAWAY
from gutils import TicToc
from gprimitives import Light, Camera, Sphere, CheckeredSphere, Plane, Disc, raytrace

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=800)
parser.add_argument('--image-height', default=400)
args = parser.parse_args()


# size of the image to render
(w, h) = (args.image_width, args.image_height)

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

# aspect ratio
r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1, 1 / r + .25, 1, -1 / r + .25)
x = np.tile(np.linspace(S[0], S[2], w), h)
y = np.repeat(np.linspace(S[1], S[3], h), w)

# start tracking rendering time
timer = TicToc()


# all the points in the viewport
Q = vec3(x, y, 0)

# let's raytrace!
color = raytrace(camera0.position, 
                (Q - camera0.position).norm(), 
                scene, 
                light0.position, 
                camera0.position)

# convert into a numpy array [w,h,c]
rgb = np.stack([(255 * np.clip(c, 0, 1).reshape((h, w))).astype(np.uint8) for c in color.components()], axis=2)

lab = QLabel()
lab.setWindowTitle("Giraffe")
lab.setPixmap(array2qpixmap(rgb))
lab.resize(w, h)
lab.show()

# stop tracking rendering time
print("Rendered in {}s.".format(timer.now))


# sys.exit(gui_app.exec_()) TODO check the difference
gui_app.exec_()


'''
TODO 
- camera interaction
- transparency
- refraction
- disc primitive (some sort)

3. triangle-ray intersection
4. cube-ray intersection
'''