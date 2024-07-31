import networkx as nx

import heapq 
def find_max_degrees(community, degrees):
    li = [(-1,-1), (-1,-1), (-1,-1)]
    heapq.heapify(li)
    for item in community:
        heapq.heappushpop(li, (degrees[item], item))

    return tuple([item for _, item in sorted(li, reverse=True)])



def find_max_degrees_for_communities(communities, dataset):
    degrees = dataset.degree()
    answer = []
    for community in communities:
        answer.append(find_max_degrees(community, degrees))
    return answer

