

elfe_capacities = []
curr_elfe = []
with open('input-1.txt') as f:
	for line in f.readlines():
		if line.strip() == "":
			elfe_capacities.append(list(map(int, curr_elfe)))
			curr_elfe = []
		else: curr_elfe.append(line.strip())


elfe_capacities = [sum(elfe_capacity) for elfe_capacity in elfe_capacities]
elfe_capacities = sorted(elfe_capacities, reverse=True)
top_3 = elfe_capacities[:3]
print(sum(top_3))