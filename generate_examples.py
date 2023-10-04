from genSBM import *
import numpy as np

n=1200
list=[2,3,4,5,6,10]


for k in list:
    for p in np.arange(0.1,0.9,0.1):
        for q in np.arange(0.001,p/100,0.001):
            for s in range(11):
                genSBM(n,k,p,q,s)

