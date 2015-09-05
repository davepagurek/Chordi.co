from os import listdir
from model import SongModel
import pdb
class SongFactory:
    def __init__(self):
        files =  listdir("training")
        self.models = []
        for x in files:
            if x != '.DS_Store':
                print("Working on %s" % x)
                tempModel = open("training/"+x,'r')
                self.models.append(SongModel(tempModel.readline()))

    def getModels(self):
        return self.models
