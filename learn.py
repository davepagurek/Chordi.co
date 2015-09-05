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
hidden1 = SigmoidLayer(25)
hidden2 = SigmoidLayer(5)

#add the layers
net.addInputModule(inLayer)
net.addOutputModule(outLayer)
net.addModule(hidden1)
net.addModule(hidden2)

#create the connection
in_h1 = FullConnection(inLayer,hidden1)
h1_h2 = FullConnection(hidden1, hidden2)
h2_out = FullConnection(hidden2, outLayer)
b_h1  = FullConnection(bias, hidden1)
b_h2  = FullConnection(bias, hidden2)

#add the connection
net.addConnection(in_h1)
net.addConnection(h1_h2)
net.addConnection(h2_out)
net.addConnection(b_h1)
net.addConnection(b_h2)

net.sortModules()

#trainer to edit the network
trainer = BackpropTrainer(net, ds, learningrate = 0.003)

trainer.trainEpochs(25)
#generate a song given an input sequence
def getSong(inputSequence):
    inputSequence = [x for x in inputSequence]
    song = [str(inputSequence[x])  for x in range(0, static.NUM_OF_INPUTS)]
    nextout = 0
    for x in range(0, 64):
        nextout = int(net.activate(tuple(inputSequence)))

        # just to shake it up a little if we get 4 of the same chord in a row
        if nextout == inputSequence[-1] and nextout == inputSequence[-2] and nextout == inputSequence[-3]:
            recurring = dict()
            for i in song:
                if i in recurring:
                    recurring[i] += 1
                else:
                    recurring[i] = 1

            nextout = int(min(recurring, key = recurring.get))

        song.append(str(nextout))
        inputSequence = inputSequence[1:]
        inputSequence.append(nextout)

    print song[4:]
    f = open('output.txt', 'w')
    f.write(' '.join(song[4:]))
    f.close()

getSong([7, 9, 7, 9])
