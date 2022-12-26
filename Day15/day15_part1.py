import re

X = 0
Y = 1

def distance(pointA, pointB):
    return abs(pointA[X] - pointB[X]) + abs(pointA[Y] - pointB[Y])

def point_to_str(point):
    return str(point[X]) + '-' + str(point[Y])

with open("input.txt") as file:
    lines = [line.strip() for line in file.readlines()]

pairs = []
beacons = []
distances = []
for line in lines:
    numbers = list(map(int, re.findall(r"-?\d+", line)))
    sensor_position = numbers[:2]
    beacon_position = numbers[2:]
    pairs.append({'sensor': sensor_position, 'beacon': beacon_position, 'distance': distance(sensor_position, beacon_position)})
    beacons.append(beacon_position)
    

def is_close_beacon(test, beacons, sensors):
    if test in beacons: return False
    for sensor in sensors:
        sensor_p = sensor["sensor"]
        # print(distance_to_closest_beacon)
        # if sensor_p[Y] - distance_to_closest_beacon - 1 <= LINE and LINE <= sensor_p[Y] + distance_to_closest_beacon + 1:
        if distance(sensor_p, test) <= sensor["distance"]:
            return True
    return False


def compute_coverage(sensors, LINE):
    min_x = min([x['sensor'][X] for x in sensors])
    max_x = max([x['sensor'][X] for x in sensors])
    max_d = max([sensor['distance'] for sensor in sensors])
    start_x = min_x - max_d - 1
    end_x = max_x + max_d + 1

    out = []
    for x in range(start_x, end_x + 1):
        test = [x, LINE]
        out.append(is_close_beacon(test, beacons, sensors))

    return sum(out)

LINE = 2000000
# LINE = 10
out = compute_coverage(pairs, LINE)
print(out)
# 5166077