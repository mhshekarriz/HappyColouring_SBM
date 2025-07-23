import networkx as nx
import numpy as np
import math, random, copy, time

from Support import *
from metaheuristics import *

def free_vertices(G,lpc):
    free_ver=list(G.nodes)
    for i in lpc:
        free_ver.remove(i)
    return free_ver

def evaluate(G,colours,r):
    ev=[]
    for col in colours:
        ev.append(Happy_number(G,col,r))

    return ev

def evaluate_LS(G,colours,lpc,n,k,r,TL):
    ev=[]
    new=[]
    for col in colours:
        G1=colour_graph(G,col)
        V=Vertex_partition(G1,k)
        [G1,V,pt]=Profound_Local_Search(G1,V,lpc,r,TL)
        new.append(colour_list(G1,n))
        ev.append(len(Happy_v(G1,r)))
    new=np.array(new)
    return new, ev

def select_parents(colours,pop_size):
    parents=[]
    for i in range(int(pop_size/2),pop_size):
        parents.append(colours[i])

   
    return parents

def cross_over(G, n, r, pop_size, parents):
    new_gen=parents
    for i in range(0,int(pop_size/2),2):
        A=parents[i]
        B=parents[i+1]
        offsp1=[]
        offsp2=[]
        for j in range(n):
            choice=np.random.choice(2, 1).item()
            if choice==1:
                offsp1.append(A[j])
            else:
                offsp1.append(B[j])
        new_gen.append(offsp1)
        for j in range(n):
            choice=np.random.choice(2, 1).item()
            if choice==1:
                offsp2.append(A[j])
            else:
                offsp2.append(B[j])
        new_gen.append(offsp2)

    while len(new_gen)>pop_size:
        new_gen.pop(-1)
    return new_gen

def mute(G, n, k, r, pop_size,free_v, new_gen, mute_factor):
    m=math.floor(mute_factor*n)
    if m==0:
        m=1
    for i in range(int(pop_size/2),pop_size):
        vert=np.random.choice(free_v, m)
        for j in vert:
            new_gen[i][j]=np.random.choice(k, 1).item()

    return new_gen

def Evolutionary(Graph, U, lpc, k, r, Time_limit, pop_size, mute_factor, method):
    start_time=time.process_time()
    #np.random.seed(0)
    G=copy.deepcopy(Graph)
    GBest=copy.deepcopy(G)
    nBest=len(Happy_v(GBest,r))
    n=G.number_of_nodes()
    free_v=free_vertices(G,lpc)
    V=Vertex_partition(G,k)

    colours=(-1)*np.ones((pop_size,n),int)
    scores = np.zeros(pop_size)
    #generating the gen-0 of the population, introducing the precolouring and calculatin their fitness:
    if method=="random":
        for j in range(pop_size):
            for i in free_v:
                colours[j,i]=int(np.random.choice(k, 1).item())
            for i in lpc:
                colours[j,i]=G.nodes[i]["c"]

            scores[j]=Happy_number(G,colours[j],r)

    elif method=="LMC":
        for j in range(pop_size):
            [G_1, V_1, pt_1]=LMC(G,V,U)
            for i in range(n):
                colours[j,i]=G_1.nodes[i]["c"]
            scores[j]=Happy_number(G,colours[j],r)
    elif method=="LS":
        for j in range(pop_size):
            [G_1, V_1, pt_1]=Local_Search(G,V,lpc,r)
            for i in range(n):
                colours[j,i]=G_1.nodes[i]["c"]
            scores[j]=Happy_number(G,colours[j],r)


    top_ind = np.argpartition(scores , -pop_size)[-pop_size:]

        # extract the elit sub_population
    colours=colours[top_ind]
    scores.sort()



    while (time.process_time()-start_time <Time_limit and nBest<n):
        parents=select_parents(colours,pop_size)

        new_gen=cross_over(G,n,r,pop_size,parents)

        new_gen=mute(G, n, k, r, pop_size,free_v, new_gen, mute_factor)

        scores=evaluate(G,new_gen,r)


        top_ind = np.argpartition(scores , -pop_size)[-pop_size:]
        new_gen=np.array(new_gen)
        colours=new_gen[top_ind]
        scores.sort()


        if nBest<Happy_number(G, colours[-1], r):
            GBest=colour_graph(G, colours[-1])
            nBest=int(scores[-1])


    VP=Vertex_partition(GBest,k)
    end_time=time.process_time()-start_time

    return GBest, VP, end_time#, nBest, colours[-1]

def Memetic(Graph, U, lpc, k, r, Time_limit, pop_size, mute_factor, method):
    start_time=time.process_time()
    #np.random.seed(0)
    G=copy.deepcopy(Graph)
    GBest=copy.deepcopy(G)
    nBest=len(Happy_v(GBest,r))
    n=G.number_of_nodes()
    V=Vertex_partition(G,k)
    free_v=free_vertices(G,lpc)
    TL=Time_limit/(2*pop_size)




    colours=(-1)*np.ones((pop_size,n),int)
    scores = np.zeros(pop_size)
    #generating the gen-0 of the population, introducing the precolouring and calculatin their fitness:
    if method=="random":
        for j in range(pop_size):
            for i in free_v:
                colours[j,i]=int(np.random.choice(k, 1).item())
            for i in lpc:
                colours[j,i]=G.nodes[i]["c"]
            G_1=colour_graph(G,colours[j])
            V_1=Vertex_partition(G_1,k)
            [G_1,V_1,pt]=Local_Search(G_1,V_1,lpc,r)
            colours[j]=colour_list(G_1,n)
            scores[j]=Happy_number(G,colours[j],r)

    elif method=="LMC":
        for j in range(pop_size):
            [G_1, V_1, pt_1]=LMC(G,V,U)
            [G_1,V,pt]=Local_Search(G_1,V_1,lpc,r)
            for i in range(n):
                colours[j,i]=G_1.nodes[i]["c"]
            scores[j]=Happy_number(G,colours[j],r)
    elif method=="LS":
        for j in range(pop_size):
            [G_1, V_1, pt_1]=Local_Search(G,V,lpc,r)
            [G_1,V_1,pt]=Extended_Local_Search(G_1,V,lpc,r)
            for i in range(n):
                colours[j,i]=G_1.nodes[i]["c"]
            scores[j]=Happy_number(G,colours[j],r)

    top_ind = np.argpartition(scores , -pop_size)[-pop_size:]

        # extract the elit sub_population
    colours=colours[top_ind]
    scores.sort()
    #####################################

    
    while (time.process_time()-start_time <Time_limit and nBest<n):
        parents=select_parents(colours,pop_size)

        new_gen=cross_over(G,n,r,pop_size,parents)

        new_gen=mute(G, n, k, r, pop_size,free_v, new_gen, mute_factor)

        [new_gen,scores]=evaluate_LS(G,new_gen,lpc,n,k,r,TL)


        top_ind = np.argpartition(scores , -pop_size)[-pop_size:]
        new_gen=np.array(new_gen)
        colours=new_gen[top_ind]
        scores.sort()


        if nBest<Happy_number(G, colours[-1], r):
            GBest=colour_graph(G, colours[-1])
            nBest=int(scores[-1])
        #caclulate the number of happy vetices

    VP=Vertex_partition(GBest,k)
    end_time=time.process_time()-start_time

    return GBest, VP, end_time
