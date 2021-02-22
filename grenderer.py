'''
grenderer.py
'''

import numpy as np
import random
from gutils import TicToc
from gmath import vec3
from gprimitives import raytrace
from tqdm import tqdm
from functools import partial
from PIL import Image
import os

import multiprocessing


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


def render_single_frame(index, animations, path):
    for idx, sphere in enumerate(global_scene[1:]):
        sphere.c.y = animations[idx][index]
    rgb = render(global_scene, global_camera, global_light, global_size)
    #     rgbs.append(rgb)
    # return index
    rgb_img = Image.fromarray(rgb)
    rgb_path = os.path.join(path, '0_' + str(index) + '.png')
    rgb_img.save(rgb_path)
    return rgb


def animate(scene, camera, light, size, spheres, path):
    '''
    Parameters: size, scene, camera, light
    Returns: a sequence of images
    '''
    # multiprocessing
    global global_camera
    global global_scene
    global global_light
    global global_size
    
    global_camera = camera
    global_scene = scene
    global_light = light
    global_size = size
    
    pool = multiprocessing.Pool()

    sphere_y_animations = []

    seq_length = 30
    offset = 0.05

    # rgbs = []
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
    
    # print(sphere_y_animations)


    pool_fn = partial(render_single_frame, animations=sphere_y_animations, path=path)
    

    rgbs = pool.map(pool_fn, range(seq_length * 2 - 1))

    # print(rgbs)
    
    # for i in tqdm(range(seq_length * 2 - 1)):
    #     _scene = scene
    #     for index, sphere in enumerate(_scene[1:]):
    #         sphere.c.y = sphere_y_animations[index][i]
    #     rgb = render(_scene, camera, light, size)
    #     rgbs.append(rgb)

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