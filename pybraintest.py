from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets import SupervisedDataSet

dataModel = [
    [(0,0,0), (0,)],
    [(0,0,1), (0,)],
    [(0,1,0), (0,)],
    #[(0,1,1), (0,)],
    #[(1,0,0), (0,)],
    #[(1,1,0), (0,)],
    [(1,0,1), (0,)],
    [(1,1,1), (1,)],
]

ds = SupervisedDataSet(3, 1)
for input, target in dataModel:
         ds.addSample(input, target)

import random
random.seed()
trainingSet = SupervisedDataSet(3, 1);
for ri in range(0,1000):
    input,target = dataModel[random.getrandbits(2)];
    trainingSet.addSample(input, target)

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(3, 10, 1, bias=True)

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)

trainer.trainEpochs(1000)

for x in dataModel:
    print x[0],"-->",round(net.activate(x[0]))
