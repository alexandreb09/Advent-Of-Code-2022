from collections import deque
import numpy as np

def dijkstra(graph, vertex):
    queue = deque([vertex])
    distance = {vertex: 0}
    while queue:
        t = queue.popleft()
        for voisin in graph[t]:
                queue.append(voisin)
                nouvelle_distance = distance[t] + graph[t][voisin]
                if(voisin not in distance or nouvelle_distance < distance[voisin]):
                    distance[voisin] = nouvelle_distance
    return distance

def bfs(G, node) :
    parents = { node: None }
    file = [node]
    while file:
        node = file.pop(0)
        for node_child in G[node]:
            if node_child in parents: 
                continue
            parents[node_child] = node
            file.append(node_child)
    return parents

def bellmanFord(graph, sommetDepart):
    distances = {} 
    predecesseurs = {}
    for sommet in graph:
        distances[sommet] = np.inf
        predecesseurs[sommet] = None
    distances[sommetDepart] = 0
    
    for i in range(len(graph)-1):
        for j in graph:
            for k in graph[j]: 
                if distances[k] > distances[j] + graph[j][k]:
                    distances[k]  = distances[j] + graph[j][k]
                    predecesseurs[k] = j
    for i in graph:
        for j in graph[i]:
            assert distances[j] <= distances[i] + graph[i][j]
    return distances, predecesseurs