import networkx as nx

def IsHappy(G,v,r):
    i=0
    for t in list(G.adj[v]):
        if (G.nodes[t]["c"]==G.nodes[v]["c"]):
            i+=1
    if (i<r*G.degree[v]):
        return False
    else:
        return True


def Happy_v(G,r):
    Hv=[]
    for v in list(G.nodes):
         if (IsHappy(G,v,r)==True):
             Hv.append(v)
    return Hv

def P_v(G,r):



#def U_v(G,r):
def L_p(G,r):

def L_h(G,r):


def L_u(G,r):

def L_f(G,r):


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

def growth_HC_r(G,V,U,r):
