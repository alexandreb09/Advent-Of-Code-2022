import re

# [V]         [T]         [J]        
# [Q]         [M] [P]     [Q]     [J]
# [W] [B]     [N] [Q]     [C]     [T]
# [M] [C]     [F] [N]     [G] [W] [G]
# [B] [W] [J] [H] [L]     [R] [B] [C]
# [N] [R] [R] [W] [W] [W] [D] [N] [F]
# [Z] [Z] [Q] [S] [F] [P] [B] [Q] [L]
# [C] [H] [F] [Z] [G] [L] [V] [Z] [H]
#  1   2   3   4   5   6   7   8   9 

list_queue = [
  ['C', 'Z', 'N', 'B', 'M', 'W', 'Q', 'V'],
  ['H', 'Z', 'R', 'W', 'C', 'B'],
  ['F', 'Q', 'R', 'J'],
  ['Z', 'S', 'W', 'H', 'F', 'N', 'M', 'T'],
  ['G', 'F', 'W', 'L', 'N', 'Q', 'P'],
  ['L', 'P', 'W'],
  ['V', 'B', 'D', 'R', 'G', 'C', 'Q', 'J'],
  ['Z', 'Q', 'N', 'B', 'W'],
  ['H', 'L', 'F', 'C', 'G', 'T', 'J'],
]


def do_move(instructions, keep_order):
    n = instructions[0]
    _from = instructions[1] - 1 
    _to = instructions[2] - 1

    numbers_moves = list_queue[_from][-n:]
    del list_queue[_from][len(list_queue[_from]) - n:]
    
    if not keep_order:
        numbers_moves.reverse()

    list_queue[_to] += numbers_moves

with open('input.txt') as file:
    for line in file.readlines():
        instructions = list(map(int, re.findall(r'\d+', line)))
        do_move(instructions, True)

    [print(_) for _ in list_queue]


print("".join([l[-1] for l in list_queue]))