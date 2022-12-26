X = 0
Y = 1

MOVE_OUT = 1
BLOCKED = 2

SAND_POSITION = [500, 0]

EXTRA_COLUMNS = 1000

with open("E:\Divers\Perso\AdventOfCode\Day14\input.txt") as file:
    data = [line.strip().split(" -> ") for line in file.readlines()]
    paths = [[list(map(int, coordinates.split(","))) for coordinates in line] for line in data ]

def find_extreme(paths):
    min_x = SAND_POSITION[X]
    max_x = SAND_POSITION[X]
    min_y = SAND_POSITION[Y]
    max_y = SAND_POSITION[Y]

    for path in paths:
        for point in path:
            min_x = min(min_x, point[X])
            min_y = min(min_y, point[Y])
            max_x = max(max_x, point[X])
            max_y = max(max_y, point[Y])

    return (min_x, min_y), (max_x, max_y + 2)

def build_grid(paths):
    top_left, bottom_right = find_extreme(paths)
    paths = [[[coordinate[X] - top_left[X], coordinate[Y]] for coordinate in path] for path in paths]

    SIZE_X = bottom_right[X] - top_left[X] + 1
    SIZE_Y = bottom_right[Y] - top_left[Y] + 1
    grid = [["." for _ in range(SIZE_X)] for y in range(SIZE_Y)]

    paths.append([[0, SIZE_Y-1], [SIZE_X-1, SIZE_Y-1]])
    
    for path in paths:
        for start, end in zip(path, path[1:]):
            if start[X] != end[X] and start[Y] != end[Y]: 
                raise "Move diagonally for items: " + start + " " + end
            if start[X] == end[X]:
                # always draw from top to bottom
                if start[Y] > end[Y]: start, end = end, start
                for y_delta in range(end[Y] - start[Y] + 1):
                    grid[start[Y] + y_delta][start[X]] = "#"
            if start[Y] == end[Y]:
                # always draw from left to right
                if start[X] > end[X]: start, end = end, start
                for x_delta in range(end[X] - start[X] + 1):
                    grid[start[Y]][start[X] + x_delta] = "#"


    # Add extra columns
    paths = [[[coordinate[X] + EXTRA_COLUMNS, coordinate[Y]] for coordinate in path] for path in paths]
    for i in range(EXTRA_COLUMNS):
        for i, line in enumerate(grid):
            val = '.' if i < len(grid) - 1 else '#'
            grid[i] = [val] + line + [val]

    SAND_POSITION[X] = SAND_POSITION[X] - top_left[X] + EXTRA_COLUMNS
    grid[SAND_POSITION[Y]][SAND_POSITION[X]] = "+"
    
    return paths, grid, SAND_POSITION

paths, grid, SAND_POSITION = build_grid(paths)

def get_next_position(grid, position):
    # Check Down move
    move_down = [position[X], position[Y] + 1]
    if move_down[Y] >= len(grid): return MOVE_OUT
    if grid[move_down[Y]][move_down[X]] == ".": return move_down
    # Check down left
    move_down_left = [move_down[X] - 1, move_down[Y]]
    if move_down_left[X] < 0 :  return MOVE_OUT
    if grid[move_down_left[Y]][move_down_left[X]] == ".": return move_down_left
    # Check down right
    move_down_right = [move_down[X] + 1, move_down[Y]]
    if move_down_right[X] >= len(grid[0]) :  return MOVE_OUT
    if grid[move_down_right[Y]][move_down_right[X]] == ".": return move_down_right
    return BLOCKED


def draw_sand(grid, SAND_POSITION):
    current_position = SAND_POSITION
    new_position = get_next_position(grid, current_position)
    while new_position not in [MOVE_OUT, BLOCKED]:
        current_position = new_position
        new_position = get_next_position(grid, current_position)
        if new_position == MOVE_OUT: raise "Moved OUT  from " + current_position
    if new_position == BLOCKED:
        grid[current_position[Y]][current_position[X]] = "o"
    return grid, new_position == BLOCKED and current_position == SAND_POSITION


i = 0
blocked = False
while not blocked:
    grid, blocked = draw_sand(grid, SAND_POSITION)
    i += 1
[print("".join(line)) for line in grid]
print(i)
