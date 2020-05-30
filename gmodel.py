'''
gmodel.py
'''

import torch
from torch import nn

class RayTracingDecoder(nn.Module):
    def __init__(self):
        super(RayTracingDecoder, self).__init__()
        self.decoder = nn.Sequential(
            nn.Linear(29, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True),
            nn.Linear(128, 1024),
            nn.ReLU(True),
            nn.Linear(1024, 256 * 256 * 3),
            nn.Tanh()
        )
    def forward(self, x):
        x = self.decoder(x)
        return x