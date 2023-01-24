import torch
import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, noClasses):
        super(NeuralNet,self).__init__()
        self.l1 = nn.Linear(inputSize, hiddenSize)
        self.l2 = nn.Linear(hiddenSize, hiddenSize)
        self.l3 = nn.Linear(hiddenSize, noClasses)
        self.relu = nn.ReLU()

    def forward(self, xData):
        # here in this function we will only be passing our data from the
        # three neural net layers, but we will not concider any kind of
        # cross entropy loss that will be managed in the traing file

        out = self.l1(xData)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        return out
