import networkx as nx
import math, random, copy, time

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
    j=i+iu
    if (j<r*G.degree[v]):
        return False
    else:
        return True


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
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    Uc=copy.deepcopy(U)
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
            Graph.nodes[u]["c"]='u'

    for u in Uc:
        Vc[j].add(u)
        Graph.nodes[u]["c"]=j

    return Graph,Vc

def greedy2_HC_r(G,V,U,r):
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    Uc=copy.deepcopy(U)
    k=len(Vc)
    m=0
    j=0
    while (Uc!=set()):
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
                Graph.nodes[u]["c"]='u'

        Nj=set()
        for v in Vc[j]:
            Nj=Nj.union(Graph.adj[v])
        Z=Uc.intersection(Nj)
        for u in Z:
            Vc[j].add(u)
            Graph.nodes[u]["c"]=j
            Uc.remove(u)
    return Graph,Vc


def greedy3_HC_r(G,V,U,r):
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    Uc=copy.deepcopy(U)
    Uc1=list(Uc)
    k=len(Vc)
    m=0
    j=0
    while Uc1!=[]:
        u=random.choice(Uc1)
        max_c=[]
        for s in range(k):
            max_c.append([])
        for t in list(Graph.adj[u]):
            if (Graph.nodes[t]["c"]!="u"):
                max_c[Graph.nodes[t]["c"]].append(t)
        i=0
        cq='u'
        for q in range(len(max_c)):
            if (len(max_c[q])>i):
                i=len(max_c[q])
                cq=q
        if cq!='u':
            Graph.nodes[u]["c"]=cq
            Vc[cq].add(u)
            Uc1.remove(u)
    return Graph,Vc
                    
       

def growth_HC_r(G,V,U,r):
    Graph=copy.deepcopy(G)
    Vc=copy.deepcopy(V)
    Uc=copy.deepcopy(U)
    k=len(Vc)
    while (Uc!=set()):
        A=P_v(Graph,r,k)
        while (A!=[]):
            v=random.choice(A)
            Up=list(set(Graph.adj[v]).intersection(Uc))
            if Up!=[]:
                i=0
                for u in list(Graph.adj[v]):
                    if (Graph.nodes[u]["c"]==Graph.nodes[v]["c"]):
                        i+=1
                t=math.ceil(r*Graph.degree[v])-i
                for j in range(t):
                    x=random.choice(Up)
                    Graph.nodes[x]["c"]=Graph.nodes[v]["c"]
                    Up.remove(x)
                    Uc.remove(x)
                    Vc[Graph.nodes[v]["c"]].add(x)
                A=P_v(Graph,r,k)

        B=L_h(Graph,r,k)
        while (A==[] and B!=[]):
            v=random.choice(B)
            Up=list(set(Graph.adj[v]).intersection(Uc))
            if Up!=[]:
                i=0
                for u in list(Graph.adj[v]):
                    if (Graph.nodes[u]["c"]==Graph.nodes[v]["c"]):
                        i+=1
                max_c=[]
                for s in range(k):
                    max_c.append([])
                for w in list(Graph.adj[v]):
                    if (Graph.nodes[w]["c"]!="u"):
                        max_c[Graph.nodes[w]["c"]].append(t)
                t=math.ceil(r*Graph.degree[v])-i
                l=0
                cq='u'
                for q in range(len(max_c)):
                    if (len(max_c[q])>l):
                        l=len(max_c[q])
                        cq=q
                for j in range(t):
                    if Up!=[]:
                        x=random.choice(Up)
                        Graph.nodes[x]["c"]=cq
                        Up.remove(x)
                        Uc.remove(x)
                        Vc[cq].add(x)
                Uc.remove(v)
                Vc[cq].add(v)
            A=P_v(Graph,r,k)
            B=L_h(Graph,r,k)
        C=L_u(Graph,r,k)
        while (A==[] and B==[] and C!=[]):
            v=random.choice(C)
            Up=list(set(Graph.adj[v]).intersection(Uc))
            if Up!=[]:
                i=0
                for u in list(Graph.adj[v]):
                    if (Graph.nodes[u]["c"]==Graph.nodes[v]["c"]):
                        i+=1
                max_c=[]
                for s in range(k):
                    max_c.append([])
                for w in list(Graph.adj[v]):
                    if (Graph.nodes[w]["c"]!="u"):
                        max_c[Graph.nodes[w]["c"]].append(t)
                t=math.ceil(r*G.degree[v])-i
                l=0
                cq='u'
                for q in range(len(max_c)):
                    if (len(max_c[q])>l):
                        l=len(max_c[q])
                        cq=q
                for j in range(t):
                    if Up!=[]:
                        x=random.choice(Up)
                        Graph.nodes[x]["c"]=cq
                        Up.remove(x)
                        Uc.remove(x)
                        Vc[cq].add(x)
                Uc.remove(v)
                Vc[cq].add(v)
            A=P_v(Graph,r,k)
            B=L_h(Graph,r,k)
            C=L_u(Graph,r,k)
    return Graph,Vc
