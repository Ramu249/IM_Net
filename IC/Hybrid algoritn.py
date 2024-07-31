import networkx as nx
import heapq

def dijkstra(graph, src):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[src] = 0
    priority_queue = [(0, src)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight['weight']
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def bellman_ford(graph, src):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[src] = 0
    
    for _ in range(len(graph.nodes) - 1):
        for u, v, weight in graph.edges.data('weight'):
            if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
    
    return distances

def floyd_warshall(graph):
    distances = dict(nx.all_pairs_dijkstra_path_length(graph))
    return distances

def hybrid_shortest_path(graph, src):
    if any(weight < 0 for _, _, weight in graph.edges.data('weight')):
        print("Using Bellman-Ford Algorithm")
        return bellman_ford(graph, src)
    
    if len(graph.edges) > len(graph.nodes)**2 // 2:
        print("Using Floyd-Warshall Algorithm")
        return floyd_warshall(graph)
    
    print("Using Dijkstra's Algorithm")
    return dijkstra(graph, src)

# Example usage:
G = nx.DiGraph()
edges = [
    (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7), (2, 8, 2), 
    (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10), (5, 6, 2), (6, 7, 1), 
    (6, 8, 6), (7, 8, 7)
]
for u, v, w in edges:
    G.add_edge(u, v, weight=w)

src = 0
distances = hybrid_shortest_path(G, src)
print("Shortest distances from node 0 to all other nodes:")
print(distances)
