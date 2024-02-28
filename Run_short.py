import pandas as pd
import numpy as np
from genSBM import *
from Happy_v_time import *





path_inp="/home/ethernal/Documents/Happy-community/Code/Data/Raw/"

path_out="/home/ethernal/Documents/Happy-community/Code/Data/Out/"

n=1000 #number of vertices
parts=list(range(2,21)) #number of colours
i=0 #number of runs
i_r=[]
P_r=[]
Q_r=[]
S_r=[]
R_r=[]
itt_r=[]

gr1_time=[]
gr2_time=[]
gr3_time=[]
gro_time=[]

gr1_hr=[]
gr2_hr=[]
gr3_hr=[]
gro_hr=[]

gr1_cr=[]
gr2_cr=[]
gr3_cr=[]
gro_cr=[]

k_r=[]
n_r=[]
comm_hr=[]

xi=[]
#epsilon=0.0000001
epsilon=0.000000001



for k in parts:
    print('k = \t',k)
    for p in np.arange(0.1,1,0.1):
        print('p = \t',p)
        for q in np.arange(0.01,(p/2)+0.001,0.1):
            print('q = \t',q)
            for seed in [0,3,6,10]:
                print('seed= \t',seed)
                for itt in range(1,11,1):
                    print('number of precoloured vertices per partition= \t',itt)
                    [G,V,U]=genSBM(n,k,p,q,seed,itt)
                    filename="SBM_n="+str(n)+"_k="+str(k)+"_p="+str(round(p,2))+"_q="+str(round(q,3))+"_seed="+str(seed)+"pre_col_pp="+str(itt)
                    comment_file="n="+str(n)+" k="+str(k)+" p="+str(round(p,2))+" q="+str(round(q,3))+" seed="+str(seed)+"number of precoloured vertices per partition="+str(itt)+"\n"
                    write_dimacs(G,V,path_inp+filename+".txt","c "+comment_file)
                    for r in np.arange(0.1,1.1,0.1):
                        i+=1
                        n_r.append(n)
                        i_r.append(i)
                        P_r.append(p)
                        Q_r.append(q)
                        S_r.append(seed)
                        R_r.append(r)
                        k_r.append(k)
                        itt_r.append(itt)
                        print('Run number:\t',i)
                        [F1,T1,ctgreedy1]=greedy1_HC_r(G,V,U,r)
                        write_dimacs(F1,T1,path_out+filename+"_r="+str(round(r,2))+"_greedy1.txt","c "+comment_file+"c Algorithm: Greedy 1\n")
                        gr1_time.append(ctgreedy1)
                        hcd1=How_accurate_is_comm_det(n,k,T1)
                        gr1_cr.append(hcd1)
                        gr1_hr.append(len(Happy_v(F1,r))/n)



                        [F2,T2,ctgreedy2]=greedy2_HC_r(G,V,U,r)
                        write_dimacs(F2,T2,path_out+filename+"_r="+str(round(r,2))+"_greedy2.txt","c "+comment_file+"c Algorithm: Greedy 2\n")
                        gr2_time.append(ctgreedy2)
                        hcd2=How_accurate_is_comm_det(n,k,T2)
                        gr2_cr.append(hcd2)
                        gr2_hr.append(len(Happy_v(F2,r))/n)


                        [F3,T3,ctgreedy3]=greedy3_HC_r(G,V,U,r)
                        write_dimacs(F3,T3,path_out+filename+"_r="+str(round(r,2))+"_LMC.txt","c "+comment_file+"c Algorithm: LocalMaximalColouring\n")
                        gr3_time.append(ctgreedy3)
                        hcd3=How_accurate_is_comm_det(n,k,T3)
                        gr3_cr.append(hcd3)
                        gr3_hr.append(len(Happy_v(F3,r))/n)



                        [H,S,ctgrowth]=growth_HC_r(G,V,U,r)
                        write_dimacs(H,S,path_out+filename+"_r="+str(round(r,2))+"_growth.txt","c "+comment_file+"c Algorithm: Growth\n")
                        gro_time.append(ctgrowth)
                        hcd_g=How_accurate_is_comm_det(n,k,S)
                        gro_cr.append(hcd_g)
                        gro_hr.append(len(Happy_v(H,r))/n)

                        [H1,V1]=Comm_HC(G,k)
                        comm_hr.append(len(Happy_v(H1,r))/n)

                        xi.append(max(0,min((p/(p+q*(k-1))),np.log(((k/n)*np.log(epsilon)+p*np.exp(1)+ q*(k-1))/(p+q*(k-1))))))


                datag={'k': k_r,'p': P_r, 'q': Q_r, 's': S_r, 'pre-col / comm': itt_r, 'r': R_r, 'GR1-time': gr1_time, 'GR1-Happy': gr1_hr, 'GR1-Comm': gr1_cr, 'GR2-time': gr2_time, 'GR2-Happy': gr2_hr, 'GR2-Comm': gr2_cr, 'GR3-time': gr3_time, 'GR3-happy': gr3_hr, 'GR3-comm': gr3_cr, 'GrR-time': gro_time, 'GrR-happy': gro_hr, 'GrR-comm': gro_cr,'Comm-Happy':comm_hr,'xi':xi}
                df=pd.DataFrame(data=datag,index=i_r,)# columns=['p','q','seed','r','g1_time','g1_happy','g1_comm','g2_time','g2_happy','g2_comm','g3_time','g3_happy','g3_comm','gro_time','gro_happy','gro_comm']
                df.to_excel("output.xlsx")



