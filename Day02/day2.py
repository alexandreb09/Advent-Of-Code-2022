
YOU = {
	"A": "pierre",
	"B": "papier",
	"C": "ciseaux"
}
ME = {
	"X": "pierre",
	"Y": "papier",
	"Z": "ciseaux"
}

def get_score_from_shape(shape):
	if shape == "pierre": return 1
	elif shape == "papier": return 2
	elif shape == "ciseaux": return 3
	return 0

def get_score_from_result(you_shape, me_shape):
	if (you_shape == me_shape): return 3
	if you_shape == "pierre":
		if me_shape == "papier": return 6
		if me_shape == "ciseaux": return 0
	if you_shape == "papier":
		if me_shape == "pierre": return 0
		if me_shape == "ciseaux": return 6
	if you_shape == "ciseaux":
		if me_shape == "pierre": return 6
		if me_shape == "papier": return 0

def deduce_my_shape(you_shape, elf_advice):
	if elf_advice == "Y": return you_shape
	if elf_advice == "X": 
		if you_shape == "ciseaux": return "papier"
		if you_shape == "pierre": return "ciseaux"
		if you_shape == "papier": return "pierre"
	if elf_advice == "Z": 
		if you_shape == "ciseaux": return "pierre"
		if you_shape == "pierre": return "papier"
		if you_shape == "papier": return "ciseaux"

total_score = 0
with open('input.txt') as f:
	lines = f.readlines()
	for line in lines:
		line_list = line.strip().split(" ")
		you_shape = YOU[line_list[0]]
		# me_shape = ME[line_list[1]]
		me_shape = line_list[1]

		me_shape = deduce_my_shape(you_shape, me_shape)
		score_from_shape = get_score_from_shape(me_shape)
		score_from_result = get_score_from_result(you_shape, me_shape)
		round_score = score_from_shape + score_from_result

		total_score += round_score

print(total_score)

