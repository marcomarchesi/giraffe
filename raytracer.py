'''
Giraffe
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
from logo import show_logo
from gmath import vec3, extract, FARAWAY
# from gprimitives import Sphere, CheckeredSphere

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=1600)
parser.add_argument('--image-height', default=800)
args = parser.parse_args()

# start with this
show_logo()

# size of the image to render
(w, h) = (args.image_width, args.image_height)



class Camera:
    def __init__(self, position):
        self.position = position

class Light:
    def __init__(self, position, intensity):
        self.position = position


# Point light position
light0 = Light(vec3(5, 5, -1), 1.0)
# Camera position       
camera0 = Camera(vec3(0, 0.3, -1))

class Primitive:
    pass

class Sphere (Primitive):
    def __init__(self, center, r, diffuse, mirror = 0.5):
        self.c = center
        self.r = r
        self.diffuse = diffuse
        self.mirror = mirror

    def intersect(self, O, D):
        b = 2 * D.dot(O - self.c)
        c = abs(self.c) + abs(O) - 2 * self.c.dot(O) - (self.r * self.r)
        disc = (b ** 2) - (4 * c)
        sq = np.sqrt(np.maximum(0, disc))
        h0 = (-b - sq) / 2
        h1 = (-b + sq) / 2
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        pred = (disc > 0) & (h > 0)
        return np.where(pred, h, FARAWAY)

    def diffusecolor(self, M):
        return self.diffuse

    def light(self, O, D, d, scene, bounce):
        M = (O + D * d)                         # intersection point
        N = (M - self.c) * (1. / self.r)        # normal

        toL = (light0.position - M).norm()                    # direction to light
        toO = (camera0.position - M).norm()                    # direction to ray origin
        nudged = M + N * .0001                  # M nudged to avoid itself

        # Shadow: find if the point is shadowed or not.
        # This amounts to finding out if M can see the light
        light_distances = [s.intersect(nudged, toL) for s in scene]
        light_nearest = reduce(np.minimum, light_distances)
        seelight = light_distances[scene.index(self)] == light_nearest

        # Ambient
        color = vec3(0.05, 0.05, 0.05)

        # Lambert shading (diffuse)
        lv = np.maximum(N.dot(toL), 0)
        color += self.diffusecolor(M) * lv * seelight

        # Reflection
        if bounce < 5:
            rayD = (D - N * 2 * D.dot(N)).norm()
            color += raytrace(nudged, rayD, scene, bounce + 1) * self.mirror

        # Blinn-Phong shading (specular)
        phong = N.dot((toL + toO).norm())
        color += vec3(1, 1, 1) * np.power(np.clip(phong, 0, 1), 50) * seelight
        return color

class CheckeredSphere(Sphere):
    def diffusecolor(self, M):
        checker = ((M.x * 2).astype(int) % 2) == ((M.z * 2).astype(int) % 2)
        return self.diffuse * checker

def raytrace(O, D, scene, bounce = 0):

    # O is the ray origin, D is the normalized ray direction
    # scene is a list of Sphere objects (see below)
    # bounce is the number of the bounce, starting at zero for camera rays

    distances = [s.intersect(O, D) for s in scene]
    nearest = reduce(np.minimum, distances)
    color = vec3(0, 0, 0)

    for (s, d) in zip(scene, distances):
        hit = (nearest != FARAWAY) & (d == nearest)
        if np.any(hit):
            dc = extract(hit, d)
            Oc = O.extract(hit)
            Dc = D.extract(hit)
            cc = s.light(Oc, Dc, dc, scene, bounce)
            color += cc.place(hit)
        
    return color




scene = [
    Sphere(vec3(.75, .1, 1), .6, vec3(0, 0, 1)),
    Sphere(vec3(-.75, .1, 2.25), .6, vec3(.5, .223, .5)),
    Sphere(vec3(-2.75, .1, 3.5), .6, vec3(1, .572, .184)),
    CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(.75, .75, .75), 0.25),
    ]

r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1, 1 / r + .25, 1, -1 / r + .25)
x = np.tile(np.linspace(S[0], S[2], w), h)
y = np.repeat(np.linspace(S[1], S[3], h), w)

t0 = time.time()
Q = vec3(x, y, 0)
color = raytrace(camera0.position, (Q - camera0.position).norm(), scene)
print ("Took", time.time() - t0)

rgb = [Image.fromarray((255 * np.clip(c, 0, 1).reshape((h, w))).astype(np.uint8), "L") for c in color.components()]



# Visualisation on PySide
app = QApplication(sys.argv)


GRAY_COLORTABLE = []
for i in range(256):
    GRAY_COLORTABLE.append(QtGui.qRgb(i, i, i))


def array2qpixmap(img_array):
    height, width = img_array.shape
    bytesPerLine, _ = img_array.strides
    image = QtGui.QImage(
        img_array.data.tobytes(),
        width,
        height,
        bytesPerLine,
        QtGui.QImage.Format_Indexed8,
    )
    image.setColorTable(GRAY_COLORTABLE)
    return QtGui.QPixmap.fromImage(image)


# bytesPerLine, _, _ = img.strides
# qi = QtGui.QImage(img, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB32)
# # # convert it to a QPixmap for display:
# qp = QtGui.QPixmap.fromImage(qi)

img_array = np.zeros((w,h), dtype=np.uint8)
img_array[:, :] = 127

lab = QLabel()
# lab.resize(w, h)
lab.setWindowTitle("Hello Marco")
lab.setPixmap(array2qpixmap(img_array.copy()))
lab.show()

# img = Image.merge("RGB", rgb)
# img.show()

sys.exit(app.exec_())


'''
TODO 
2. instance lights, cameras, objects
2b. generalize to multiple
3. render on pyside
'''