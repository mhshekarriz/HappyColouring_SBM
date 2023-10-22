import networkx as nx
import random
import math

def IsHappy(G,v,r): #checks whether the vertex v is r-happy or not
    i=0
    for t in list(G.adj[v]):
        if (G.nodes[t]["c"]==G.nodes[v]["c"]):
            i+=1
    if (i<r*G.degree[v]):
        return False
    else:
        return True

def CanBeHappy(G,v,r,k): #Checks if the vertex v can be r-happy if there are k colours
    i=0
    iu=0
    if (G.nodes[v]["c"]!="u"): #if v is not coloured yet
        for t in list(G.adj[v]):
            if (G.nodes[t]["c"]==G.nodes[v]["c"]):
                i+=1
            if (G.nodes[t]["c"]=="u"):
                iu+=1
    else: #if v is already coloured
        max_c=[]
        for s in range(k):
                    max_c.append([])
        for t in list(G.adj[v]):
            if (G.nodes[t]["c"]!="u"):
                max_c[G.nodes[t]["c"]].append(t)
            else:
                iu+=1
        i=max(len(x) for x in max_c )
    return i+iu


def Happy_v(G,r): #gives the list of r-happy vertices in a partially coloured graph G
    Hv=[]
    for v in list(G.nodes):
         if (IsHappy(G,v,r)==True):
             Hv.append(v)
    return Hv

def P_v(G,r,k): #gives the list of P-vertices
    Pv=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]!="u" and IsHappy(G,v,r)==False and CanBeHappy(G,v,r,k)==True):
            Pv.append(v)
    return Pv


#def U_v(G,r):
#def L_p(G,r):


def L_h(G,r,k): #gives the list of L_h vertices
    Lh=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]=="u" and CanBeHappy(G,v,r,k)==True):
            Lh.append(v)
    return Lh
        
        


def L_u(G,r,k): #gives the list of L_u vertices
    Lu=[]
    for v in list(G.nodes):
        if (G.nodes[v]["c"]=="u" and CanBeHappy(G,v,r,k)==False):
            Lu.append(v)
    return Lu

#def L_f(G,r):


def greedy1_HC_r(G,V,U,r): #the greedy algorithm as it is mentioned in Peng Zhang and Angsheng Li. Algorithmic aspects of homophyly of networks. Theoretical Computer Science, 593:117–131, 2015
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
            if (G.nodes[t]["c"]!="u"):
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
        A=P_v(G,r,k)
        while (A!=[]):
            v=random.choice(A)
            Up=list(G.adj(v)).intersection(U)
            i=0
            for u in list(G.adj(v)):
                if (G.nodes[u]["c"]==G.nodes[v]["c"]):
                    i+=1
            t=math.ceil(r*G.deg(v))-i
            for j in range(t):
                x=random.choice(Up)
                G.nodes[x]["c"]=G.nodes[v]["c"]
                Up.remove(x)
                U.remove(x)
                V[G.nodes[v]["c"]].append(x)
            A=P_v(G,r,k)
        B=L_h(G,r,k)
        while (A==[] and B!=[]):
            v=random.choice(B)
            Up=list(G.adj(v)).intersection(U)
            i=0
            for u in list(G.adj(v)):
                if (G.nodes[u]["c"]==G.nodes[v]["c"]):
                    i+=1
            max_c=[]
            for s in range(k):
                max_c.append([])
            for w in list(G.adj[v]):
                if (G.nodes[w]["c"]!="u"):
                    max_c[G.nodes[w]["c"]].append(t)
            t=math.ceil(r*G.deg(v))-i
            l=0
            cq='u'
            for q in range(len(max_c)):
                if (len(max_c[q])>l):
                    l=len(max_c[q])
                    cq=q
            U.remove(v)
            V[cq].append(v)
            for j in range(t):
                x=random.choice(Up)
                G.nodes[x]["c"]=cq
                Up.remove(x)
                U.remove(x)
                V[cq].append(x)
            A=P_v(G,r,k)
            B=L_h(G,r,k)
        C=L_u(G,r,k)
        while (A==[] and B==[] and C!=[]):
            v=random.choice(C)
            Up=list(G.adj(v)).intersection(U)
            i=0
            for u in list(G.adj(v)):
                if (G.nodes[u]["c"]==G.nodes[v]["c"]):
                    i+=1
            max_c=[]
            for s in range(k):
                max_c.append([])
            for w in list(G.adj[v]):
                if (G.nodes[w]["c"]!="u"):
                    max_c[G.nodes[w]["c"]].append(t)
            t=math.ceil(r*G.deg(v))-i
            l=0
            cq='u'
            for q in range(len(max_c)):
                if (len(max_c[q])>l):
                    l=len(max_c[q])
                    cq=q
            U.remove(v)
            V[cq].append(v)
            for j in range(t):
                x=random.choice(Up)
                G.nodes[x]["c"]=cq
                Up.remove(x)
                U.remove(x)
                V[cq].append(x)
            A=P_v(G,r,k)
            B=L_h(G,r,k)
            C=L_u(G,r,k)
    return G,V
