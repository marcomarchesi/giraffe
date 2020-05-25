'''
grenderer.py
'''

import numpy as np
from gutils import TicToc
from gmath import vec3
from gprimitives import raytrace

def render(size, scene, camera, light):

    w,h = size
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
    color = raytrace(camera.position, 
                    (Q - camera.position).norm(), 
                    scene, 
                    light.position, 
                    camera.position)

    # convert into a numpy array [w,h,c]
    rgb = np.stack([(255 * np.clip(c, 0, 1).reshape((h, w))).astype(np.uint8) for c in color.components()], axis=2)

    # stop tracking rendering time
    print("Rendered in {}s.".format(timer.now))

    return rgb

def preview(size, factor=10):

    w,h = np.divide(size, factor)    # divide both dimensions by the factor