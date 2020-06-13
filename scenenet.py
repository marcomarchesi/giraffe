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
import zipfile

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

    with h5py.File("scenenet.hdf5", "w") as f:
        data_array = []
        counter = 0
        for file in tqdm(os.listdir(path)):
            img = Image.open(os.path.join(path, file))
            img_resized = img.resize((128,128))
            data = np.asarray(img_resized, dtype=np.uint8)
            data_array.append(data)
            counter +=1
            if counter == dataset_size:
                print('done')
                f.create_dataset("images", data=data_array, compression='gzip', compression_opts=9)
                break
        

def zip_images(path, size=1000):
    with zipfile.ZipFile('dataworld.zip', 'w') as myzip:
        for index, file in enumerate(os.listdir(path)):
            if index < size:
                filename = os.path.join(path, file)
                print(filename)
                myzip.write(filename)
            else:
                print('done')
                exit()

def copy_images(path, dst, size=1000):
    for index, file in enumerate(os.listdir(path)):
        if index < size:
            input_filename = os.path.join(path, file)
            output_filename = os.path.join(dst, file)
            copyfile(input_filename, output_filename)
        else:
            print('done')
            break


if __name__ == "__main__":
    # zip_images(args.path)
    # copy_images(args.path, args.dst)
    # get_images(args.path, args.dst)
    generate_dataset(args.path, 10000)