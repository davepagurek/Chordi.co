from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets import SupervisedDataSet
from songfactory import SongFactory
from model import SongModel

dataModel = SongFactory().getModels()

ds = SupervisedDataSet(5, 1)
for data in dataModel:
    for input, target in data.model:
        ds.addSample(input, target)

trainingSet = SupervisedDataSet(5, 1);

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(5, 10, 1, bias=True)

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)

trainer.trainEpochs(100)

def getSong(inputSequence):
    song = [inputSequence[x] for x in range(0,5)]
    nextout = 0
    #iterate for 15 notes
    for x in range(0,15):
        nextout = net.activate(inputSequence)
        song.append(nextout)
        inputSequence = tuple([inputSequence[x] for x in range(1,5),nextout])
    return song
