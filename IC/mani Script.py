import time
import matplotlib.pyplot as plt
import random
import networkx as nx
import numpy as np
from degreeDiscount import degreeDiscountIC
from randomHeuristic import randomHeuristic
from Algorithms import degreeHeuristic
from singleDiscount import singleDiscount
from IC import runIC
from clique1 import find_k_cliques
from generalGreedy import generalGreedy
import matplotlib.path as mpath

# Hybrid Influence Maximization Algorithm
def hybrid_influence_maximization(G, k):
    degree_nodes = degreeHeuristic(G, k, p=0.01)
    random_nodes = randomHeuristic(G, k, p=0.01)
    hybrid_nodes = list(set(degree_nodes + random_nodes))[:k]
    return hybrid_nodes

def getdata1(G1, G2, algo, maxk, p):
    assert isinstance(G1, nx.Graph), f"G1 should be a NetworkX Graph object, got {type(G1)}"
    assert isinstance(G2, nx.Graph), f"G2 should be a NetworkX Graph object, got {type(G2)}"
    
    S1 = list(G1.nodes)
    S2 = list(G2.nodes)

    if algo == hybrid_influence_maximization:
        S1_maxk = algo(G1, maxk)
        S2_maxk = algo(G2, maxk)
    else:
        S1_maxk = algo(G1, maxk, p)
        S2_maxk = algo(G2, maxk, p)
    
    S3 = []
    l = 0
    for i in range(maxk):
        if i < len(S1_maxk) and S1_maxk[i] in S2 and S1_maxk[i] not in S3:
            if l == maxk:
                return S3
            S3.append(S1_maxk[i])
            l += 1
        if i < len(S2_maxk) and S2_maxk[i] in S1 and S2_maxk[i] not in S3:
            if l == maxk:
                return S3
            S3.append(S2_maxk[i])
            l += 1
    return S3

def getData(G1, G2, maxk, algo, p, axis):
    assert isinstance(G1, nx.Graph), f"G1 should be a NetworkX Graph object, got {type(G1)}"
    assert isinstance(G2, nx.Graph), f"G2 should be a NetworkX Graph object, got {type(G2)}"
    
    algo_functions = {
        "randomHeuristic": randomHeuristic,
        "degreeDiscountIC": degreeDiscountIC,
        "generalGreedy": generalGreedy,
        "degreeHeuristic": degreeHeuristic,
        "singleDiscount": singleDiscount,
        "hybrid_influence_maximization": hybrid_influence_maximization
    }

    if algo == "find_k_cliques":
        F1 = find_k_cliques(G1, maxk, p)
        F2 = find_k_cliques(G2, maxk, p)
        S3 = getdata1(G1, G2, lambda g, k, p: list(g.nodes)[:k], maxk, p)
        print(f"F1: {F1}, F2: {F2}")  # Debug print
    else:
        if algo not in algo_functions:
            raise ValueError(f"Unknown algorithm: {algo}")
        S3 = getdata1(G1, G2, algo_functions[algo], maxk, p)

    data = dict()
    for k in range(maxk):
        if axis == "size" and algo in algo_functions:
            size1 = runIC(G1, S3[0:k+1], p)
            size2 = runIC(G2, S3[0:k+1], p)
            size = len(list(set(size1 + size2)))
            data[k] = size
            print(f"Algorithm: {algo}, k: {k}, Influenced Nodes: {size}")  # Debug print
    
    return data

def load_graph(file_path):
    G = nx.Graph()
    with open(file_path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                u, v = parts[1:3]  # Adjust based on file format
                if not G.has_edge(u, v):
                    G.add_edge(u, v, weight=random.random())
                else:
                    G[u][v]['weight'] += 1
    return G

if __name__ == "__main__":
    time2implement = time.time()
    time2build = time.time()
    
    G1 = load_graph(r'C:\Users\SIC-LAB\Downloads\influence-maximization-master\influence-maximization-master\graphdata\homogenetic1.txt')
    G2 = load_graph(r'C:\Users\SIC-LAB\Downloads\influence-maximization-master\influence-maximization-master\graphdata\homogenetic2.txt')

    fig = plt.figure()
    plot = []
    algor = ['singleDiscount', 'degreeDiscountIC', 'find_k_cliques', 'degreeHeuristic', 'randomHeuristic', 'hybrid_influence_maximization']
    shape = ['^', 'o', 'v', 'o', '^', 'D']
    col = ['orange', 'red', 'green', 'cyan', 'magenta', 'black']
    valid_algorithms = []
    
    for i in range(len(algor)):
        sha = ['-.', '', '.-', '.-', '--', ':']
        print(f"Running algorithm: {algor[i]}")  # Debug print
        data1 = getData(G1, G2, 50, algor[i], .01, "size")
        if not data1:
            print(f"No data for algorithm: {algor[i]}")  # Debug print
            continue
        valid_algorithms.append(i)
        star = mpath.Path.unit_regular_star(6)
        circle = mpath.Path.unit_circle()
        verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
        codes = np.concatenate([circle.codes, star.codes])
        cut_star = mpath.Path(verts, codes)
        d, = plt.semilogy(list(data1.keys()), list(data1.values()), sha[i], color=col[i])
        plot.append(d)
    
    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    plt.legend([plot[i] for i in range(len(plot))], [algor[i] for i in valid_algorithms], loc=9)
    plt.yscale('linear')
    plt.show()
    fig.savefig('influence_comparison.png', dpi=fig.dpi)
