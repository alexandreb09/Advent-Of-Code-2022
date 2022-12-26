import numpy as np

with open('input.txt') as file:
    data = [list(line.strip()) for line in file.readlines()]


width = len(data[0])
height = len(data)
visible_edge = width * 2 + height * 2 - 4

print("Edge: " + str(visible_edge))

array_data = np.array(data)

def getCardinalList(array_data, y, x):
    column = list(array_data[:, x])
    top = column[: y]
    bottom = column[y+1:]
    value = column[y]
    row = list(array_data[y, :])
    left = row[:x]
    right = row[x+1:]
    return top, bottom, left, right, value

def isTreeHigher(array_data, y, x):
    top, bottom, left, right, value = getCardinalList(array_data, y, x)
    # get vertical row
    if value > max(top) or value > max(bottom):
        return True
    # get horizontal row
    if value > max(left) or value > max(right):
        return True
    return False

def getFirstValue(list, value):
    return next((i+1 for i, x in enumerate(list) if x >= value), len(list))

def tree_distance(array_data, y, x):
    top, bottom, left, right, value = getCardinalList(array_data, y, x)
    # get vertical row
    top.reverse()
    left.reverse()

    return getFirstValue(top, value) * getFirstValue(bottom, value) * getFirstValue(left, value) * getFirstValue(right, value)
    

# PART 1
# n = 0
# for y in range(1, len(data) - 1):
#     for x in range(1, len(data[0]) - 1):
#         if isTreeHigher(array_data, y, x): 
#             n+=1
# print(n)
# print(n + visible_edge)

# PART 2
tree_distances = []
for y in range(1, len(data) - 1):
    for x in range(1, len(data[0]) - 1):
        tree_distances.append(tree_distance(array_data, y, x))
print(tree_distances)
print(max(tree_distances))

# print(tree_distance(array_data, 3, 2))
