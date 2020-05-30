'''
gdataset.py
'''

import random
import numpy as np
from gmath import vec3
from gprimitives import Light, Camera, Sphere, CheckeredSphere
from grenderer import render, preview
from argparse import ArgumentParser
import h5py
from tqdm import tqdm
from PIL import Image
from giraffe import Giraffe, todo, timer

import torch
from torch.utils.data import Dataset

# app = Giraffe()

parser = ArgumentParser()
parser.add_argument('--image-width', default=256)
parser.add_argument('--image-height', default=256)
parser.add_argument('--focal-length', default=1.0)
args = parser.parse_args()


# size of the image to render
(width, height) = (args.image_width, args.image_height)
size = (width, height)  # ???

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
    data = [cam_x, cam_y, cam_z, f, lx, ly, lz, i,
            xs[0], ys[0], zs[0], radius[0], cs[0], cs[1], cs[2],
            xs[1], ys[1], zs[1], radius[1], cs[3], cs[4], cs[5],
            xs[2], ys[2], zs[2], radius[2], cs[6], cs[7], cs[8]
    ]
    return data, scene, camera, light

@timer
def generate_dataset():

    with h5py.File("dataset.hdf5", "w") as f:
        data_array = []
        rgb_array = []
        for _ in tqdm(range(50)):
            data, scene, camera, light = generate_scene()
            rgb = render(size, scene, camera, light)
            data_array.append(data)
            rgb_array.append(rgb)
        f.create_dataset("scenes", data=data_array, compression='gzip', compression_opts=9)
        f.create_dataset("renders", data=rgb_array, compression='gzip', compression_opts=9)

def load_scene(s):
    camera = Camera(vec3(s[0], s[1], s[2]), s[3])
    light = Light(vec3(s[4], s[5], s[6]), s[7])
    scene = [
        Sphere(vec3(s[8], s[9], s[10]), s[11], vec3(s[12], s[13], s[14])),
        Sphere(vec3(s[15], s[16], s[17]), s[18], vec3(s[19], s[20], s[21])),
        Sphere(vec3(s[22], s[23], s[24]), s[25], vec3(s[26], s[27], s[28])),
        CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(1.,1.,1.), 0.25),
    ]

# TODO merge with the class RayTracingDataset
def load_dataset(path):
    with h5py.File(path, "r") as f:
        rgb = np.array(f["renders"])
        scenes = np.array(f["scenes"])
        # print(scenes[0])
        # for img in rgb:
        #     im = Image.fromarray(img)
        #     im.show()
        return scenes, rgb

class RayTracingDataset(Dataset):

    def __init__(self, scenes, renders, transform=None):
        '''
        Args:
            scenes (Numpy array)
            renders (Numpy array)
            transform (callable, optional)
        '''
        self.scenes = scenes
        self.renders = renders
        self.transform = transform
    
    def __len__(self):
        return len(self.scenes)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        sample = {'scene': self.scenes[idx],
                  'render': self.renders[idx]}

        return sample


if __name__ == "__main__":
    # pass
    generate_dataset()
    # load_dataset()
    