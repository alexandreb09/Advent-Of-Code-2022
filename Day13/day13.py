from functools import cmp_to_key

LEFT = 0
RIGHT = 1

OK = 1
KO = -1
OO = 0


def compare(left, right):
    if type(left) != type(right): 
        if type(left) != list:
            left = [left]
        if type(right) != list: 
            right = [right]
    elif type(left) == int and type(right) == int:
        return OK if left < right else KO
        
    for i in range(len(left)):
        if i >= len(right):
            return KO
        if type(left[i]) == int and type(right[i]) == int:
            if left[i] != right[i]:
                return OK if left[i] < right[i] else KO
            else: continue
        else: 
            result = compare(left[i], right[i])
            if result in [OK, KO]:
                return result
    
    if len(left) != len(right):
        return OK if len(left) < len(right) else KO
    
    return OO

with open(r"E:\Divers\Perso\AdventOfCode\Day13\input.txt") as file:
    data = [line.strip() for line in file.readlines() if line.strip() != ""]

##################################
###           PART 1           ###
##################################

# pairs = [[eval(data[i]), eval(data[i+1])] for i in range(0,len(data),2)]

# out = [compare(pair[0], pair[1]) for pair in pairs]
# for i, pair in enumerate(pairs):
#     print("{}: {}".format(i + 1, "YES" if compare(pair[0], pair[1]) == OK else "NO"))
# print(sum([i+1 for i,_ in enumerate(out) if _ == OK]))

##################################
###           PART 2           ###
##################################
pairs = [eval(item) for item in data]
pairs.append([[2]])
pairs.append([[6]])
pairs = sorted(pairs, key=cmp_to_key(compare), reverse=True)
print((pairs.index([[2]]) + 1) * (pairs.index([[6]]) + 1) )
# 20758