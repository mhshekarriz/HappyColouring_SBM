import networkx as nx
import numpy as np
from genSBM import *
from Happy_v import *

#r=0.5
n=1200
#parts=[2,3,4,5,6,8,10]
k=5
path_inp="/home/dhananjay/Iman/Data/Raw/"
path_out1="/home/dhananjay/Iman/Data/Greedy3_out/"
path_out2="/home/dhananjay/Iman/Data/Growth_out/"

i=0
ratio_greedy=0
time_greedy=0
ratio_growth=0
time_growth=0
with open("/home/dhananjay/Iman/Data/log5.txt", "w") as f_log:
    for p in np.arange(0.1,1,0.1):
            for q in np.arange(0.01,p+0.001,0.1):
                for seed in [0,3,6,10]:
                    [G,V,U]=genSBM(n,k,p,q,seed)
                    filename="SBM_n="+str(n)+"_k="+str(k)+"_p="+str(round(p,2))+"_q="+str(round(q,3))+"_seed="+str(seed)
                    comment1="c n="+str(n)+" k="+str(k)+" p="+str(round(p,2))+" q="+str(round(q,3))+" seed="+str(seed)+"\n"
                    write_dimacs(G,V,path_inp+filename+".txt",comment1)
                    for r in np.arange(0.1,1.1,0.1):
                        i+=1
                        print('Run numbrt:\t',i)
                        [F,T,ctgreedy]=greedy3_HC_r(G,V,U,r)
                        hcd1=How_accurate_is_comm_det(n,k,T)
                        Av=[]
                        for t in range(len(T)):
                            Av.append(len(T[t]))
                        comment2="c Algorithm: greedy3_HC_r \n"+comment1+"c Time consumed: "+str(ctgreedy)+"\n"+"c r="+str(r)+"\n"+"c The number happy vertices: "+str(len(Happy_v(F,r)))+"\n"+"c Fraction of happy vertices: "+str(round(len(Happy_v(F,r))/n,4))+"\n"+"c Vertex partition sizes are "+str(Av)+"\n"+"c Accuracy of community detection is "+str(round(hcd1,4))+"\n"
                        write_dimacs(F,T,path_out1+"Out_"+filename+"_r="+str(round(r,3))+".txt",comment2)
                        f_log.write(comment2+"--------------------------------------------------------\n")
                        ratio_greedy+=len(Happy_v(F,r))/n
			time_greedy+=ctgreedy


                        [H,S,ctgrowth]=growth_HC_r(G,V,U,r)
                        hcd2=How_accurate_is_comm_det(n,k,S)
                        Bv=[]
                        for s in range(len(S)):
                            Bv.append(len(S[s]))
                        comment3="c Algorithm: growth_HC_r \n"+comment1+"c Time consumed: "+str(ctgrowth)+"\n"+"c r="+str(r)+"\n"+"c The number happy vertices: "+str(len(Happy_v(H,r)))+"\n"+"c Fraction of happy vertices: "+str(round(len(Happy_v(H,r))/n,4))+"\n"+"c Vertex partition sizes are "+str(Bv)+"\n"+"c Accuracy of community detection is "+str(round(hcd2,4))+"\n"
                        write_dimacs(H,S,path_out2+"Out_"+filename+"_r="+str(round(r,3))+".txt",comment3)
                        f_log.write(comment3+"--------------------------------------------------------\n")
                        ratio_growth+=len(Happy_v(H,r))/n
			time_growth+=ctgrowth

    Ave_ratio_greedy=ratio_greedy/i
    Ave_ratio_growth=ratio_growth/i
    f_log.write("Average ratio of happy vertices for the greedy3 algorithm= "+str(Ave_ratio_greedy)+"\n")
    f_log.write("Average ratio of happy vertices for the growth algorithm= "+str(Ave_ratio_growth)+"\n")

    f_log.write("Avarage time for greedy3: "+str(time_greedy/i)+" seconds.\n")
    f_log.write("Avarage time for growth: "+str(time_growth/i)+" seconds.\n")

