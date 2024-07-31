import time
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.path as mpath
import random

# Import or define the algorithms here
from degreeDiscount import degreeDiscountIC
from randomHeuristic import randomHeuristic
from Algorithms import degreeHeuristic
from singleDiscount import singleDiscount
from IC import runIC
from clique1 import find_k_cliques
from generalGreedy import generalGreedy

# Refined Hybrid Influence Maximization Algorithm
def refined_hybrid_influence_maximization(G, k):
    # Degree Heuristic part
    degree_nodes = degreeHeuristic(G, k, p=0.01)
    
    # Random Heuristic part
    random_nodes = randomHeuristic(G, k, p=0.01)
    
    # Hybrid Combination: Prioritize Degree Heuristic, then Random Heuristic
    combined_nodes = list(set(degree_nodes + random_nodes))[:k]
    
    # Additional refinement: Remove duplicates and validate
    unique_nodes = []
    seen = set()
    for node in combined_nodes:
        if node not in seen:
            seen.add(node)
            unique_nodes.append(node)
    
    return unique_nodes[:k]

# Algorithm function mappings
algo_functions = {
    "singleDiscount": singleDiscount,
    "degreeDiscountIC": degreeDiscountIC,
    "find_k_cliques": find_k_cliques,
    "degreeHeuristic": degreeHeuristic,
    "randomHeuristic": randomHeuristic,
    "refined_hybrid_influence_maximization": refined_hybrid_influence_maximization
}

def getdata1(G1, G2, algo, maxk, p):
    if algo == refined_hybrid_influence_maximization:
        S1_maxk = algo(G1, maxk)
        S2_maxk = algo(G2, maxk)
    else:
        if algo not in algo_functions:
            raise ValueError(f"Unknown algorithm: {algo}")
        S1_maxk = algo_functions[algo](G1, maxk, p)
        S2_maxk = algo_functions[algo](G2, maxk, p)
    
    S3 = []
    l = 0
    for i in range(maxk):
        if S1_maxk[i] in G2.nodes and S1_maxk[i] not in S3:
            if l == maxk:
                return S3
            S3.append(S1_maxk[i])
            l += 1
        if S2_maxk[i] in G1.nodes and S2_maxk[i] not in S3:
            if l == maxk:
                return S3
            S3.append(S2_maxk[i])
            l += 1
    return S3

def getData(G1, G2, maxk, algo, p, axis):
    if algo == "find_k_cliques":
        F1 = find_k_cliques(G1, maxk, p)
        F2 = find_k_cliques(G2, maxk, p)
        S3 = getdata1(G1, G2, lambda g, k, p: list(g.nodes)[:k], maxk, p)
    else:
        if algo not in algo_functions:
            raise ValueError(f"Unknown algorithm: {algo}")
        S3 = getdata1(G1, G2, algo_functions[algo], maxk, p)

    data = dict()
    for k in range(maxk):
        if axis == "size" and algo in algo_functions:
            size1 = runIC(G1, S3[0:k+1], p)
            size2 = runIC(G2, S3[0:k+1], p)
            size = len(set(size1 + size2))
            data[k] = size
    
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
    algor = ['singleDiscount', 'degreeDiscountIC', 'find_k_cliques', 'degreeHeuristic', 'randomHeuristic', 'refined_hybrid_influence_maximization']
    shape = ['^', 'o', 'v', 'o', '^', 'D']
    col = ['orange', 'red', 'green', 'cyan', 'magenta', 'black']
    
    for i in range(len(algor)):
        sha = ['-.', '', '.-', '.-', '--', ':']
        try:
            print(f"Running algorithm: {algor[i]}")  # Debugging line
            data1 = getData(G1, G2, 50, algor[i], .01, "size")
            if data1:  # Check if data1 is not empty
                print(f"Data for {algor[i]}: {data1}")  # Debugging line
                star = mpath.Path.unit_regular_star(6)
                circle = mpath.Path.unit_circle()
                verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
                codes = np.concatenate([circle.codes, star.codes])
                cut_star = mpath.Path(verts, codes)
                d, = plt.semilogy(list(data1.keys()), list(data1.values()), sha[i], color=col[i])
                plot.append(d)
            else:
                print(f"No data for {algor[i]}")  # Debugging line
        except ValueError as e:
            print(f"Error with algorithm {algor[i]}: {e}")

    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    if plot:
        plt.legend([plot[i] for i in range(len(plot))], ["Single Discount", "Degree Discount", "Find k Cliques", "Degree Heuristic", "Random Heuristic", "Refined Hybrid Influence Maximization"], loc=9)
    plt.yscale('linear')
    plt.show()
    fig.savefig('influence_comparison.png', dpi=fig.dpi)
