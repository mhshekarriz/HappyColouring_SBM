import networkx as nx
import numpy as np
from genSBM import *
from Happy_v import *

#r=0.5
n=1200
parts=[2,3,4,5,6,10]
path_inp="/home/ethernal/Documents/HappyColouring_SBM/Data/Raw/"
path_out1="/home/ethernal/Documents/HappyColouring_SBM/Data/Greedy3_out/"
path_out2="/home/ethernal/Documents/HappyColouring_SBM/Data/Growth_out/"

i=0
ratio_greedy=0
ratio_growth=0


for k in parts:
    for p in np.arange(0.1,1,0.1):
        for q in np.arange(0.001,p+0.001,0.01):
            for seed in range(11):
                [G,V,U]=genSBM(n,k,p,q,seed)
                filename="SBM_n="+str(n)+"_k="+str(k)+"_p="+str(round(p,2))+"_q="+str(round(q,3))+"_seed="+str(seed)
                comment1="c n="+str(n)+" k="+str(k)+" p="+str(round(p,2))+" q="+str(round(q,3))+" seed="+str(seed)+"\n"
                write_dimacs(G,V,path_inp+filename+".txt",comment1)
                for r in np.arange(0.1,1.1,0.1):
                    [F,T,ctgreedy]=greedy3_HC_r(G,V,U,r)
                    Av=[]
                    for t in range(len(T)):
                        Av.append(len(T[t]))
                    comment2=comment1+"c Algorithm: greedy3_HC_r \n"+"Time consumed: "+str(ctgreedy)+"\n"+"c r="+str(r)+"\n"+"c The number happy vertices: "+str(len(Happy_v(F,r)))+"\n"+"c Fraction of happy vertices: "+str(round(len(Happy_v(F,r))/n,4))+"\n"+"c Vertex partition sizes are "+str(Av)+"\n"
                    write_dimacs(F,T,path_out1+"Out_"+filename+"_r="+str(round(r,3))+".txt",comment2)
                    i+=1
                    ratio_greedy+=len(Happy_v(F,r))/n


                    [H,S,ctgrowth]=growth_HC_r(G,V,U,r)
                    Bv=[]
                    for s in range(len(S)):
                        Bv.append(len(S[s]))
                    comment3=comment1+"c Algorithm: growth_HC_r \n"+"Time consumed: "+str(ctgrowth)+"\n"+"c r="+str(r)+"\n"+"c The number happy vertices: "+str(len(Happy_v(H,r)))+"\n"+"c Fraction of happy vertices: "+str(round(len(Happy_v(H,r))/n,4))+"\n"+"c Vertex partition sizes are "+str(Bv)+"\n"
                    write_dimacs(H,S,path_out2+"Out_"+filename+"_r="+str(round(r,3))+".txt",comment3)
                    ratio_growth+=len(Happy_v(H,r))/n

Ave_ratio_greedy=ratio_greedy/i
Ave_ratio_growth=ratio_growth/i

with open("/home/ethernal/Documents/HappyColouring_SBM/Data/log.txt", "w") as f:
    f.write("Ave_ratio_greedy= "+str(Ave_ratio_greedy)+"\n")
    f.write("Ave_ratio_growth= "+str(Ave_ratio_growth)+"\n")
