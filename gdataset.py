'''
gdataset.py
'''

import random
import numpy as np
from gmath import vec3
from gprimitives import Light, Camera, Sphere, CheckeredSphere, Plane
from grenderer import render, preview, animate
from argparse import ArgumentParser
import h5py
from tqdm import tqdm
from PIL import Image
from giraffe import Giraffe
from gdesign_patterns import TODO, timer
import os
import pickle

import torch
from torch.utils.data import Dataset

# app = Giraffe()

parser = ArgumentParser()
parser.add_argument('--path', default='data/art/images_1102')
parser.add_argument('--data-path', default='data/images_100.pkl')
parser.add_argument('--size', default=128)
parser.add_argument('--focal-length', default=1.0)
parser.add_argument('--spheres', default=10)
args = parser.parse_args()


# size of the image to render
# (width, height) = (args.image_width, args.image_height)
size = args.size

'''
format of each scene:
camera: [px,py,pz,f]
light: [px,py,pz,i]
sphere: [px,py,pz, r, cr,cg,cb, rf]
rt_array: (w,h,3)
'''

def generate_scene(spheres=10):

    Y = 5.0
    X = 5.0
    Z = 5.0
    I = 2.0
    R = 3.0


    cam_x = 0.
    cam_y = 1.
    cam_z = 0.5
    f = 0.5
    lx = -4.
    ly = 5.
    lz = -4.

    i = random.uniform(0.6,1.1)
    radius = [random.uniform(.1,.5) for _ in range(spheres)]
    xs = [random.uniform(-8,8) for _ in range(spheres)]
    ys = [random.uniform(-0.5, 6) for _ in range(spheres)]
    zs = [random.uniform(.5,10.) for _ in range(spheres)]
    cs = [random.uniform(0.0, 1.0) for _ in range(spheres * 3)]

    camera = Camera(vec3(cam_x, cam_y, cam_z), f)
    light = Light(vec3(lx, ly, lz), i)
    scene = [
        Sphere(vec3(0,-99999.5, 0), 99999, vec3(1.,1.,1.), 0.1)
    ]


    # data are sort of normalized now
    data = [cam_x, cam_y, cam_z, f, lx/X, ly/Y, lz/Z, i/I]
    for i in range(spheres):
        scene.append(Sphere(vec3(xs[i], ys[i], zs[i]), radius[i], vec3(cs[3 * i], cs[(3 * i) + 1], cs[(3 * i) + 2])))
        data.extend([xs[i]/X, ys[i]/Y, zs[i]/Z, radius[i]/R, cs[3 * i], cs[(3 * i) + 1], cs[(3 * i) + 2]])
    
    return data, scene, camera, light

@timer
def save_dataset(data_path, scene, camera, light, size, spheres):

    rgb_array = []

    index = 0
    # scene, camera, light = generate_scene()
    # rgb = render(size, scene, camera, light)
    rgbs = animate(scene, camera, light, size, spheres)
    # print(rgb.shape)
    frame = 0
    for rgb in rgbs:
        rgb_img = Image.fromarray(rgb)
        rgb_path = os.path.join(args.path, str(index) + '_' + str(frame) + '.png')
        rgb_img.save(rgb_path)
        # rgb_array.append(data)
        frame += 1
    img_path = os.path.join(args.path, "")
    os.system("ffmpeg -r 30 -i {}%01d.png -vcodec libx264 -pix_fmt yuv420p -crf 1 -y {}.mp4".format(os.path.join(args.path, str(index) + "_"), os.path.join(args.path, str(index))))

def load_data(data_path):

    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        print(len(data[0]))

@TODO("deprecated")
def load_scene(s):
    camera = Camera(vec3(s[0], s[1], s[2]), s[3])
    light = Light(vec3(s[4], s[5], s[6]), s[7])
    scene = [
        Sphere(vec3(s[8], s[9], s[10]), s[11], vec3(s[12], s[13], s[14])),
        Sphere(vec3(s[15], s[16], s[17]), s[18], vec3(s[19], s[20], s[21])),
        Sphere(vec3(s[22], s[23], s[24]), s[25], vec3(s[26], s[27], s[28])),
        CheckeredSphere(vec3(0,-99999.5, 0), 99999, vec3(1.,1.,1.), 0.25),
    ]

@TODO("to merge with the model")
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
    # generate_dataset(args.size)
    _, scene, camera0, light0 = generate_scene(args.spheres)
    save_dataset('data/art/images', scene, camera0, light0, args.size, args.spheres)
    # load_data(args.data_path)
    # load_dataset()
    