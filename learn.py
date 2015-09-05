from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets import SupervisedDataSet
from songfactory import SongFactory
from model import SongModel

from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.structure.modules import BiasUnit
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

import random
import pdb
import static

n = FeedForwardNetwork()

dataModel = SongFactory().getModels()

ds = SupervisedDataSet(static.NUM_OF_INPUTS, 1)

#adds samples from the data received from songfactory and the k
for data in dataModel:
    for input, target in data.model:
        print input, target
        ds.addSample(input, target)


#instantiate the network
net = FeedForwardNetwork()
bias = BiasUnit()
net.addModule(bias)

#create the layers of the network
inLayer = LinearLayer(static.NUM_OF_INPUTS)
outLayer = LinearLayer(1)
hidden1 = SigmoidLayer(6)

#add the layers
net.addInputModule(inLayer)
net.addOutputModule(outLayer)
net.addModule(hidden1)

#create the connection
in_h1 = FullConnection(inLayer,hidden1)
h1_out = FullConnection(hidden1, outLayer)
b_h1  = FullConnection(bias, hidden1)

#add the connection
net.addConnection(in_h1);
net.addConnection(h1_out)
net.addConnection(b_h1)

net.sortModules()

#trainer to edit the network
trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)

trainer.trainEpochs(100)
#generate a song given an input sequence
def getSong(inputSequence):
    inputSequence = [x for x in inputSequence]
    song = [str(inputSequence[x])  for x in range(0,static.NUM_OF_INPUTS)]
    nextout = 0
    for x in range(0,128):
        nextout = int(net.activate(tuple(inputSequence)))
        song.append(str(nextout))
        inputSequence = inputSequence[1:]
        inputSequence.append(nextout)

    print song
    f = open('output.txt', 'w')
    f.write(' '.join(song))
    f.close()

getSong([4,2,4,5,7,3,5,4])
