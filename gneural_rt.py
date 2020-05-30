'''
gneural_rt.py
'''

import torch
from torch.utils.data import random_split
import torchvision
from giraffe import Giraffe, show_build
from gdataset import load_dataset, RayTracingDataset
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--dataset-path', default='data/dataset.hdf5')
parser.add_argument('--split-factor', default=0.8)
args = parser.parse_args()


app = Giraffe()
show_build(app)

# load the dataset
scenes, rgb = load_dataset(args.dataset_path)

rt_dataset = RayTracingDataset(scenes=scenes, renders=rgb)
print("Dataset length is {}.".format(len(rt_dataset)))

dataset_split_size = [int(len(rt_dataset) * args.split_factor), 
                        len(rt_dataset) - int(len(rt_dataset) * args.split_factor)]

# split the dataset into train and test
train_dataset, test_dataset = random_split(rt_dataset, dataset_split_size)

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True, num_workers=4, pin_memory=True
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=32, shuffle=False, num_workers=4
)


