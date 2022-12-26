with open("input-3.txt") as file:
    instructions = [line.strip().split() for line in file]


X = 1
Y = 0
N = 15
grid = [[False for _ in range(2 * N)] for __ in range(2 * N)]


def move_right_one_step(head, tail):
    if head == None:
        tail[X] += 1
    elif head[X] - tail[X] > 1:
        # move vertically
        tail[Y] = head[Y]
        # move horizontally
        tail[X] = head[X] - 1
    return head, tail

def move_left_one_step(head, tail):
    if head == None:
        tail[X] -= 1
    elif tail[X] - head[X] > 1:
        # move vertically
        tail[Y] = head[Y]
        # move horizontally
        tail[X] = head[X] + 1
    return head, tail

def move_up_one_step(head, tail):
    if head == None:
        tail[Y] += 1
    elif head[Y] - tail[Y] > 1:
        # move vertically
        tail[X] = head[X]
        # move horizontally
        tail[Y] = head[Y] - 1
    return head, tail

def move_down_one_step(head, tail):
    if head == None:
        tail[Y] -= 1
    elif tail[Y] - head[Y] > 1:
        # move vertically
        tail[X] = head[X]
        # move horizontally
        tail[Y] = head[Y] + 1
    return head, tail

def move_tail(head, tail):
    if head[X] - tail[X] > 1:
        # move vertically
        tail[Y] = head[Y]
        # move horizontally
        tail[X] = head[X] - 1
    if tail[X] - head[X] > 1:
        # move vertically
        tail[Y] = head[Y]
        # move horizontally
        tail[X] = head[X] + 1
    if head[Y] - tail[Y] > 1:
        # move vertically
        tail[X] = head[X]
        # move horizontally
        tail[Y] = head[Y] - 1
    if tail[Y] - head[Y] > 1:
        # move vertically
        tail[X] = head[X]
        # move horizontally
        tail[Y] = head[Y] + 1
    return tail

def move_head(direction, head):
    if direction == "D": 
        head[Y] -= 1
    elif direction == "U": 
        head[Y] += 1
    elif direction == "R": 
        head[X] += 1
    elif direction == "L": 
        head[X] -= 1
    return head

#############################
###         PART 1        ###
#############################
# #      [x,    y]
# head = [0, N]
# tail = [0, N]
# grid[tail[X]][tail[Y]] = True

# number_points = 2


# for i, instruction in enumerate(instructions):
#     direction = instruction[0]
#     steps = instruction[1]

#     for _ in range(int(steps)):
#         if direction == "D": head, tail = move_down_one_step(head, tail)
#         elif direction == "U": head, tail = move_up_one_step(head, tail)
#         elif direction == "R": head, tail = move_right_one_step(head, tail)
#         elif direction == "L": head, tail = move_left_one_step(head, tail)
        
#         grid[tail[X]][tail[Y]] = True


# # [print(["x" if x else "." for x in _]) for _ in grid]
# print(sum([sum(_) for _ in grid]))




#############################
###         PART 2        ###
#############################
#      [x,    y]
# head = [0, N]
# tail = [0, N]

number_points = 10
points = [[N, N] for _ in range(number_points)]
grid[points[-1][X]][points[-1][Y]] = 's'


for i, instruction in enumerate(instructions):
    direction = instruction[0]
    steps = instruction[1]

    for _ in range(int(steps)):
        points[0] = move_head(direction, points[0])
        for k, tail in enumerate(points[1:]):
            head = points[k]
            points[k + 1] = move_tail(head, tail)
        grid[points[-1][X]][points[-1][Y]] = True

[print(" ".join(["#" if x else "." for x in _])) for _ in grid]
print(sum([sum(_) for _ in grid]))
# 2595