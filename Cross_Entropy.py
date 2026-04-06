import networkx as nx
import numpy as np
import math, random, copy, time

from Support import *
from LocalSearch import *

def CE_LS(Graph, lpc, k, r, Time_limit, pop_size, elite, smoothing_factor):
    '''Cross-Entropy integrated with Local Search for soft happy colouring.
    The input is:
    Graph - a (coloured or partially coloured) NetworkX graph,
    lpc - list of precoloured vertices,
    k - number of colours,
    r - the proportion of happiness,
    Time_limit - time limit for the function (in seconds),
    pop_size - population size,
    elite - the size of the elite samples, and
    smoothing_factor - the smoothing factor for updating the probability distribution.
    The output is
    GBest - a (coloured) NetworkX graph, the best found solution,
    Vp - updated list of list of colouring, and
    end_time - the CPU runtime of the function.'''
    start_time=time.process_time()
    G=copy.deepcopy(Graph)
    GBest=copy.deepcopy(G)
    nBest=len(Happy_v(GBest,r))
    n=G.number_of_nodes()
    probs={}

    # Create a list of nodes (starting from zero)
    keys = list(G.nodes)
    # Create initial probabilities
    for key in keys:
        probs[key] = (1/k)*np.ones(k)

# Probebility of assigning the colour of precoloured vertices to them must be 1
    for i in lpc:
        probs[i]=np.zeros(k)
        probs[i][G.nodes[i]["c"]]=1

    population=(-1)*np.ones((pop_size,n),int)


    while (time.process_time()-start_time <Time_limit and nBest<n):
        for j in range(pop_size):
            for i in keys:
                population[j,i]=np.random.choice(k, 1, p=probs[i]).item()
        #caclulate the number of happy vetices

        scores = np.zeros(pop_size)

        # employing local search over the population
        for j in range(pop_size):
            G=colour_graph(G,population[j])
            V=Vertex_partition(G,k)
            [G,V,pt]=Local_Search(G,V,lpc,r)
            scores[j]=len(Happy_v(G,r))
            if scores[j]>nBest:
                GBest=copy.deepcopy(G)
                nBest=scores[j]
            for x in G.nodes:
                population[j][x]=G.nodes[x]["c"]

        #get top max scores
        num_top_indices=int(np.ceil(pop_size*elite)) #number of items in the elite sample
        top_ind = np.argpartition(scores , -num_top_indices)[-num_top_indices:]

        # extract the elite sub_population
        elite_mat=population[top_ind, :]

        #modified probabilties based on the elite sample
        probs_b={}
        for key in keys:
            aa=elite_mat[:,key]
            unique, counts = np.unique(aa, return_counts=True)
            new_probs=np.zeros(k)
            for i in range(len(unique)):
                new_probs[unique.astype('i')[i]]=counts.astype('i')[i]/num_top_indices
            probs_b[key] = new_probs


        probs_new={}
        for key in keys:
            probs_new[key] = smoothing_factor*probs[key]+(1-smoothing_factor)*probs_b[key]

        for i in lpc:
            probs_new[i]=np.zeros(k)
            probs_new[i][G.nodes[i]["c"]]=1

        probs=probs_new


    VP=Vertex_partition(GBest,k)
    end_time=time.process_time()-start_time

    return GBest, VP, end_time


def Cross_Entropy(Graph, lpc, k, r, Time_limit, pop_size, elite, smoothing_factor):
    '''Pure Cross-Entropy for soft happy colouring.
    The input is:
    Graph - a (coloured or partially coloured) NetworkX graph,
    lpc - list of precoloured vertices,
    k - number of colours,
    r - the proportion of happiness,
    Time_limit - time limit for the function (in seconds),
    pop_size - population size,
    elite - the size of the elite samples, and
    smoothing_factor - the smoothing factor for updating the probability distribution.
    The output is
    GBest - a (coloured) NetworkX graph, the best found solution,
    Vp - updated list of list of colouring, and
    end_time - the CPU runtime of the function.'''
    start_time=time.process_time()
    G=copy.deepcopy(Graph)
    GBest=copy.deepcopy(G)
    nBest=len(Happy_v(GBest,r))
    n=G.number_of_nodes()
    probs={}

    # Create a list of nodes (starting from zero)
    keys = list(G.nodes)
    # Create initial probabilities
    for key in keys:
        probs[key] = (1/k)*np.ones(k)

# Probebility of assigning the colour of precoloured vertices to them must be 1
    for i in lpc:
        probs[i]=np.zeros(k)
        probs[i][G.nodes[i]["c"]]=1

    population=(-1)*np.ones((pop_size,n),int)


    while (time.process_time()-start_time <Time_limit and nBest<n):
        for j in range(pop_size):
            for i in keys:
                population[j,i]=np.random.choice(k, 1, p=probs[i]).item()
        #caclulate the number of happy vetices

        scores = np.zeros(pop_size)
        for i in range(pop_size):#new probability distribution
            scores[i]=Happy_number(G, population[i], r)
            if scores[i]>nBest:
                nBest=scores[i]
                GBest=colour_graph(G,population[i])



        #get top max scores
        num_top_indices=int(np.ceil(pop_size*elite)) #number of items in the elite sample
        top_ind = np.argpartition(scores , -num_top_indices)[-num_top_indices:]

        # extract the elite sub_population
        elite_mat=population[top_ind, :]

        #modified probabilties based on the elite sample
        probs_b={}
        for key in keys:
            aa=elite_mat[:,key]
            unique, counts = np.unique(aa, return_counts=True)
            new_probs=np.zeros(k)
            for i in range(len(unique)):
                new_probs[unique.astype('i')[i]]=counts.astype('i')[i]/num_top_indices
            probs_b[key] = new_probs
        #

        # updating colour probabilities of the vertices based on their neigbourhoods
        probs_a={}
        for key in keys:
            probs_a[key]=np.zeros(k)
            summate=0
            for i in range(k):
                for u in G.adj[key]:
                    probs_a[key][i]+=probs_b[u][i]
                summate+=probs_a[key][i]
            probs_a[key]=(1/summate)*probs_a[key]


        coeff=2
        probs_c={}
        for key in keys:
            probs_c[key]=np.zeros(k)
            for i in range(k):
                probs_c[key][i]=(probs_b[key][i]+coeff*probs_a[key][i])/(1+coeff)


        #new probability distribution
        probs_new={}
        for key in keys:
            probs_new[key] = smoothing_factor*probs[key]+(1-smoothing_factor)*probs_c[key]

        for i in lpc:
            probs_new[i]=np.zeros(k)
            probs_new[i][G.nodes[i]["c"]]=1

        probs=probs_new



    VP=Vertex_partition(GBest,k)
    end_time=time.process_time()-start_time

    return GBest, VP, end_time
