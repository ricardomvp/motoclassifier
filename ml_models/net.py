#Torch libraries
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#Create Net
class Net(nn.Module):
    def __init__(self, num_channels):
        super(Net,self).__init__()

        self.num_channels = num_channels

        self.conv1 = nn.Conv2d(3, self.num_channels, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(self.num_channels)
        self.conv2 = nn.Conv2d(self.num_channels, self.num_channels*2, 3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(self.num_channels*2)
        self.conv3 = nn.Conv2d(self.num_channels*2, self.num_channels*4, 3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(self.num_channels*4)

        #full conected
        self.fc1 =  nn.Linear(self.num_channels*4*4*4*4, self.num_channels*4)
        self.fcbn1 =  nn.BatchNorm1d(self.num_channels*4)
        self.fc2 =  nn.Linear(self.num_channels*4, 10)

    def forward(self, x):
            x = self.bn1(self.conv1(x)) #num_channelsx64x64
            x = F.relu(F.max_pool2d(x, 2)) #num_channelsx32x32
            x = self.bn2(self.conv2(x)) #num_channels*2x32x32
            x = F.relu(F.max_pool2d(x, 2)) #num_channels*2x16x16
            x = self.bn3(self.conv3(x)) #num_channels*4x16x16
            x = F.relu(F.max_pool2d(x, 2)) #num_channels*4x8x8
            #flatten
            x = x.view(-1, self.num_channels*4*4*4*4)
            # fc
            x = self.fc1(x)
            x = self.fcbn1(x)
            x = F.relu(x)
            x = F.dropout(x, p=0.8, training=True)
            x = self.fc2(x)
            #log_softmax
            x = F.log_softmax(x, dim=1)
            return x
