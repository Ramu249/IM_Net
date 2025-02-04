''' Independent cascade model for influence propagation
'''
__author__ = 'ivanovsergey'

def runIC (G, S, p = .01):
    ''' Runs independent cascade model.
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    '''
    from copy import deepcopy
    from random import random
    T = deepcopy(S) # copy already selected nodes

    # ugly C++ version
    i = 0
    while i < len(T):
        for v in G[T[i]]: # for neighbors of a selected node
            if v not in T: # if it wasn't selected yet
                w = G[T[i]][v]['weight'] # count the number of edges between two nodes
                #m=random()
                #l=random()
                #l= 1 - (1-p)**w
                #print(m, "and", l)
                #print(1-(1-p)**w) 
                if 0.0194451854525 <= 1 - (1-p)**w: # if at least one of edges propagate influence
                # Sacch - 0.0099450, cele- 0.01931854525
                #if m <= l: 0.0094521
                    #print (T[i], 'influences', v)
                    T.append(v)
        i += 1

    # neat pythonic version
    # legitimate version with dynamically changing list: http://stackoverflow.com/a/15725492/2069858
    # for u in T: # T may increase size during iterations
    #     for v in G[u]: # check whether new node v is influenced by chosen node u
    #         w = G[u][v]['weight']
    #         if v not in T and random() < 1 - (1-p)**w:
    #             T.append(v)
    return T

def runIC3 (G, S, p = .01):
    
    from copy import deepcopy
    from random import random
    #T = deepcopy(S)
    T=list(S)
    k=len(S)
    #print("length",k)
    #print(type(S))
    i = 0
    
    while i< len(T):
        for v in G[T[i]]:
            #w = G[T[i]][v]['weight']
            #print(1 - (1-p)**w)
            #print(k)
            if v not in T:
                w = G[T[i]][v]['weight']
                if random() < 1 - (1-p)**w:
            # for 10,3, 0.5 and seed 5 then 0.0089, 50,4, 0.5 and seed 30 then 0.009902
            #if v not in T and 0.5 < w:    
                #print('hai')
                    T.append(v)
                    k=k+1
    #print(len(T))
        i += 1
    return len(T)


def runIC4 (G, S, p = .01):
    
    from copy import deepcopy
    from random import random
    #T = deepcopy(S)
    T=list(S)
    k=len(S)
    #print("length",k)
    #print(type(S))
    i = 0
    
    for u in T:
        for v in G[u]:
            w = G[T[i]][v]['weight']
            #print(1 - (1-p)**w)
            #print(k)
            #d=random()
            #print(d)
            if v not in T and 0.003452<1 - (1-p)**w: #< 1 - (1-p)**w['weight']:
            #if v not in T and random() < 1 - (1-p)**w['weight']:
            # for 10,3, 0.5 and seed 5 then 0.0089, 50,4, 0.5 and seed 30 then 0.009902
            #if v not in T and 0.5 < w:    
                #print('hai')
                T.append(v)
                k=k+1
    #print(len(T))            
    return T




def runIC2(G, S, p=.01):
    ''' Runs independent cascade model (finds levels of propagation).
    Let A0 be S. A_i is defined as activated nodes at ith step by nodes in A_(i-1).
    We call A_0, A_1, ..., A_i, ..., A_l levels of propagation.
    Input: G -- networkx graph object
    S -- initial set of vertices
    p -- propagation probability
    Output: T -- resulted influenced set of vertices (including S)
    '''
    from copy import deepcopy
    import random
    T = deepcopy(S)
    Acur = deepcopy(S)
    Anext = []
    i = 0
    while Acur:
        values = dict()
        for u in Acur:
            for v in G[u]:
                if v not in T:
                    w = G[u][v]['weight']
                    if random.random() < 1 - (1-p)**w:
                        Anext.append((v, u))
        Acur = [edge[0] for edge in Anext]
        print (i, Anext)
        i += 1
        T.extend(Acur)
        Anext = []
    return T
    
def avgSize(G,S,p,iterations):
    avg = 0
    for i in range(iterations):
        avg += float(len(runIC4(G,S,p)))/iterations
    return avg
