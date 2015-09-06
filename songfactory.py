from os import listdir
from model import SongModel
import pdb
class SongFactory:
    def __init__(self, folder):
        print folder
        files =  listdir(folder)
        self.models = []
        print files
        for x in files:
            if x != '.DS_Store':
                print("Working on %s" % x)
                tempModel = open(folder+"/"+x,'r')
                self.models.append(SongModel(tempModel.readline()))

    def getModels(self):
        return self.models
