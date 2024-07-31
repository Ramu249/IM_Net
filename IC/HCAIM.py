#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
from degreeDiscount import degreeDiscountIC
import random
from randomHeuristic import randomHeuristic
from Algorithms import degreeHeuristic
import matplotlib.path as mpath
import numpy as np
from singleDiscount import singleDiscount
from IC import runIC
from clique1 import find_k_cliques
from generalGreedy import generalGreedy
from community import community_louvain
import networkx as nx

# Define the hybrid influence maximization algorithm
def hcaim_algorithm(G, k, p):
    partition = community_louvain.best_partition(G)
    communities = {}
    for node, comm in partition.items():
        if comm not in communities:
            communities[comm] = []
        communities[comm].append(node)

    heuristic_scores = calculate_heuristic_scores(G)
    similarity_scores = calculate_similarity_scores(G)
    
    all_seeds = []
    for community_nodes in communities.values():
        seeds = hybrid_seed_selection(community_nodes, k, heuristic_scores, similarity_scores)
        all_seeds.extend(seeds)

    seeds = refine_seeds_across_communities(seeds, k, all_seeds)
    
    # Calculate influence
    influenced_nodes = set()
    for seed in seeds:
        influenced_nodes.add(seed)
        neighbors = set(G.neighbors(seed))
        influenced_nodes.update(neighbors)
    
    influence_count = len(influenced_nodes)

    return seeds, influence_count

def calculate_heuristic_scores(G):
    return nx.betweenness_centrality(G)

def calculate_similarity_scores(G):
    return dict(G.degree())

def hybrid_seed_selection(nodes, k, heuristic_scores, similarity_scores):
    combined_scores = {}
    for node in nodes:
        heuristic_score = heuristic_scores.get(node, 0)
        similarity_score = similarity_scores.get(node, 0)
        combined_scores[node] = 0.6 * heuristic_score + 0.4 * similarity_score

    seeds = sorted(combined_scores, key=combined_scores.get, reverse=True)[:k]
    return seeds

def refine_seeds_across_communities(seeds, k, all_seeds):
    unique_seeds = list(set(all_seeds))
    refined_seeds = unique_seeds[:k]
    return refined_seeds

def getData(G1, G2, maxk, algo, p, axis):
    print(f"Running {algo}...")
    S3 = ""
    if algo == "find_k_cliques":
        F1 = find_k_cliques(G1, maxk, p)
        F2 = find_k_cliques(G2, maxk, p)
        S1 = list(G1.nodes)
        S2 = list(G2.nodes)
        S3 = getdata2(F1, F2, S1, S2, maxk)
    elif algo == "randomHeuristic":
        S3 = getdata1(G1, G2, randomHeuristic, maxk, p)
    elif algo == "degreeDiscountIC":
        S3 = getdata1(G1, G2, degreeDiscountIC, maxk, p)
    elif algo == "generalGreedy":
        S3 = getdata1(G1, G2, generalGreedy, maxk, p)
    elif algo == "degreeHeuristic":
        S3 = getdata1(G1, G2, degreeHeuristic, maxk, p)
    elif algo == "singleDiscount":
        S3 = getdata1(G1, G2, singleDiscount, maxk, p)
    elif algo == "hcaim_algorithm":
        seeds, influence_count = hcaim_algorithm(G1, maxk, p)
        S3 = seeds

    print(f"S3 (Seed Nodes): {S3}")

    data = dict()
    for k in range(maxk):
        if axis == "size":
            size1 = runIC(G1, S3[0:k+1], p)
            size2 = runIC(G2, S3[0:k+1], p)
            size = len(list(set(size1 + size2)))
            data[k] = size

    print(f"Data for {algo}: {data}")
    return data

def getdata1(G1, G2, algo, maxk, p):
    S1 = list(G1.nodes)
    S2 = list(G2.nodes)
    S1_maxk = algo(G1, maxk, p)
    S2_maxk = algo(G2, maxk, p)
    S3 = []
    l = 0
    for i in range(maxk):
        for j in range(len(S2)):
            if S1_maxk[i] == S2[j]:
                if S1_maxk[i] not in S3:
                    if l == maxk:
                        return S3
                    else:
                        S3.append(S1_maxk[i])
                        l += 1
                break
        for j in range(len(S1)):
            if S2_maxk[i] == S1[j]:
                if S2_maxk[i] not in S3:
                    if l == maxk:
                        return S3
                    else:
                        S3.append(S2_maxk[i])
                        l += 1
                break
    return S3

def getdata2(F1, F2, S1, S2, maxk):
    F3 = []
    l = 0
    for i in range(maxk):
        for j in range(len(S2)):
            if F1[i] == S2[j]:
                if F1[i] not in F3:
                    if l == maxk:
                        return F3
                    else:
                        F3.append(F1[i])
                        l += 1
        for j in range(len(S1)):
            if F2[i] == S1[j]:
                if F2[i] not in F3:
                    if l == maxk:
                        return F3
                    else:
                        F3.append(F2[i])
                        l += 1
    return F3

if __name__ == "__main__":
    time2build = time.time()
    G1 = nx.Graph()
    with open(r'C:\Users\SIC-LAB\Downloads\influence-maximization-master\influence-maximization-master\graphdata\homogenetic1.txt') as f:
        data = f.readlines()
        for line in data:
            u, v = line.split(" ")[1], line.split(" ")[2]
            try:
                G1[u][v]['weight'] += 1
            except:
                G1.add_edge(u, v, weight=random.random())
    
    G2 = nx.Graph()
    with open(r'C:\Users\SIC-LAB\Downloads\influence-maximization-master\influence-maximization-master\graphdata\homogenetic2.txt') as f:
        data = f.readlines()
        for line in data:
            u, v = line.split(" ")[1], line.split(" ")[2]
            try:
                G2[u][v]['weight'] += 1
            except:
                G2.add_edge(u, v, weight=random.random())

    fig = plt.figure()
    plot = []
    algor = ['singleDiscount', 'degreeDiscountIC', 'find_k_cliques', 'degreeHeuristic', 'randomHeuristic', 'hcaim_algorithm']
    shape = ['^', 'o', 'v', 'o', '^', 's']
    col = ['orange', 'red', 'green', 'cyan', 'magenta', 'blue']

    for i in range(len(algor)):
        sha = ['-.', '', '.-', '.-', '--', '-']
        data1 = getData(G1, G2, 50, algor[i], .01, "size")
        print(f"Data1 for {algor[i]}: {data1}")
        d, = plt.semilogy(list(data1.keys()), list(data1.values()), sha[i], color=col[i])
        plot.append(d)

    plt.xlabel("Seed set size k")
    plt.ylabel("# of Influenced nodes")
    plt.legend([plot[0], plot[1], plot[2], plot[3], plot[4], plot[5]], ["Single Discount", "Degree Discount", "Find k Cliques", "Degree Heuristic", "Random Heuristic", "HCAIM"], loc=9)
    plt.yscale('linear')
    plt.show()
    fig.savefig('413.png', dpi=fig.dpi)
