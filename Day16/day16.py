import sys
sys.path.insert(1, r'D:\Informatique\AdventOfCode\utils')

from dataclasses import dataclass
import re
import itertools
import random
import pickle

from utils import bellmanFord



global TIME_MAX, START_NODE

@dataclass(frozen=True, eq=True)
class Node:
    name: str
    flow: int

class Solution:
    def __init__(self, node, nodes, distances_all) -> None:
        self.current_node = node 
        self.visited_points = node.name
        self.next_nodes = { node.name: node for node in nodes }
        self.time = 1
        self.flow = 0
        self.total = 0
        self.score_max = 0
        self.compute_score_max(distances_all)
    
    #   t     T  t+d
    #   |     |   |    
    def move_to_point(self, node, distances_all):
        if node == None: return

        self.visited_points += "-" + node.name

        distance_to_point = distances_all[self.current_node.name][node.name]
        distance_to_point = TIME_MAX - self.time if self.time + distance_to_point > TIME_MAX else distance_to_point

        self.total += distance_to_point * self.flow
        self.time += distance_to_point
        if self.time < TIME_MAX:
            self.time += 1
            self.flow += node.flow
            self.total += self.flow

        self.current_node = node
        del self.next_nodes[node.name]
        self.compute_score_max(distances_all)

    def get_score(self):
        return self.total + max(TIME_MAX - self.time, 0) * self.flow
    
    def get_next_nodes(self):
        return self.next_nodes.values()

    def get_score_max(self):
        return self.score_max

    def compute_score_max(self, distances_all):
        next_nodes = self.get_next_nodes()
        self.score_max = self.get_score()
        min_distance = min((distances_all[self.current_node.name][next_node.name] for next_node in next_nodes), default=0) - 1
        # t     t+d        T
        # |      |         |
        for next_node in next_nodes:
            self.score_max += max((TIME_MAX - self.time - min_distance - 1), 0) * next_node.flow



    def __str__(self) -> str:
        return "score: {} using {}".format(self.get_score(), self.visited_points)

class SolutionSet:
    def __init__(self, solutions) -> None:
        self.solutions = solutions

    def get_next_nodes_pair(self):
        next_nodes_2d = [solution.get_next_nodes() for solution in self.solutions]
        candidates = set.intersection(*map(set,next_nodes_2d)) 
        # if len(candidates) == 1: candidates = candidates | set([None])
        return itertools.permutations(candidates, len(self.solutions))

    def get_score(self):
        return sum(solution.get_score() for solution in self.solutions)

    def move_to_point(self, node_pair, distances_all):
        for next_node, solution in zip(node_pair, self.solutions):
            solution.move_to_point(next_node, distances_all)
    
    def canImprove(self, current_best_score):
        if all(solution.time > TIME_MAX for solution in self.solutions):
            return False
        score_max_possible = sum(solution.get_score_max() for solution in self.solutions)
        return score_max_possible > current_best_score

    def __str__(self) -> str:
        return " ".join(solution.visited_points for solution in self.solutions)

def read_data(filename, start_node_name, display=True):
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]

    graph = {}
    graph_distances = {}
    for line in lines:
        name = re.findall(r"Valve (.*) has", line)[0]
        flow = int(re.findall(r'flow rate=(\d+)', line)[0])

        node = Node(name=name, flow=flow)
        graph[node.name] = node
        doors = re.findall(r'tunnels? leads? to valves? (.*)', line)[0].split(",")
        graph_distances[node.name] = {door.replace(" ", ""):1 for door in doors}

    # Compute distances
    distances_all = {}
    for key in graph:
        if graph[key].flow > 0 or key == start_node_name:
            distances_curr, _ = bellmanFord(graph_distances, key)
            distances_all[key] = {key_:val_ for key_, val_ in distances_curr.items() if graph[key_].flow > 0 and val_ > 0}
            
            if display: print("{}: {}".format(key, distances_all[key]))
    
    return graph, distances_all


def search_solution(graph, distances_all, starting_node_name, number_agent, best_score = 0):
    nodes = [graph[node_name] for node_name in distances_all[starting_node_name]]

    solutions = [Solution(graph[starting_node_name], nodes, distances_all) for _ in range(number_agent)]
    solution_set = SolutionSet(solutions)
    queue = [ solution_set ]

    i = 0
    while (queue):
        # i += 1
        # solution_set = queue.pop(random.randrange(len(queue)))
        # if i % 10000: 
        #     solution_set = queue.pop(0)
        # else:
        solution_set = queue.pop()
        
        if not solution_set.canImprove(best_score):
            continue

        if (score := solution_set.get_score()) > best_score:
            best_score = score
            print(best_score, str(solution_set), sep=" ")
            i = 0
        for next_nodes_pair in solution_set.get_next_nodes_pair():
            new_solution = pickle.loads(pickle.dumps(solution_set, -1))

            new_solution.move_to_point(next_nodes_pair, distances_all)
            if (score := solution_set.get_score()) > best_score:
                best_score = score
                print(best_score, str(solution_set), sep=" ")
                i = 0

            if new_solution.canImprove(best_score):
                queue.append(new_solution)
    return best_score


START_NODE = "AA"
FILE_NAME = r"D:\Informatique\AdventOfCode\Day16\input.txt"
graph, distances_all = read_data(FILE_NAME, START_NODE)


TIME_MAX = 30
best_score = search_solution(graph, distances_all, START_NODE, 1, 0)
print(best_score)
# 2087 AA-YI-UA-AW-EL-OY-FL-EG-XY


# TIME_MAX = 26
# best_score = 0
# best_score = 2400
# best_score = search_solution(graph, distances_all, START_NODE, 2, best_score)
# print(best_score)
# # 2591 AA-YI-UA-AW-EL-OY-FL-EG AA-OZ-FX-VA-GQ-TU-CR-XY
