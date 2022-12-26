with open('input.txt') as file:
    lines = [line.strip() for line in file.readlines()]



############# PART 1 #######################
def is_interval_contained(int1, int2):
    if int1[0] <= int2[0] and int1[1] >= int2[1]: return True
    if int2[0] <= int1[0] and int2[1] >= int1[1]: return True
    return False

n=0
for line in lines:
    parts = line.split(",")
    part_1 = list(map(int, parts[0].split("-")))
    part_2 = list(map(int, parts[1].split("-")))
    if is_interval_contained(part_1, part_2):
        n+=1
print(n)

############# PART 2 #######################
def is_interval_intersecting(int1, int2):
    list1 = [i for i in range(int1[0], int1[1]+1, 1)]
    list2 = [i for i in range(int2[0], int2[1]+1, 1)]
    return set(list1) & set(list2)

n=0
for line in lines:
    parts = line.split(",")
    part_1 = list(map(int, parts[0].split("-")))
    part_2 = list(map(int, parts[1].split("-")))
    if is_interval_intersecting(part_1, part_2):
        n+=1
print(n)

