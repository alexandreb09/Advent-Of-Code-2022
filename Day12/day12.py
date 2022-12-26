import numpy as np

START = "S"
DESTINATION = "E"

REVERSE = False

class Point:
    def __init__(self, x, y, value) -> None:
        self.x = x
        self.y = y
        self.id = "x-{}-y-{}".format(self.x, self.y)
        self.value = value if value != START else "a"
        self.candidates = []

    def __str__(self) -> str:
        return self.id + ": " + self.candidates

    def compute_candidate_check(self, candidate_value) -> bool:
        if candidate_value == DESTINATION:
            return self.value == "z"
        else:
            return ord(candidate_value) <= ord(self.value) + 1 #or (current_val == "z" and candidate_value == DESTINATION)

    # def compute_candidate_check(self, candidate_value) -> bool:
    #     out = self._compute_candidate_check(candidate_value)
    #     if REVERSE: out = not out
    #     return out

    def compute_candidates(self, grid) -> None:
        SIZE_X = len(grid[0])
        SIZE_Y = len(grid)

        self.candidates = []

        if self.value == DESTINATION:
            return

        # MOVE right >>>
        if self.x < SIZE_X - 1:
            candidate_point = grid[self.y][self.x + 1]
            if self.compute_candidate_check(candidate_point.value):
                self.candidates.append(candidate_point)
        # MOVE left <<<
        if self.x > 0:
            candidate_point = grid[self.y][self.x - 1]
            if self.compute_candidate_check(candidate_point.value):
                self.candidates.append(candidate_point)
        # MOVE UP ^^^ 
        if self.y > 0:
            candidate_point = grid[self.y - 1][self.x]
            if self.compute_candidate_check(candidate_point.value):
                self.candidates.append(candidate_point)
        # MOVE DOWN vvv 
        if self.y < SIZE_Y - 1:
            candidate_point = grid[self.y + 1][self.x]
            if self.compute_candidate_check(candidate_point.value):
                self.candidates.append(candidate_point)



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



#####################################
# with open("input-2.txt") as file:
with open(r"D:\Informatique\AdventOfCode\Day12\input2.txt") as file:
    grid = [list(line.strip()) for line in file.readlines()]

# Prepare data
point_dest = None
for y, line in enumerate(grid):
    for x, cell in enumerate(line):
        point = Point(x, y, cell)
        grid[y][x] = point
        if cell == START:
            point_curr = point
        if cell == DESTINATION:
            point_dest = point

# Compute candidates
graphe = {}
map_id_value = {}
for y, line in enumerate(grid):
    for x, cell in enumerate(line):
        point = grid[y][x]
        point.compute_candidates(grid)
        graphe[point.id] = {_.id:1 for _ in point.candidates}
        map_id_value[point.id] = point.value

distances, predecesseurs = bellmanFord(graphe, point_curr.id)


def find_shortest_path(parents, point_E, point_S):
    path = []
    point_curr_id = point_E
    while point_curr_id != None and map_id_value[point_curr_id] != point_S:
        point_curr_id = parents[point_curr_id]
        path.append(point_curr_id)
    path.reverse()
    return path

print(predecesseurs)
print(distances[point_dest.id])
path = find_shortest_path(predecesseurs, point_dest.id, "a")
print(path)
print(len(path))
# 524
# bellow 492