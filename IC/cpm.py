from collections import defaultdict
import networkx as nx
import operator

'''
paper : <<Uncovering the overlapping community structure of complex networks in nature and society>>
'''

    
# def __init__(self,G,k=4):
#     self._G = G
#     self._k = k

def CPM(G,k,p):
    # find all cliques which size > k
    cliques = list(nx.find_cliques(G))
    vid_cid = defaultdict(lambda:set())
    for i,c in enumerate(cliques):
        if len(c) < k:
            continue
        for v in c:
            vid_cid[v].add(i)

    # build clique neighbor
    clique_neighbor = defaultdict(lambda:set())
    remained = set()
    for i,c1 in enumerate(cliques):
        #if i % 100 == 0:
            #print i
        if len(c1) < k:
            continue
        remained.add(i)
        s1 = set(c1)
        candidate_neighbors = set()
        for v in c1:
            candidate_neighbors.update(vid_cid[v])
        candidate_neighbors.remove(i)
        for j in candidate_neighbors:
            c2 = cliques[j]
            if len(c2) < k:
                continue
            if j < i:
                continue
            s2 = set(c2)
            if len(s1 & s2) >= min(len(s1),len(s2)) -1:
                clique_neighbor[i].add(j)
                clique_neighbor[j].add(i) 

    # depth first search clique neighbors for communities
    communities = []
    for i,c in enumerate(cliques):
        if i in remained and len(c) >= k:
            #print 'remained cliques', len(remained)
            communities.append(set(c))
            neighbors = list(clique_neighbor[i])
            while len(neighbors) != 0:
                n = neighbors.pop()
                if n in remained:
                    #if len(remained) % 100 == 0:
                        #print 'remained cliques', len(remained)
                    communities[len(communities)-1].update(cliques[n])
                    remained.remove(n)
                    for nn in clique_neighbor[n]:
                        if nn in remained:
                            neighbors.append(nn)
#     sample=list(range(1,51))
#     return sample
    #return communities
    result=[]
    resultdegree=[]
    for community in communities:
        for i in community:
            result.append(i)
            resultdegree.append(G.degree[i])
    res = dict(zip(result, resultdegree))
    sorted_res = sorted(res.items(), key=operator.itemgetter(1))
    whatwewant=[]
    for k,v in sorted_res:
        whatwewant.append(k)
        
#     print(whatwewant)           #sorted all according to the degree of their in network.
    
    final=whatwewant[:50]
    return final
#     print(len(final))
#     print(len(res))
    
#     print(len(result))
#     print(len(resultdegree))
#     print(sorted_res)
#         print(community)
        
if __name__ == '__main__':
    console = []
#     import random as random
#     G1=nx.Graph()
#     with open(r'C:\Users\samin\OneDrive\Desktop\work\influence-maximization-master\influence-maximization-master\graphdata\celega1.txt') as f:
#         data = f.readlines()
#         for line in data:
#                     #coloumn2.append(line.split(" ")[1])
#                     u=line.split(" ")[1]
#                     v=line.split(" ")[2]
#                     try:
#                         G1[u][v]['weight'] += 1
#                     except:
#                         #G1.add_edge(u,v, weight=1)
#                         G1.add_edge(u,v, weight=random.random())
#     CPM(G1,4)
#     G = nx.karate_club_graph()
#     algorithm = CPM(G, 4)
#     communities = algorithm.execute()
#     for community in communities:
#         print(community)
