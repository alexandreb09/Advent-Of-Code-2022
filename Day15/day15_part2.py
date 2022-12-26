from shapely.geometry import LineString
import itertools
import re

X = 0
Y = 1

def distance(pointA, pointB):
    return abs(pointA[X] - pointB[X]) + abs(pointA[Y] - pointB[Y])


with open("E:\Divers\Perso\AdventOfCode\Day15\input.txt") as file:
    lines_raw = [line.strip() for line in file.readlines()]

pairs = []
lines = []
for line in lines_raw:
    numbers = list(map(int, re.findall(r"-?\d+", line)))
    sensor_position = numbers[:2]
    beacon_position = numbers[2:]
    d = distance(sensor_position, beacon_position)
    pairs.append({'sensor': sensor_position, 'beacon': beacon_position, 'distance': d})
    s_top   = (sensor_position[X], sensor_position[Y] - d)
    s_down  = (sensor_position[X], sensor_position[Y] + d)
    s_left  = (sensor_position[X] - d, sensor_position[Y])
    s_right = (sensor_position[X] + d, sensor_position[Y])
    lines.append([s_top, s_right])
    lines.append([s_right, s_down])
    lines.append([s_down, s_left])
    lines.append([s_left, s_top])

lines = list(map(LineString, lines))

def is_valid_point(point, pairs, MAX):
    if  point[X] < 0 or point[Y] < 0 or point[X] > MAX or point[Y] > MAX: return False
    return all([distance(pair['sensor'], point) > pair['distance'] for pair in pairs])

def find_direct_voisins(point):
    out = [point]
    out.append([point[X] - 1, point[Y] - 1])
    out.append([point[X] - 1, point[Y]])
    out.append([point[X] - 1, point[Y] + 1])
    out.append([point[X], point[Y] - 1])
    out.append([point[X], point[Y]])
    out.append([point[X], point[Y] + 1])
    out.append([point[X] + 1, point[Y] - 1])
    out.append([point[X] + 1, point[Y]])
    out.append([point[X] + 1, point[Y] + 1])
    return out

def search(lines, pairs, MAX):
    for line1, line2 in itertools.combinations(lines, 2):
        intersection = line1.intersection(line2)
        candidates = []
        if not intersection.is_empty:
            coords = list(map(int, list(intersection.coords[0])))
            candidates.append([coords[X], coords[Y]])
            candidates.append([coords[X] + 1, coords[Y]])
            candidates.append([coords[X], coords[Y] + 1])
            candidates.append([coords[X] + 1, coords[Y] + 1])
            
            for candidate in candidates:
                voisins = find_direct_voisins(candidate)
                for voisin in voisins:
                    if is_valid_point(voisin, pairs, MAX):
                        return voisin
    return None

MAX = 4000000
out = search(lines, pairs, MAX)
print(out)