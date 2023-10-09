#!/usr/bin/env python
import os,re,glob
import math
import sys

seed = 20

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def avgd(X):
    total = 0.0
    i = 0
    for x in X:
        total+=x
        i+=1
    if i==0: i=1
    return total/float(i)

# Return a meaningful string seperated by an _
def concat(f,postfix):
    filename = ""
    for k in f[:-1]:
        filename += k + "_"
    if postfix == 1:
        filename += f[-1]+".txt"
    else:
        filename += f[-1]
    return filename

# a simple data class to keep track of all the data from the files
class Data:
    def __init__(self,filename,EA):
        self.read(filename,EA)
    def valid(self): return hasattr(self,"HC")
    def read(self,fname,EA):
        t_fname = fname
        self.happy = -1
        self.unhappy = -1
        self.gap = -1
        self.vert = float(t_fname.split("_")[2])
        self.ss = -1 # start score
        self.ub = -1
        self.time = 600.0

        filename = t_fname
        lines = open(filename).readlines()
        if not lines:
            print ("Warning, missing data in" + t_fname)
            return
        try:
            # Extract happy, unhappy
            ind = -1
            while True:
                if "***" in lines[ind]: break
                ind -= 1
            f = lines[ind].strip().split()
            self.unhappy = float(f[3].split(",")[0])
            self.happy = self.vert-self.unhappy
        except:
            print(fname)


# the mean of some values in X some of which may not be defined

# the mean of some values in X some of which may not be defined

def avg(X):
    total = 0.0
    i = 0
    for x in X:
        if(x>-1):
            total+=x
            i+=1
    return total/max(1.0,float(i))


def stdDev(X):
    ss,mn = 0.0,0.0
    i=0
    for x in X:
        if(x>0):
            ss+=x*x
            mn+=x
            i+=1
    if i==0: i=1
    mn /= i
    return math.sqrt(max(0,ss/float(i)-mn*mn))

# create a tuple to obtain a sorted order
def testKey(key):
    "convert something like '100_8' into (100,8) for sorting purposes"
    return tuple( int(x) for x in re.split("_?|-",key)[:])

def getKey(item):
    return testKey(item)[:]

def tabulateResults(allResults):
    if not allResults: return
    # extract prob from allResults given prob,method
    print ("Instance\tHV\tUV\tGap\tTime")
    instances = set( prob for meth,prob in allResults)
    #print(instances)
    methods = set( meth for meth,prob in allResults)
    for m in methods:
        #for instance in sorted(instances,key = getKey):
        for instance in sorted(instances):
            if (m,instance) not in allResults.keys(): continue
            for i in allResults[m,instance]:
                print ("%s,%2.0f,%2.0f" % (instance, i.happy, i.unhappy))

p1="."
allResults = {}
for dir1 in os.listdir(p1):
    # look in OUTDIR
    if not os.path.isdir(p1+os.sep+dir1): continue
    p2 = p1+os.sep+dir1
    #if not "-CP" in p2: continue
    for fname in os.listdir(p2):
        #print(fname)
        EA = False
        if "EA" in p2: EA = True
        if os.path.isdir(fname): continue
        if fname.find("out_")==-1: continue
        prob = fname.split("out_HCD_")[1]
        pro = prob.split(".txt")[0]
        d = Data(p2+os.sep+fname,EA)
        meth = dir1
        allResults[meth,pro] = allResults.get((meth,pro),[])+[d]

tabulateResults(allResults)
