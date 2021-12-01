import math

def file_check(f):
    try:
        r = open(f, "r")
        r.close()
        return True
    except:
        return False

def stitch_measure(count):
    stitch = 1/count
    diagonal = math.sqrt(2*(stitch**2))
    thread_length = (2*stitch) + (2*diagonal)
    return thread_length

file_name = input("Enter file name: ")
while file_check(file_name) == False:
    file_name = input("File not found. Please enter file name: ")
file = open(file_name, "r")
file_contents = file.read()
file.close()
split_file = file_contents.split("\n")
pattern = []
for i in range(len(split_file)):
    row = split_file[i].split(",")
    pattern.append(row)
colors = {}
for i in range(len(pattern)):
    for x in range(len(pattern[i])):
        color = pattern[i][x]
        if color == "":
            pattern[i].remove(color)
        elif color not in colors.keys():
            colors[color] = 1
        else:
            colors[color] = colors.get(color) + 1
names = list(colors.keys())
list_of_colors = []
for i in range(len(names)):
    symbol = names[i]
    color_name = input("What color is represented by the " + symbol + " symbol in this pattern? ")
    while color_name in list_of_colors or color_name == "":
        if color_name in list_of_colors:
            color_name = input("You have already used that name for another color. What color is represented by the " + symbol + " symbol in this pattern? ")
        elif color_name == "":
            color_name = input("Input not recognized. Please try again. What color is represented by the " + symbol + " symbol in this pattern? ")
    colors[color_name] = colors.pop(symbol)
    list_of_colors.append(color_name)
count = int(input("What is the thread count of the fabric being used? "))
for i in range(len(names)):
    name = list(colors.keys())[i]
    thread = round(stitch_measure(count)*colors[name], 2)
    print("This pattern requires " + str(thread) + " inches of " + name + " thread.")
