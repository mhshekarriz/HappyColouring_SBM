import pandas as pd
import numpy as np
from genSBM import *
from Happy_v_time import *

n=1200

parts=[2,3,4,5,6,8,10,12,15,20]

path_inp="/home/dhananjay/Iman/Data/Raw/"

path_out="/home/dhananjay/Iman/Data/Out/"







for k in parts:
    print('k = \t',k)
    i=0 #number of runs
    i_r=[]
    P_r=[]
    Q_r=[]
    S_r=[]
    R_r=[]

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
    with open("/home/dhananjay/Iman/Data/log"+str(k)+".txt", "w") as f_log:
        for p in np.arange(0.2,1,0.1):
            print('p = \t',p)
            for q in np.arange(0.01,(p/2)+0.001,0.1):
                print('q = \t',q)
                for seed in [0,3,6,10]:
                    print('seed = \t',seed)
                    [G,V,U]=genSBM(n,k,p,q,seed)
                    filename="SBM_n="+str(n)+"_k="+str(k)+"_p="+str(round(p,2))+"_q="+str(round(q,3))+"_seed="+str(seed)
                    comment_file="n="+str(n)+" k="+str(k)+" p="+str(round(p,2))+" q="+str(round(q,3))+" seed="+str(seed)+"\n"
                    write_dimacs(G,V,path_inp+filename+".txt","c "+comment_file)
                    f_log.write("++++++++++++New graph loaded+++++++++++++++\n"+" File="+filename+".txt\n"+comment_file)
                    #with open(path_out+filename+".txt","w") as f_out:
                        #f_out.write(" Graph's File="+filename+".txt\n"+comment_file+"***********************************\n")
                    for r in [0.1,0.3,0.5,0.8,1]:
                        i+=1
                        i_r.append(i)
                        P_r.append(p)
                        Q_r.append(q)
                        S_r.append(seed)
                        R_r.append(r)
                        print('Run numbrt:\t',i)
                        #f_out.write(" r="+str(r)+"\n"+"________________________________________________\n")
                        [F1,T1,ctgreedy1]=greedy1_HC_r(G,V,U,r)
                        gr1_time.append(ctgreedy1)
                        hcd1=How_accurate_is_comm_det(n,k,T1)
                        #f_out.write(comm1)
                        gr1_cr.append(hcd1)
                        gr1_hr.append(len(Happy_v(F1,r))/n)



                        [F2,T2,ctgreedy2]=greedy2_HC_r(G,V,U,r)
                        gr2_time.append(ctgreedy2)
                        hcd2=How_accurate_is_comm_det(n,k,T2)
                        #f_out.write(comm2)
                        gr2_cr.append(hcd2)
                        gr2_hr.append(len(Happy_v(F2,r))/n)


                        [F3,T3,ctgreedy3]=greedy3_HC_r(G,V,U,r)
                        gr3_time.append(ctgreedy3)
                        hcd3=How_accurate_is_comm_det(n,k,T3)
                        # f_out.write(comm3)
                        gr3_cr.append(hcd3)
                        gr3_hr.append(len(Happy_v(F3,r))/n)



                        [H,S,ctgrowth]=growth_HC_r(G,V,U,r)
                        gro_time.append(ctgrowth)
                        hcd_g=How_accurate_is_comm_det(n,k,S)
                        #f_out.write(comm_g+"===============================================\n")
                        gro_cr.append(hcd_g)
                        gro_hr.append(len(Happy_v(H,r))/n)

                datag={'col1': P_r, 'col2': Q_r, 'col3': S_r, 'col4': R_r, 'col5': gr1_time, 'col6': gr1_hr, 'col7': gr1_cr, 'col8': gr2_time, 'col9': gr2_hr, 'col10': gr2_cr, 'col11': gr3_time, 'col12': gr3_hr, 'col13': gr3_cr, 'col14': gro_time, 'col15': gro_hr, 'col16': gro_cr}
                df=pd.DataFrame(data=datag,index=i_r,)# columns=['p','q','seed','r','g1_time','g1_happy','g1_comm','g2_time','g2_happy','g2_comm','g3_time','g3_happy','g3_comm','gro_time','gro_happy','gro_comm']
                df.to_excel("output"+str(k)+".xlsx")
