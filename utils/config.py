# -*- coding: utf-8 -*-
import pickle




class Config():
    
    def __init__(self, path):
        self.path = path
        
        self.data = {}
    
    
    def loadData(self):
        f = open(self.path, "r")
        self.data = pickle.load(f)
        f.close()
        
        
    def saveData(self):
        f = open(self.path, "w")
        pickle.dump(self.data, f)
        f.close()
        
        
    def __iter__(self):
        return self.data.__iter__()
        
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
        
    def __getitem__(self, key):
        return self.data[key]
        
        
    def iteritems(self):
        return self.data.iteritems()
        
        
    def iterkeys(self):
        return self.data.iterkeys()
        
        
        
        
        
if __name__ == "__main__":
    
    conf = Config("E:/Programmieren/Python/McModder_v5/config")
    
    conf["workspace"] = "E:/Programmieren/Python/McModder_v5/workspace"
    
    conf.saveData()