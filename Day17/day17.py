import copy
import numpy as np

MOVE_LEFT = "<"
MOVE_RIGHT = ">"
MAX_X = 7
LIMIT_CYCLICITY = 50000 # Search cyclicity if simulation go higher than "LIMIT_CYCLICITY" falls


# +--> (x)
# |
# v (y)


# N [. . . . . .]
# . [. . . . . .]
# 3 [. . . . . .]
# 2 [. . . . . .]
# 1 [. . . . . .]
# 0 [# # # # # #]

shapes = [
    np.array([(2,0), (3,0), (4,0), (5,0)], dtype=np.int64),
    np.array([(3,1), (3,2), (4,1), (3,0), (2,1)], dtype=np.int64),
    np.array([(2,0), (3,0), (4,0), (4,1), (4,2)], dtype=np.int64),
    np.array([(2,3), (2,2), (2,1), (2,0)], dtype=np.int64),
    np.array([(2,0), (2,1), (3,1), (3,0)], dtype=np.int64)
]

def draw_shape(index_shape, y_offset) -> np.array:
    shape = np.copy(shapes[index_shape])
    move_y(shape, y_offset + 4)
    return shape

def move_x(shape, dx=1) -> None:
    shape[:,0] += dx
def move_y(shape, dy=1) -> None:
    shape[:,1] += dy

def draw_str_shape(blocks, height, shape = None) -> None:
    blocks = copy.deepcopy(blocks)
    if shape is not None: 
        blocks = update_blocks(blocks, shape)
        height = max(max(shape[:, 1]), height)
    for y in range(height +1, -1,-1):
        line_str = "".join("#" if (x,y) in blocks else "." for x in range(MAX_X))
        line_str = "|{}|".format(line_str)
        print(line_str)
    print("+" + "-" * MAX_X + "+\n")

def is_intersect(blocks, shape) -> bool:
    return any((tuple(point.tolist()) in blocks) for point in shape)

def update_blocks(blocks, shape) -> set:
    for point in shape:
        blocks.add(tuple(point.tolist()))
    return blocks

def fall_rock(moves_str, i, shape, blocks):
    has_moved = True
    while has_moved:
        move_str = moves_str[i % len(moves_str)]
        minx, miny, maxx = min(shape[:,0]), min(shape[:,1]), max(shape[:,0])
        if MOVE_LEFT == move_str and minx > 0:
            move_x(shape, -1)
            if is_intersect(blocks, shape):
                move_x(shape, 1)
        elif MOVE_RIGHT == move_str and maxx < MAX_X - 1:
            move_x(shape, 1)
            if is_intersect(blocks, shape):
                move_x(shape, -1)
        
        has_moved = False
        if miny > 0:
            move_y(shape, -1)
            if is_intersect(blocks, shape):
                move_y(shape, 1)
            else: has_moved = True
        i += 1
    return shape, i

def search_correlation(mapping_height_nrocks):
    periodicity = 0
    for i in range(3, len(mapping_height_nrocks)):
        if all(mapping_height_nrocks[j] % mapping_height_nrocks[i] == 0 for j in range(i, len(mapping_height_nrocks), i)):
            periodicity = i
            break
    if periodicity > 0:
        return periodicity, mapping_height_nrocks[periodicity]

def simulate(number_rocks_total, mapping_height_nrocks = {}):
    index_shape = 0
    curr_height = -1
    shape = draw_shape(index_shape, curr_height)

    blocks = set()

    i = 0
    n_rocks = 0
    while n_rocks < number_rocks_total:
        shape, i = fall_rock(moves_str, i, shape, blocks)

        blocks = update_blocks(blocks, shape)
        curr_height = max(max(shape[:,1]), curr_height)

        n_rocks += 1
        shape = draw_shape(n_rocks % len(shapes), curr_height)
        mapping_height_nrocks[n_rocks] = curr_height
    return curr_height + 1


def solve(number_rocks_total, mapping_height_nrocks):
    if number_rocks_total < LIMIT_CYCLICITY:
        return simulate(number_rocks_total)
    
    mapping_height_nrocks = {}
    simulate(LIMIT_CYCLICITY, mapping_height_nrocks)
    period, height_delta = search_correlation(mapping_height_nrocks)
    remaining_falls = number_rocks_total % period
    height = simulate(remaining_falls)
    total = (number_rocks_total // period) * height_delta + height 
    return total



moves_str = open(r'D:\Informatique\AdventOfCode\Day17\input.txt').readlines()[0]
# moves_str = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

part1 = solve(2022, LIMIT_CYCLICITY)
print("Part 1: {}".format(part1))

NUMBER_ROCKS = 1000000000000
part2 = solve(NUMBER_ROCKS, LIMIT_CYCLICITY)
print("Part 2: {}".format(part2))
# 1567723342929