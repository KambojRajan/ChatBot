import torch
import json
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from utilFile import tokenize, steming, bagOfWords
from prototypeModel import NeuralNet

with open('prototypeTrainingData.json', 'r') as traingFile:
    userInputs = json.load(traingFile)

allWords = []
tags = []
inOutcomun = []

for intent in userInputs["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        word = tokenize(pattern)
        # here we used extend and not append because we
        # don't want to create a list of lists
        allWords.extend(word)
        inOutcomun.append((word, tag))

wordsToIgnore = ["?", ".", ",", "!", "'", '"', "#", "@", "%", "&"]

allWords = [steming(word) for word in allWords if word not in wordsToIgnore]
allWords = sorted(set(allWords))
# this is not a compulsury step as tags are themself unique
tags = sorted(set(tags))

inputTrain = []
outputTrain = []
for (patternSent, tag) in inOutcomun:
    bag = bagOfWords(patternSent, allWords)
    inputTrain.append(bag)
    classLables = tags.index(tag)
    outputTrain.append(classLables)
inputTrain = np.array(inputTrain)
outputTrain = np.array(outputTrain)

epochItrations = 1000
batchSize = 8
learningRate = 0.001
midLayerSize = 8  # didden_size
outerLayerSize = len(tags)  # output_size
firstLayerSize = len(allWords)  # input_size

device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')


class ChatDataSet(Dataset):
    def __init__(self):
        self.sampleSize = len(inputTrain)
        self.inputData = inputTrain
        self.outputData = outputTrain

    def __getitem__(self, index):
        return self.inputData[index], self.outputData[index]

    def __len__(self):
        return self.sampleSize


dataset = ChatDataSet()
trainLoader = DataLoader(
    dataset=dataset, batch_size=batchSize, shuffle=True, num_workers=2)

protoType = NeuralNet(firstLayerSize, midLayerSize, outerLayerSize).to(device)

# as we reffered in the other file we here will perform the
# task of loss optimization
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(protoType.parameters(), lr=learningRate)


data = {
    "model_state": protoType.state_dict(),
    "input_size": firstLayerSize,
    "hidden_size":midLayerSize,
    "output_size":outerLayerSize,
    "all_words":allWords,
    "tags":tags
}


if __name__ == "__main__":

    # print(len(allWords))
    # print(len(inputTrain))
    for epoch in range(epochItrations):
        for (words, labels) in trainLoader:
          
            words = words.to(device)
            labels = labels.to(dtype = torch.long).to(device)
            outPut = protoType(words)
            loss = criterion(outPut, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f"epoch {epoch + 1}/{epochItrations},loss = {loss.item():.4f}")


    print(f'final loss: {loss.item():.4f}')
    
    FILE= "data.pth"
    torch.save(data,FILE)

    print(f"training complete file save to {FILE}")

