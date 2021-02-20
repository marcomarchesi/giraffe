'''
grenderer.py
'''

import numpy as np
import random
from gutils import TicToc
from gmath import vec3
from gprimitives import raytrace

def render(scene, camera, light, size=128):

    w = size
    h = size
    # aspect ratio
    r = float(w) / h
    # Screen coordinates: x0, y0, x1, y1.
    S = (-1, 1 / r + .25, 1, -1 / r + .25)
    x = np.tile(np.linspace(S[0], S[2], w), h)
    y = np.repeat(np.linspace(S[1], S[3], h), w)

    # start tracking rendering time
    timer = TicToc()
    # all the points in the viewport
    Q = vec3(camera.position.x + x, camera.position.y + y, camera.position.z + camera.focal_length)

    # let's raytrace!
    color = raytrace(camera.position, 
                    (Q - camera.position).norm(), 
                    scene, 
                    light, 
                    camera)

    # convert into a numpy array [w,h,c]
    rgb = np.stack([(255 * np.clip(c, 0, 1).reshape((h, w))).astype(np.uint8) for c in color.components()], axis=2)

    # stop tracking rendering time
    # print("Rendered in {}s.".format(timer.now))

    return rgb

def animate(size, scene, camera, light):
    '''
    Parameters: size, scene, camera, light
    Returns: a sequence of images
    '''
    seq_length = 30
    offset = 0.05
    sphere_y_animations = []
    rgbs = []
    direction = random.randint(0,1)
    for sphere in scene[1:]:
        offset_randomness = random.uniform(0.3, 1.5)
        # print(offset_randomness)
        sphere_y_anim = []
        if direction == 0:
            sphere_y_anim = list(np.linspace(sphere.c.y - offset * offset_randomness,sphere.c.y + offset * offset_randomness, seq_length))
            sphere_y_anim.extend(reversed(sphere_y_anim[:-1]))
            direction = 1
        else:
            sphere_y_anim = list(np.linspace(sphere.c.y + offset * offset_randomness,sphere.c.y - offset * offset_randomness, seq_length))
            sphere_y_anim.extend(reversed(sphere_y_anim[:-1]))
            direction = 0
        sphere_y_animations.append(sphere_y_anim)
        # print(len(sphere_y_anim))
    
    for i in range(seq_length * 2 - 1):
        _scene = scene
        for index, sphere in enumerate(_scene[1:]):
            sphere.c.y = sphere_y_animations[index][i]
        rgb = render(_scene, camera, light, size=512)
        rgbs.append(rgb)

    return rgbs

def preview(rgb,factor=20):
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