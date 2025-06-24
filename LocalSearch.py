import networkx as nx
import numpy as np
import math, random, copy, time

from Support import *

def Local_Search(G,V,lpc,r): #lpc=list of precoloured vertices
    '''The function performs a local search on the (partially) coloured graph G.
    The input is:
    G - a (coloured or partially coloured) NetworkX graph,
    V - list of lists of coloured vertices; the vertex v in the ith list means that v has the colour i,
    lpc - list of precoloured vertices, and
    r - the proportion of happiness.
    The output is
    Graph - a (coloured) NetworkX graph,
    Vc - updated list of list of colouring, and
    pt - the CPU runtime of the function.'''
    start_time=time.process_time()
    #st_real=time.time()
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    k=len(Vc)
    U=Unhappy_v(Graph,r)
    Un=[x for x in U if x not in lpc]
    Un1=copy.deepcopy(Un)

   # j=0#counter of the while loop with consecutive no improvement
    while Un!=[]:
        Un_pr=copy.deepcopy(Un)
        for u in Un:
            colour_palette=[]
            for s in range(k):
                colour_palette.append([])
            for t in list(Graph.adj[u]):
                if (Graph.nodes[t]["c"]!=-1):
                    colour_palette[Graph.nodes[t]["c"]].append(t)
            i=0
            cq=-1
            for q in range(len(colour_palette)):
                if (len(colour_palette[q])>i):
                    i=len(colour_palette[q])
                    cq=q
            if cq!=Graph.nodes[u]["c"]:
                Graph.nodes[u]["c"]=cq
                Vc[cq].append(u)
                Un.remove(u)


        if (len(Un)==len(Un_pr)):
            break

    U_final=Unhappy_v(Graph,r)
    improved_v=len(U)-len(U_final)
    if (improved_v<0): #if the algorithm actually made more vertices unhappy
        Graph=G
        Vc=V
        improved_v=0

    end_time = time.process_time()
    pt=end_time-start_time
    #print('CPU runtime for the improvement algorithm:\t',pt)
    #print('Improved '+str(improved_v)+' vertices\n')
    return Graph,Vc,pt


def Repeated_Local_Search(G,V,lpc,r): #lpc=list of precoloured vertices
    '''The function performs a local search on the (partially) coloured graph G.
    The input is:
    G - a (coloured or partially coloured) NetworkX graph,
    V - list of lists of coloured vertices; the vertex v in the ith list means that v has the colour i,
    lpc - list of precoloured vertices, and
    r - the proportion of happiness.
    The output is
    Graph - a (coloured) NetworkX graph,
    Vc - updated list of list of colouring, and
    pt - the CPU runtime of the function.'''
    start_time=time.process_time()
    #st_real=time.time()
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    k=len(Vc)
    U=Unhappy_v(Graph,r)
    Un=[x for x in U if x not in lpc]
    Un1=copy.deepcopy(U)

   # j=0#counter of the while loop with consecutive no improvement
    while Un!=[]:
        Un_pr=copy.deepcopy(Un)
        for u in Un:
            colour_palette=[]
            for s in range(k):
                colour_palette.append([])
            for t in list(Graph.adj[u]):
                if (Graph.nodes[t]["c"]!=-1):
                    colour_palette[Graph.nodes[t]["c"]].append(t)
            i=0
            cq=-1
            for q in range(len(colour_palette)):
                if (len(colour_palette[q])>i):
                    i=len(colour_palette[q])
                    cq=q
            if cq!=Graph.nodes[u]["c"]:
                Graph.nodes[u]["c"]=cq
                Vc[cq].append(u)
                Un.remove(u)

        U=Unhappy_v(Graph,r)
        Un=[x for x in U if x not in lpc]
        if (Un==Un_pr):
            break

    U_final=Unhappy_v(Graph,r)
    improved_v=len(Un1)-len(U_final)
    if (improved_v<0): #if the algorithm actually made more vertices unhappy
        Graph=G
        Vc=V
        improved_v=0

    end_time = time.process_time()
    pt=end_time-start_time
    #print('CPU runtime for the improvement algorithm:\t',pt)
    #print('Improved '+str(improved_v)+' vertices\n')
    return Graph,Vc,pt


def Enhanced_Local_Search(G,V,lpc,r, TL): #lpc=list of precoloured vertices
    '''The function performs a deep local search on the (partially) coloured graph G.
    The input is:
    G - a (coloured or partially coloured) NetworkX graph,
    V - list of lists of coloured vertices; the vertex v in the ith list means that v has the colour i,
    lpc - list of precoloured vertices, and
    r - the proportion of happiness.
    TL - time limit
    The output is
    Graph - a (coloured) NetworkX graph,
    Vc - updated list of list of colouring, and
    pt - the CPU runtime of the function.'''
    start_time=time.process_time()
    #st_real=time.time()
    Graph=copy.deepcopy(G)
    Gbest=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    k=len(Vc)
    U=Unhappy_v(Graph,r)
    Un=[x for x in U if x not in lpc]


   # j=0#counter of the while loop with consecutive no improvement
    while (Un!=[] and (time.process_time()-start_time<TL)):
        Un_pr=copy.deepcopy(Un)
        for u in Un:
            colour_palette=[]
            for s in range(k):
                colour_palette.append([])
            for t in list(Graph.adj[u]):
                if (Graph.nodes[t]["c"]!=-1):
                    colour_palette[Graph.nodes[t]["c"]].append(t)
            i=0
            for q in range(k):
                if (len(colour_palette[q])>= r*Graph.degree[u]) and (time.process_time()-start_time<TL):
                    Graph.nodes[u]["c"]=q
                    if len(Happy_v(Gbest,r))<len(Happy_v(Graph,r)):
                        Gbest=copy.deepcopy(Graph)
                        Vc[q].append(u)
                        if u in Un:
                            Un.remove(u)

        # U1=Unhappy_v(Graph,r)
        # Un=[x for x in U1 if x not in lpc]
        # if (Un==Un_pr):
        #     break

    U_final=Unhappy_v(Graph,r)
    improved_v=len(U)-len(U_final)
    if (improved_v<0): #if the algorithim actually made more vertices unhappy
        Graph=G
        Vc=V
        improved_v=0

    end_time = time.process_time()
    pt=end_time-start_time
    #print('CPU runtime for the improvement algorithm:\t',pt)
    #print('Improved '+str(improved_v)+' vertices\n')
    return Graph,Vc,pt


def random_shuffle(Graph,lpc,k,t): #t= the number of vertices that are going to change their colours
    G=copy.deepcopy(Graph)
    n=G.number_of_nodes()
    free_vertices=[x for x in list(range(n)) if x not in lpc]
    A=[]
    for i in range(t):
        u=random.choice(free_vertices)
        A.append(u)
        free_vertices.remove(u)

    for v in A:
        B=list(range(k))
        if G.nodes[v]["c"]!=-1:
            B.remove(G.nodes[v]["c"])

        G.nodes[v]["c"]=random.choice(B)


    # for i in lpc:
    #     col[i]=Graph.nodes[i]["c"]

    Vp=Vertex_partition(G,k)

    return G, Vp
