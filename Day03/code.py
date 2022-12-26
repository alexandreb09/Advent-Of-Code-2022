


def split_line(line):
    i = int(len(line)/2)
    return (line[0:i], line[i:])

def get_letter_value(letter):
    is_upper_case = letter.upper() == letter
    key = int(ord(letter))
    if is_upper_case: return key - 38
    else: return key - 96

# with open('input.txt') as file:
#     lines = file.readlines()
#     sum = 0
#     for line in lines:
#         first_part, second_part = split_line(line)
#         common_letter = list(set(first_part).intersection(second_part))[0]
#         print(common_letter)
#         value = get_letter_value(common_letter)
#         sum += value
# print(sum)


#######################################


with open('input.txt') as file:
    lines = file.readlines()
    lines = [_.strip() for _ in lines]
    sum = 0
    lines_grouped = [lines[n:n+3] for n in range(0, len(lines), 3)]
    for line_grouped in lines_grouped:
        print(line_grouped)
        common_letter = list(set(line_grouped[0]).intersection(line_grouped[1]).intersection(line_grouped[2]))[0]
        print(common_letter)
        value = get_letter_value(common_letter)
        sum += value
    print(sum)