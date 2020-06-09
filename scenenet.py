'''
scenenet parser
https://robotvault.bitbucket.io/scenenet-rgbd.html
'''

from argparse import ArgumentParser
from giraffe import TODO, timer
import os
from shutil import copyfile
from PIL import Image
import numpy as np
import h5py
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument('--path')
parser.add_argument('--dst')
args = parser.parse_args()

@TODO("add everything")
def get_images(path, dst):
    counter = 0
    for root, folders, _  in os.walk(path):
        if root[-5:] == 'photo':
            for file in os.listdir(root):
                if file[-3:] == 'jpg':
                    dst_filename = str(counter) + ".jpg"
                    copyfile(os.path.join(root, file), os.path.join(dst, dst_filename))
                    counter += 1

@timer
def generate_dataset(path, dataset_size = 2):

    with h5py.File("dataset.hdf5", "w") as f:
        data_array = []
        counter = 0
        for file in tqdm(os.listdir(path)):
            img = Image.open(os.path.join(path, file))
            data = np.asarray(img, dtype=np.uint8)
            data_array.append(data)
            counter +=1
            if counter == dataset_size:
                break
        f.create_dataset("images", data=data_array, compression='gzip', compression_opts=9)





if __name__ == "__main__":
    # get_images(args.path, args.dst)
    generate_dataset(args.path, 300)