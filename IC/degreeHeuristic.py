''' Implementation of degree heuristic[1] for Independent Cascade model
of influence propagation in graph G.
Takes k nodes with the largest degree.

[1] -- Wei Chen et al. Efficient influence maximization in Social Networks
'''
__author__ = 'ivanovsergey'
from priorityQueue import PriorityQueue as PQ # priority queue

def degreeHeuristic(G, k, p=.01):
    ''' Finds initial set of nodes to propagate in Independent Cascade model (with priority queue)
    Input: G -- networkx graph object
    k -- number of nodes needed
    p -- propagation probability
    Output:
    S -- chosen k nodes
    '''
    S = []
    d = PQ()
    for u in G:
        degree = sum([G[u][v]['weight'] for v in G[u]])
        # degree = len(G[u])
        d.add_task(u, -degree)
    for i in range(k):
        u, priority = d.pop_item()
        S.append(u)
    return S[0:10]

def Avg(G1,G2,k):
    g1=dict(G1.degree)
    g2=dict(G2.degree)
    max1=max(g1,key=int)
    max2=max(g2,key=int)
    g1=list(G1.degree)
    g2=list(G2.degree)
    data1=[]
    if(max2>max1):
        for l in range(max2+1):
            a=[]
            x=0
            for j in range(len(g1)):
                if(l==g1[j][0]):
                    x=x+g1[j][1]
                    break
            for j in range(len(g2)):
                if(l==g2[j][0]):
                    x=x+g2[j][1]
                    break
            a.append(l)
            a.append(x)
            data1.append(a)
    else:
        for l in range(max1+1):
            a=[]
            x=0
            for j in range(len(g1)):
                if(l==g1[j][0]):
                    x=x+g1[j][1]
                    break
            for j in range(len(g2)):
                if(l==g2[j][0]):
                    x=x+g2[j][1]
                    break
            a.append(l)
            a.append(x)
            data1.append(a)
    temp1=dict(data1)
    final1=[]
    for i in range(len(temp1)):
        u=max(temp1,key=temp1.get)
        degree=max(temp1.values())
        temp1.pop(u)
        final1.append(u)
    #print(final1[0:k])
    return final1[0:k]

def degreeHeuristic2(G, p=.01):
    ''' Finds initial set of nodes to propagate in Independent Cascade model (without priority queue)
    Input: G -- networkx graph object
    k -- number of nodes needed
    p -- propagation probability
    Output:
    S -- chosen k nodes
    '''
    S = []
    d = dict()
    for u in G:
        degree = sum([G[u][v]['weight'] for v in G[u]])
        # degree = len(G[u])
        d[u] = degree
    for i in range(G.number_of_nodes()):
        u=max(d,key=d.get)
        degree=max(d.values())
        #print(degree)
        d.pop(u)
        a=[]
        a.append(u)
        a.append(degree)
        S.append(a)
    #print(S)
    return S[0:10]
