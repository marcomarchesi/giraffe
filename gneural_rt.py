'''
gneural_rt.py
'''

import torch
from torch import nn
from torch.utils.data import random_split
from torchvision import transforms
from torch.autograd import Variable
import torchvision
from giraffe import Giraffe, show_build
from gdataset import load_dataset, RayTracingDataset
from gmodel import RayTracingDecoder
from argparse import ArgumentParser
import numpy as np


parser = ArgumentParser()
parser.add_argument('--dataset-path', default='data/dataset.hdf5')
parser.add_argument('--split-factor', default=0.8)
args = parser.parse_args()


app = Giraffe()
show_build(app)

# load the dataset
scenes, rgb = load_dataset(args.dataset_path)

img_transform = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Normalize([0.5], [0.5])
])

rt_dataset = RayTracingDataset(scenes=scenes, renders=rgb, transform=img_transform)
print("Dataset length is {}.".format(len(rt_dataset)))

dataset_split_size = [int(len(rt_dataset) * args.split_factor), 
                        len(rt_dataset) - int(len(rt_dataset) * args.split_factor)]



# split the dataset into train and test
train_dataset, test_dataset = random_split(rt_dataset, dataset_split_size)

batch_size = 128
train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=batch_size, shuffle=False, num_workers=4
)


num_epochs = 100
batch_size = 128
learning_rate = 1e-3
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RayTracingDecoder().to(device).double()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(
    model.parameters(), lr=learning_rate, 
    weight_decay=1e-5
)

# def to_img(x):
#     x = 0.5 * (x + 1)
#     x = x.clamp(0, 1)
#     x = x.view(x.size(0), 1, , 28)
#     return x

for epoch in range(num_epochs):
    for data in train_loader:

        
        render = np.reshape(data['render'], (batch_size, 256 * 256 * 3))

        # render = render.view(render.size(0), -1)
        # render = Variable(render).to(device)
        output = model(data['scene'])
        
        loss = criterion(output, render)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print('epoch [{}/{}], loss:{:.4f}'
    .format(epoch+1, num_epochs, loss.data[0]))
    if epoch % 10 == 0:
        img = output.cpu().data
        print(img)

torch.save(model.state_dict(), 'checkpoint.pth')


