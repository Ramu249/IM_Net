import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from community import community_louvain

def calculate_heuristic_scores(G):
    # Example heuristic function to calculate node scores
    return {node: np.random.random() for node in G.nodes()}

def calculate_similarity_scores(G):
    # Example similarity function to calculate node similarity scores
    return {node: np.random.random() for node in G.nodes()}

def hybrid_seed_selection(nodes, k, G):
    heuristic_scores = calculate_heuristic_scores(G)
    similarity_scores = calculate_similarity_scores(G)
    
    # Example heuristic seeds (based on heuristic scores)
    heuristic_seeds = sorted(nodes, key=lambda x: heuristic_scores[x], reverse=True)

    # Combine scores
    combined_scores = {}
    for node in nodes:
        heuristic_score = heuristic_scores.get(node, 0)  # Default to 0 if node not found
        similarity_score = similarity_scores.get(node, 0)  # Default to 0 if node not found
        combined_scores[node] = 0.7 * heuristic_score + 0.3 * similarity_score

    # Select top k nodes based on combined scores
    seeds = sorted(combined_scores, key=combined_scores.get, reverse=True)[:k]

    return seeds

def hcaim_algorithm(G, k, p, thresholds):
    # Find communities using Louvain method
    partition = community_louvain.best_partition(G)
    communities = {}
    for node, comm in partition.items():
        if comm not in communities:
            communities[comm] = []
        communities[comm].append(node)

    # Apply hybrid seed selection within each community
    all_seeds = []
    for community_nodes in communities.values():
        seeds = hybrid_seed_selection(community_nodes, k, G)
        all_seeds.extend(seeds)

    # Return top k seeds across all communities
    unique_seeds = list(set(all_seeds))
    seeds = unique_seeds[:k]

    # Calculate influence spread (example placeholder)
    influence = np.random.random()

    return seeds, influence

def visualize_seeds(graph, seed_sets):
    pos = nx.spring_layout(graph)
    
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color='lightgrey', edge_color='grey')

    for algo, seeds in seed_sets.items():
        # Check that all seeds are in the graph
        valid_seeds = [seed for seed in seeds if seed in graph.nodes()]
        nx.draw_networkx_nodes(graph, pos, nodelist=valid_seeds, node_color='red', node_size=800, label=algo)
    
    plt.legend()
    plt.title("Seed Nodes Visualization")
    plt.show()

if __name__ == "__main__":
    # Create a sample graph (replace with actual graph data)
    G = nx.erdos_renyi_graph(20, 0.2)

    k = 10  # Number of seed nodes
    p = 0.1  # Propagation probability (example placeholder)
    thresholds = {}  # Example threshold dictionary (modify as needed)

    seeds, influence = hcaim_algorithm(G, k, p, thresholds)

    print("Selected Seed Nodes:", seeds)
    print("Estimated Influence:", influence)

    # Example seed sets
    seed_sets = {
        "HCAIM_1": seeds,
        "KSN": [1, 2, 3],
        "IMCS": [4, 5, 6],
        "Additional_1": [0, 1, 3, 5, 6, 8, 11, 12, 13, 14],
        "Additional_2": [0, 1, 3, 4, 7, 8, 9, 10, 11, 12]
    }

    # Visualize the seed nodes
    visualize_seeds(G, seed_sets)
