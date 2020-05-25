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
from multiprocessing import Process


from argparse import ArgumentParser
from giraffe import show_logo, Giraffe
from gmath import vec3, extract, FARAWAY
from gutils import TicToc
from gprimitives import Light, Camera

'''
Arguments
'''

parser = ArgumentParser()
parser.add_argument('--image-width', default=400)
parser.add_argument('--image-height', default=300)
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


class Primitive:
    def __init__(self, diffuse, reflection = 0.5):
        self.diffuse = diffuse
        self.reflection = reflection
    
    def diffusecolor(self, M):
        return self.diffuse

    def light(self, O, D, d, scene, light, camera, bounce):
        M = (O + D * d)                         # intersection point
        N = (M - self.c) * (1. / self.r)        # normal

        toL = (light - M).norm()                    # direction to light
        toO = (camera - M).norm()                    # direction to ray origin
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
            color += raytrace(nudged, rayD, scene, light, camera, bounce + 1) * self.reflection

        # Blinn-Phong shading (specular)
        phong = N.dot((toL + toO).norm())
        color += vec3(1, 1, 1) * np.power(np.clip(phong, 0, 1), 50) * seelight
        return color


class Sphere (Primitive):
    def __init__(self, center, r, diffuse, reflection = 0.5):
        super().__init__(diffuse, reflection = 0.5)
        self.c = center
        self.r = r

    def intersect(self, O, D):
        b = 2 * D.dot(O - self.c)
        c = abs(self.c) + abs(O) - 2 * self.c.dot(O) - (self.r * self.r)
        disc = (b ** 2) - (4 * c) # 2nd grade equation to solve for the sphere
        sq = np.sqrt(np.maximum(0, disc))
        h0 = (-b - sq) / 2
        h1 = (-b + sq) / 2
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        pred = (disc > 0) & (h > 0)
        return np.where(pred, h, FARAWAY)



class CheckeredSphere(Sphere):
    def diffusecolor(self, M):
        checker = ((M.x * 2).astype(int) % 2) == ((M.z * 2).astype(int) % 2)
        return self.diffuse * checker




def raytrace(O, D, scene, light, camera, bounce = 0):
    '''
    O is the camera position == the ray origin
    D is the normalized ray direction
    scene is a list of Sphere objects (see below)
    bounce is the number of the bounce, starting at zero for camera rays
    '''

    # select all the points where the objects intersect ray directions
    distances = [s.intersect(O, D) for s in scene]
    nearest = reduce(np.minimum, distances)

    # start with complete dark
    color = vec3(0, 0, 0)

    # print(color.components())

    for (s, d) in zip(scene, distances):
        hit = (nearest != FARAWAY) & (d == nearest)
        if np.any(hit):
            dc = extract(hit, d)
            Oc = O.extract(hit)
            Dc = D.extract(hit)
            cc = s.light(Oc, Dc, dc, scene, light, camera, bounce)
            color += cc.place(hit)
        
    return color

# Point light position
light0 = Light(vec3(5, 5, -1), 1.0)
# Camera position       
camera0 = Camera(vec3(0, 0.3, -1))
# objects in the scene
scene = [
    Sphere(vec3(.75, .1, 1), .6, vec3(0, 0, 1)),
    Sphere(vec3(-.75, .1, 2.25), .6, vec3(.5, .223, .5)),
    Sphere(vec3(-2.75, .1, 3.5), .6, vec3(1, .572, .184)),
    CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(.75, .75, .75), 0.25),
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
color = raytrace(camera0.position, (Q - camera0.position).norm(), scene, light0.position, camera0.position)

# convert into a numpy array [w,h,c]
rgb = np.stack([(255 * np.clip(c, 0, 1).reshape((h, w))).astype(np.uint8) for c in color.components()], axis=2)

lab = QLabel()
lab.setWindowTitle("Giraffe")
lab.setPixmap(array2qpixmap(rgb))
lab.show()
lab.resize(w, h)

# stop tracking rendering time
print("Rendered in {}s.".format(timer.now))


# sys.exit(gui_app.exec_()) TODO check the difference
gui_app.exec_()


'''
TODO 
2. instance lights, cameras, objects
2b. generalize to multiple lights
4. import obj assets (we start with triangles-ray intersection)
'''