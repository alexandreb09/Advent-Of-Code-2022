import math

X, Y, Z = 0, 1, 2
SQRT_2 = math.sqrt(2)

def part_1(points):
    n = 0 
    for point_ref in points:
        n_face = 6
        for point in points:
            if point != point_ref and math.dist(point, point_ref) < SQRT_2:
                n_face -= 1
        n += n_face
    return n


def get_all_next_neightboors(point, point_min, point_max):
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            for dz in [-1,0,1]:
                neightboor = tuple([point[X] + dx, point[Y] + dy, point[Z] + dz])
                if dx == 0 and dy == 0 and dz == 0: continue
                if math.dist(point, neightboor) > 1: continue
                # Check searching area
                if neightboor[X] < point_min[X] or neightboor[X] > point_max[X]: continue
                if neightboor[Y] < point_min[Y] or neightboor[Y] > point_max[Y]: continue
                if neightboor[Z] < point_min[Z] or neightboor[Z] > point_max[Z]: continue
                yield neightboor

def part_2(points):
    point_min = tuple([
        min(point[X] for point in points) - 1,
        min(point[Y] for point in points) - 1,
        min(point[Z] for point in points) - 1,
    ])
    point_max = tuple([
        max(point[X] for point in points) + 1,
        max(point[Y] for point in points) + 1,
        max(point[Z] for point in points) + 1,
    ])

    queue = [ point_min + tuple() ]
    visited_points = set()
    matching_faces = set()
    while queue:
        point = queue.pop()
        for neightboor in get_all_next_neightboors(point, point_min, point_max):
            if neightboor in points:
                if math.dist(point, neightboor) < SQRT_2:
                    matching_faces.add(tuple(point + neightboor))
                    matching_faces.add(tuple(neightboor + point))
            elif neightboor not in visited_points:
                queue.append(neightboor)
            
            visited_points.add(point)
    return len(matching_faces) / 2



with open(r'D:\Informatique\AdventOfCode\Day18\input.txt') as file:
    points = [tuple(map(int, line.split(","))) for line in file.readlines()]

print(part_1(points))

print(part_2(points))