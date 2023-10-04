
import networkx as nx
import numpy as np
import random
from dimacs import *

def genSBM(n, k, p, q, s): #n=number of vertices, k=number of partitions, p=edge probabilities inside communities, q=intercommunity edge probabilities, s=probability seed
    sizes=np.zeros(k,dtype=int)
    c=np.zeros(k,dtype=int) #pre-colored vertices
    for i in range(k):
        sizes[i]=int(n/k)
        c[i]=random.randint(i*int(n/k), (i+1)*int(n/k))

    p1=np.ones((k,k))
    p1=q*p1
    p2=np.identity(k)
    p2=(p-q)*p2
    probs=p1+p2
    probs=probs.tolist()
    G=nx.stochastic_block_model(sizes, probs,seed=s)
    filename="SBM_n="+str(n)+"_k="+str(k)+"_p="+str(round(p,2))+"_q="+str(round(q,3))+"_seed="+str(s)+".txt"

    dimacs(G, c, k, filename)
