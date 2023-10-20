import networkx as nx
import random

def IsHappy(G,v,r):
    i=0
    for t in list(G.adj[v]):
        if (G.nodes[t]["c"]==G.nodes[v]["c"]):
            i+=1
    if (i<r*G.degree[v]):
        return False
    else:
        return True

def CanBeHappy(G,v,r,k):
    i=0
    iu=0
    if (G.nodes[v]["c"]!="u"):
        for t in list(G.adj[v]):
            if (G.nodes[t]["c"]==G.nodes[v]["c"]):
                i+=1
            if (G.nodes[t]["c"]=="u"):
                iu+=1
    else:
        max_c=[]
        for s in range(k):
                    max_c.append([])
        for t in list(G.adj[v]):
            if (G.nodes[t]["c"]!="u"]):
                max_c[G.nodes[t]["c"]].append(t)
            else:
                iu+=1
        i=max(len(x) for x in max_c )
    return i+iu


def Happy_v(G,r):
    Hv=[]
    for v in list(G.nodes):
         if (IsHappy(G,v,r)==True):
             Hv.append(v)
    return Hv

def P_v(G,r,k):
    Pv=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]!="u" and IsHappy(G,v,r)==False and CanBeHappy(G,v,r,k)==True):
            Pv.append(v)
    return Pv


#def U_v(G,r):
#def L_p(G,r):


def L_h(G,r,k):
    Lh=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]=="u" and CanBeHappy(G,v,r,k)==True):
            Lh.append(v)
    return Lh
        
        


def L_u(G,r,k):
    Lu=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]=="u" and CanBeHappy(G,v,r,k)==Frue):
            Lu.append(v)
    return Lu

#def L_f(G,r):


def greedy1_HC_r(G,V,U,r):
    Graph=G
    Vc=V
    Uc=U
    k=len(Vc)
    m=0
    j=0
    for i in range(k):
        for u in Uc:
            Vc[i].add(u)
            Graph.nodes[u]["c"]=i
        nhv=len(Happy_v(Graph,r))
        if (m<nhv):
            m=nhv
            j=i
        for u in Uc:
            Vc[i].remove(u)
            Graph.nodes[u]["c"]=''

    for u in Uc:
        Vc[j].add(u)
        Graph.nodes[u]["c"]=j

    return Graph,Vc

def greedy2_HC_r(G,V,U,r):
    k=len(V)
    m=0
    j=0
    while (U!=set()):
        for i in range(k):
            for u in U:
                V[i].add(u)
                G.nodes[u]["c"]=i
            nhv=len(Happy_v(G,r))
            if (m<nhv):
                m=nhv
                j=i
            for u in U:
                V[i].remove(u)
                G.nodes[u]["c"]=''

        Nj=set()
        for v in V[j]:
            Nj=Nj.union(G.adj[v])
        Z=U.intersection(Nj)
        for u in Z:
            V[j].add(u)
            G.nodes[u]["c"]=j
            U.remove(u)
    return G,V


def greedy3_HC_r(G,V,U,r):
    k=len(V)
    m=0
    j=0
    for u in U:
        max_c=[]
        for s in range(k):
            max_c.append([])
        for t in list(G.adj[u]):
            if (G.nodes[t]["c"]!="u"]):
                max_c[G.nodes[t]["c"]].append(t)
        i=0
        cq='u'
        for q in range(len(max_c)):
            if (len(max_c[q])>i):
                i=len(max_c[q])
                cq=q
        G.nodes[u]["c"]=cq
        V[cq].add(u)
    U=set()
    return G,V
                    
       

def growth_HC_r(G,V,U,r):
    k=len(V)
    while (U!=set()):
        while (P_v(G,r,k)!=[]):
            v=random.choice(P_v(G,r,k))
            

        while (P_v(G,r,k)==[] and L_h(G,r,k)!=[]):

        while (P_v(G,r,k)==[] and L_h(G,r,k)==[] and L_u(G,r,k)!=[]):
            
    return G,V
