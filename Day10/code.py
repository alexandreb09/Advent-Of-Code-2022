with open('input.txt') as file:
    instructions = [line.strip() for line in file.readlines()]

# cycles = []

# i = 0
# X = 1
# subcycles = [X]
# for instruction in instructions:
#     if instruction == "noop":
#         i += 1
#         if i % 20 == 0:
#             cycles.append((i, X))
#     elif instruction.startswith("addx"):
#         clock = int(instruction.split(" ")[-1])
#         i += 1
#         if i % 20 == 0:
#             cycles.append((i, X))
#         i += 1
#         if i % 20 == 0:
#             cycles.append((i, X))
#         X += clock

# # print(cycles)
# cycles = cycles[0::2]
# print(sum([x[0] * x[1] for x in cycles]))
# # 14540


#######################################
#               PART 2                #
#######################################

def update_subdraw(i, X, draws_sub):
    j = i % CYCLE_SIZE
    if j == X-1 or j == X or j == X + 1:
        draws_sub.append("#")
    else: draws_sub.append(".")
    return draws_sub

def update_draws(i, draws_sub, draws):
    if i % CYCLE_SIZE == 0:
        draws.append(draws_sub)
        draws_sub = []
    return draws_sub, draws

CYCLE_SIZE = 40
cycles = []
draws = []

i = 0
X = 1
draws_sub = list()
for instruction in instructions:
    draws_sub = update_subdraw(i, X, draws_sub)
    i += 1
    draws_sub, draws = update_draws(i, draws_sub, draws)
    if instruction.startswith("addx"):
        draws_sub = update_subdraw(i, X, draws_sub)
        i += 1
        draws_sub, draws = update_draws(i, draws_sub, draws)
        clock = int(instruction.split(" ")[-1])
        X += clock

[print("".join(draw)) for draw in draws]