import networkx as nx
import numpy as np
from community import community_louvain
import matplotlib.pyplot as plt

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

def him_cr_algorithm(G, k):
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
    
    # Calculate influence (number of influenced nodes)
    influenced_nodes = set()
    for seed in seeds:
        influenced_nodes.add(seed)
        # Simulate influence propagation (this is a placeholder)
        # In real scenarios, this should be replaced with actual diffusion model computations
        neighbors = set(G.neighbors(seed))
        influenced_nodes.update(neighbors)
    
    influence_count = len(influenced_nodes)

    return seeds, influence_count

if __name__ == "__main__":
    # Generate a larger graph
    G = nx.barabasi_albert_graph(1000, 10)  # 1000 nodes, 10 edges per node

    seed_sizes = range(10, 101, 10)  # Seed sizes from 10 to 100
    influences = []

    for size in seed_sizes:
        _, influence_count = him_cr_algorithm(G, size)
        influences.append(influence_count)
    
    # Plot the results
    plt.figure(figsize=(12, 8))
    plt.plot(seed_sizes, influences, marker='o', linestyle='-', color='b')
    plt.xlabel('Seed Set Size')
    plt.ylabel('Number of Influenced Nodes')
    plt.title('Seed Set Size vs. Number of Influenced Nodes')
    plt.grid(True)
    plt.show()
