import nbtlib
import numpy as np
import re
import json

def open_file(name):
    return nbtlib.load(name)
#returns X Y Z

def get_dimension(file):
    return map(int, [file['Width'], file['Height'], file['Length']])

def getRequiredSize(file):
    X,Y,Z = get_dimension(file)
    return np.ceil(np.array([X,Y,Z]) / 16)
def prepareArray(file):
    X,Y,Z = getRequiredSize(file)
    return np.zeros(X*Y*Z, dtype = np.int16)

def getByteArray(file):
    return file['BlockData']
def remap(palette):
    retVal = dict()
    for keys in palette:
        retVal[palette[keys]] = genCompound(keys)
    return retVal

def genCompound(fromString):
    prop = re.findall('\[(.*?]*)\]',fromString)
    propComp = dict()
    for props in prop:
        key, val = props.split('=')
        propComp[key] = nbtlib.String(val)
    propCompound = nbtlib.Compound({'Name' : nbtlib.String(re.sub('\[(.*?]*)\]','',fromString))})
    if propComp:
        propCompound['Properties']= nbtlib.Compound(propComp)
    return propCompound

    
class Schem:
    def __init__(self, file):
        if type(file) == str:
            file = nbtlib.load(file)
        x,y,z = get_dimension(file)
        self.sizeX =x
        self.sizeY =y
        self.sizeZ =z
        self.sizeLayer =x*z
        self.byteLen = x*y*z
        self.byteArray = getByteArray(file)
        self.npArray = np.array(self.byteArray).reshape(y,z,x)
        self.palette = remap(file['Palette'])
        self.paletteSize = file['PaletteMax']
        self.palette[self.paletteSize] = nbtlib.Compound({
                                    'Name' : nbtlib.String('minecraft:air')})
    def getIndex(self, x,y,z):
        return y*self.sizeLayer + z*self.sizeX + x
    def isOutofBound(self, x,y,z):
        return x >= self.sizeX or y >= self.sizeY or z >= self.sizeZ
    def getRequiredSize(self):
        return map(int, np.ceil(np.array([self.sizeX, self.sizeY, self.sizeZ]) / 16))
    def getInt(self,x,y,z):
        if self.isOutofBound(x,y,z):
            return self.paletteSize
        return self.byteArray[self.getIndex(x,y,z)]
    def translateBlock(self, integer : int):
        return self.palette[integer]
    def getBlock(self,x,y,z):
        return self.translateBlock(self.getInt(x,y,z))
    def getSection(self, x, y, z):
        ret = np.ones((16,16,16),self.paletteSize, dtype=np.int16) 
        for xi in range(16):
            for yi in range(16):
                for zi in range(16):
                    ret[xi,yi,zi] = self.getInt(xi+x*16, yi+y*16, zi+z*16)
        return ret
    def getFlatSection(self, x, y, z):
        ret = np.full(4096,self.paletteSize, dtype = np.int16)
        _ = 0
        for xi in range(16):
            for yi in range(16):
                for zi in range(16):
                    ret[_] = self.getInt(xi+x*16, yi+y*16, zi+z*16)
                    _+=1
        return ret
    def getArrayConverted(self, x,y,z):
        section = self.getFlatSection(x,y,z)
        unique = np.unique(section)
        nbtlist = []
        translatemap = dict()
        for idx, val in enumerate(unique):
            nbtlist.append(self.palette[val])
            translatemap[val] = idx
        return Schem.getSafeV2Array(Schem.translate(section, translatemap)), nbtlib.List[nbtlib.Compound](nbtlist)
    def getArrayNonConvert(self,x,y,z):
        section = self.getFlatSection(x,y,z)
        unique = np.unique(section)
        nbtlist = []
        translatemap = dict()
        for idx, val in enumerate(unique):
            nbtlist.append(self.palette[val])
            translatemap[val] = idx
        return Schem.translate(section, translatemap), nbtlib.List[nbtlib.Compound](nbtlist)
    def getSafeV2Array(v1arr):
        ret = np.zeros(8192, np.int8)
        for i in range(4096):
            ret[2*i] = (v1arr[i] & 0xff)
            ret[2*i+1] = ((v1arr[i]>>8) & 0xff)
        return ret
    def getFileToSave(self,x,y,z):
        arr, paletteList = self.getArrayConverted(x,y,z)
        innercomp = nbtlib.Compound({'bits_v2' : nbtlib.ByteArray(arr), 'palette' : paletteList})
        outerComp = nbtlib.File({'blueprint': innercomp})
        return outerComp
    def getFileForJson(self,x,y,z):
        arr, paletteList = self.getArrayNonConvert(x,y,z)
        innercomp = nbtlib.Compound({'bits_v2' : arr.tolist(), 'palette' : paletteList})
        outerComp = nbtlib.File({'blueprint': innercomp})
        return outerComp
    def saveAsJson(self, x,y,z, fileName):
        jsonFile = self.getFileForJson(x,y,z)
        with open(fileName, 'w') as f:
            json.dump(jsonFile, f)
    def saveAllJson(self, defaultName = 'a', delimeter = 'b'):
        X,Y,Z = self.getRequiredSize()
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    self.saveAsJson(x,y,z,defaultName+delimeter.join(map(str, [x,y,z])) + '.json')
        return X*Y*Z
    def saveAs(self, x,y,z, fileName, compressed = True):
        w = self.getFileToSave(x,y,z)
        w.save(fileName+'.nbt', gzipped=compressed)
    def translate(A,dictionary):
        sort_idx = np.argsort(list(dictionary.keys()))
        idx = np.searchsorted(list(dictionary.keys()), A, sorter = sort_idx)
        return np.asarray(list(dictionary.values()))[sort_idx][idx]
    def saveAll(self, defaultName = 'a', delimeter = 'b'):
        X,Y,Z = self.getRequiredSize()
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    self.saveAs(x,y,z,defaultName+delimeter.join(map(str, [x,y,z])))
        return X*Y*Z
    
#a = Schem(nbtlib.load('mumeibig.schem'))
#a.saveAll('birb')
    
