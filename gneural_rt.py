'''
gneural_rt.py
'''

import torch
from torch import nn
from torch.utils.data import random_split
from torchvision import transforms
from torch.autograd import Variable
import torchvision
from giraffe import Giraffe, show_build, TODO, timer
from gdataset import load_dataset, RayTracingDataset
from gmodel import autoencoder
from argparse import ArgumentParser
import numpy as np


parser = ArgumentParser()
parser.add_argument('--dataset-path', default='data/dataset_10000.hdf5')
parser.add_argument('--split-factor', default=0.8)
args = parser.parse_args()


app = Giraffe()
show_build(app)

# @TODO("yep!")
# def hello_world(arg1):
#     print("hello" + arg1)
#     return arg1
# phrase = hello_world("world")
# print(phrase)
# exit()

# load the dataset
scenes, rgb = load_dataset(args.dataset_path)



img_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
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

model = autoencoder().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(
    model.parameters(), lr=learning_rate, 
    weight_decay=1e-5
)


for epoch in range(num_epochs):
    for data in train_loader:

        render = data['render'].float()
        scene = data['scene'].float()
        render = render.view(-1, 256*256*3)

        render = Variable(render).to(device)
        scene = Variable(scene).to(device)
        output = model(render)

        loss = criterion(output, render)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print('epoch [{}/{}], loss:{:.4f}'
    .format(epoch+1, num_epochs, loss.data))
    if epoch % 10 == 0:
        img_array = output[0].cpu().data.numpy()
        img = np.reshape(img_array, (256,256,3)).astype(np.uint8)
        image = Image.fromarray(img)
        image.save('{}.png'.format(str(epoch)))
torch.save(model.state_dict(), 'checkpoint.pth')


