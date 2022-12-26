from math import prod

class Monkey:
    def __init__(self, items, operation, modulo, true_int, false_int) -> None:
        self.items = items
        self.operation = operation
        self.test = lambda x: true_int if x % modulo == 0 else false_int
        self.i = 0
        self.modulo = modulo

    def do_item_inspection(self, item):
        # new_item_val = int(self.operation(item) / 3)
        new_item_val = self.operation(item)
        new_item_val = new_item_val % MODULO
        return self.test(new_item_val), new_item_val

def perform_round(monkeys):
    for monkey in monkeys:
        n = len(monkey.items)
        monkey.i += n
        for item in monkey.items:
            new_monkey_i, new_item = monkey.do_item_inspection(item)
            monkeys[new_monkey_i].items.append(new_item)
        monkey.items = monkey.items[n:]
    return monkeys

monkey0 = Monkey([79, 98],         lambda x: x * 19, 23, 2, 3 )
monkey1 = Monkey([54, 65, 75, 74], lambda x: x + 6,  19, 2, 0)
monkey2 = Monkey([79, 60, 97],     lambda x: x * x,  13,1,3)
monkey3 = Monkey([74],             lambda x: x + 3,  17,0,1)
monkeys = [monkey0, monkey1, monkey2, monkey3]

monkey0 = Monkey([71, 56, 50, 73],                 lambda old: old * 11, 13, 1, 7) 
monkey1 = Monkey([70, 89, 82],                     lambda old: old + 1,  7, 3, 6) 
monkey2 = Monkey([52, 95],                         lambda old: old ** 2, 3, 5, 4) 
monkey3 = Monkey([94, 64, 69, 87, 70],             lambda old: old + 2,  19, 2, 6) 
monkey4 = Monkey([98, 72, 98, 53, 97, 51],         lambda old: old + 6,  5, 0, 5) 
monkey5 = Monkey([79],                             lambda old: old + 7,  2, 7, 0) 
monkey6 = Monkey([77, 55, 63, 93, 66, 90, 88, 71], lambda old: old * 7,  11, 2, 4) 
monkey7 = Monkey([54, 97, 87, 70, 59, 82, 59],     lambda old: old + 8,  17, 1, 3) 
monkeys = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]

MODULO = prod([monkey.modulo for monkey in monkeys]) 
for i in range(10000):
    monkeys = perform_round(monkeys)

print([monkey.items for monkey in monkeys])
print([monkey.i for monkey in monkeys])
items_inspected_per_monkey = sorted([monkey.i for monkey in monkeys], reverse=True)

out = items_inspected_per_monkey[0] * items_inspected_per_monkey[1]
print(out)