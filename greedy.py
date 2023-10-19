import networkx as nx
from genSBM import *
from Happy_v import *

r=0.5

[G,V,U]=genSBM(1200,6,0.7,0.001,10)
[H,S]=greedy1_HC_r(G,V,U,r)
[F,T]=greedy2_HC_r(G,V,U,r)

