import tkinter as tk
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

def Convert_file():
    file_name = fileName.get()
    if file_check(file_name) == False:
        lblOutput["text"] = "File not found."
    else:
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
        output = []
        count = int(clicked.get())
        thread_per_stitch = stitch_measure(count)
        number_of_strands = int(strandClicked.get())
        for i in range(len(names)):
            symbol = names[i]
            length = math.ceil((thread_per_stitch*colors[symbol]*number_of_strands) + 8)
            if measureClicked.get() == "inches":
                output.append(str(length) + " inches of thread in color " + symbol)
            elif measureClicked.get() == "centimeters":
                length = length*2.54
                output.append(str(length) + " centimeters of thread in color " + symbol)
            elif measureClicked.get() == "skeins":
                length = round(length/1879, 2)
                output.append(str(length) + " skeins of thread (8m/8.7yd each) in color " + symbol)
        outputWindow = tk.Toplevel(window)
        outputWindow.title("Thread Requirements")
        lblOutput = tk.Label(outputWindow, text = "\n".join(output))
        lblOutput.pack()
    
window = tk.Tk()
window.title("Cross stitch helper")
fileName = tk.Entry(width = 15)
aida_types = ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]
clicked = tk.StringVar()
clicked.set("18")
fabricCount = tk.OptionMenu(window, clicked, *aida_types)
strand_options = ["1", "2", "3", "4", "5", "6"]
strandClicked = tk.StringVar()
strandClicked.set("2")
strands = tk.OptionMenu(window, strandClicked, *strand_options)
measure_types = ["inches", "centimeters", "skeins"]
measureClicked = tk.StringVar()
measureClicked.set("inches")
measure = tk.OptionMenu(window, measureClicked, *measure_types)
lbl_measure = tk.Label(text = "System of measurement: ")
lbl_strands = tk.Label(text = "Number of strands: ")
lbl_fileName = tk.Label(text = "Pattern file name: ")
lbl_fabricCount = tk.Label(text = "Fabric count: ")
btnConvert = tk.Button(
    master = window,
    text = "Analyze pattern",
    width = 17,
    height = 1,
    command = Convert_file)
fileName.grid(row = 0, column = 1)
lbl_fileName.grid(row = 0, column = 0)
fabricCount.grid(row = 1, column = 1)
lbl_fabricCount.grid(row = 1, column = 0)
lbl_strands.grid(row = 2, column = 0)
strands.grid(row = 2, column = 1)
lbl_measure.grid(row = 3, column = 0)
measure.grid(row = 3, column = 1)
btnConvert.grid(row = 4, column = 1)
