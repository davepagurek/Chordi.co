from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets import SupervisedDataSet

dataModel = [
    [(-1, 0, 0, 0, 0,), (5,)],
    [(0, 0, 0, 0, 5,), (5,)],
    [(0, 0, 0, 5, 5,), (5,)],
    [(0, 0, 5, 5, 5,), (5,)],
    [(0, 5, 5, 5, 5,), (2,)],
    [(5, 5, 5, 5, 2,), (2,)],
    [(5, 5, 5, 2, 2,), (2,)],
    [(5, 5, 2, 2, 2,), (2,)],
    [(5, 2, 2, 2, 2,), (9,)],
    [(2, 2, 2, 2, 9,), (9,)],
    [(2, 2, 2, 9, 9,), (9,)],
    [(2, 2, 9, 9, 9,), (9,)],
    [(2, 9, 9, 9, 9,), (14,)]
]

ds = SupervisedDataSet(5, 1)
for input, target in dataModel:
         ds.addSample(input, target)

trainingSet = SupervisedDataSet(5, 1);

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(5, 10, 1, bias=True)

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)

trainer.trainEpochs(100)

for x in dataModel:
    print x[0],"-->",round(net.activate(x[0]))

def getSong():
    return "midi yay"