import tkinter as tk
import math
from tkinter.colorchooser import askcolor

#function to check validity of file name
def file_check(f):
    try:
        r = open(f, "r")
        r.close()
        return True
    except:
        return False

#calculates amount of thread used in 1 stitch (inches)
def stitch_measure(count):
    stitch = 1/count
    diagonal = math.sqrt(2*(stitch**2))
    thread_length = (2*stitch) + (2*diagonal)
    return thread_length

#following 3 functions make sure only one unit of measurement can be selected at a time
def inchChecked(event):
    if chkval_inch.get() == True:
        chk_cm["state"] = "disabled"
        chk_skein["state"] = "disabled"
        for i in range(len(names)):
            symbol = names[i]
            inch_length = math.ceil((thread_per_stitch*colors[symbol]*number_of_strands)*1.15)
            lbl_Output = tk.Label(outputWindow, text = str(inch_length) + " inches of color " + symbol, width = 35, height = 1)
            lbl_Output.grid(row = i+1, column = 0, columnspan = 2)
            lbl_Color = tk.Label(outputWindow, text = "  ")
            lbl_Color.grid(sticky = tk.W, row = i + 1, column = 2)
            thread_color = askcolor(title = "Select thread color for " + symbol)
            lbl_Color["bg"] = thread_color[1]
    else:
        chk_inch["state"] = "active"
        chk_cm["state"] = "active"
        chk_skein["state"] = "active"

def cmChecked(event):
    if chkval_cm.get() == True:
        chk_inch["state"] = "disabled"
        chk_skein["state"] = "disabled"
        for i in range(len(names)):
            symbol = names[i]
            inch_length = math.ceil((thread_per_stitch*colors[symbol]*number_of_strands)*1.15)
            cent_length = round(inch_length*2.54, 2)
            lbl_Output = tk.Label(outputWindow, text = str(cent_length) + " centimeters of color " + symbol, width = 35, height = 1)
            lbl_Output.grid(row = i+1, column = 0, columnspan = 2)
            lbl_Color = tk.Label(outputWindow, text = "  ")
            lbl_Color.grid(sticky = tk.W, row = i + 1, column = 2)
            thread_color = askcolor(title = "Select thread color for " + symbol)
            lbl_Color["bg"] = thread_color[1]
    else:
        chk_inch["state"] = "active"
        chk_cm["state"] = "active"
        chk_skein["state"] = "active"

def skeinChecked(event):
    if chkval_skein.get() == True:
        chk_cm["state"] = "disabled"
        chk_inch["state"] = "disabled"
        for i in range(len(names)):
            symbol = names[i]
            inch_length = math.ceil((thread_per_stitch*colors[symbol]*number_of_strands)*1.15)
            skein_length = round(inch_length/1879, 2)
            lbl_Output = tk.Label(outputWindow, text = str(skein_length) + " skeins of color " + symbol, width = 35, height = 1)
            lbl_Output.grid(row = i+1, column = 0, columnspan = 2)
            lbl_Color = tk.Label(outputWindow, text = "  ")
            lbl_Color.grid(sticky = tk.W, row = i + 1, column = 2)
            thread_color = askcolor(title = "Select thread color for " + symbol)
            lbl_Color["bg"] = thread_color[1]
    else:
        chk_inch["state"] = "active"
        chk_cm["state"] = "active"
        chk_skein["state"] = "active"

#this function reads the pattern file and counts the number of stitches of each color
def Convert_file():
    file_name = fileName.get()
    if file_check(file_name) == False:
        lbl_file["text"] = "File not found."
    else:
        lbl_file["text"] = "Analyzing " + file_name
        file = open(file_name, "r")
        file_contents = file.read()
        file.close()
        split_file = file_contents.split("\n")
        pattern = []
        for i in range(len(split_file)):
            row = split_file[i].split(",")
            pattern.append(row)
        global colors
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
        global names
        global count
        global thread_per_stitch
        global number_of_strands
        names = list(colors.keys())
        count = int(clicked.get())
        thread_per_stitch = stitch_measure(count)
        number_of_strands = int(strandClicked.get())
        #at this point, we have a list of the symbols for each color used in the pattern (names),
        #the thread count of the fabric selected (count), the number of strands being used, and
        #the length of thread in inches required to make a stitch with one strand.
        global outputWindow
        outputWindow = tk.Toplevel(window)
        outputWindow.title("Thread Requirements")
        #a new window opens, showing the following 3 checkboxes for units of measurement
        global chkval_inch
        chkval_inch = tk.BooleanVar()
        global chk_inch
        chk_inch = tk.Checkbutton(outputWindow, variable = chkval_inch, text = "inches", command = lambda: inchChecked(None))
        chk_inch.grid(row = 0, column = 0)
        global chkval_cm
        chkval_cm = tk.BooleanVar()
        global chk_cm
        chk_cm = tk.Checkbutton(outputWindow, variable = chkval_cm, text = "centimeters", command = lambda: cmChecked(None))
        chk_cm.grid(row = 0, column = 1)
        global chkval_skein
        chkval_skein = tk.BooleanVar()
        global chk_skein
        chk_skein = tk.Checkbutton(outputWindow, variable = chkval_skein, text = "skeins (each 8m of 6-strand floss)", command = lambda: skeinChecked(None))
        chk_skein.grid(row = 0, column = 2)

#defining window    
window = tk.Tk()
window.title("Cross stitch helper")

#first row: pattern file entry
lbl_fileName = tk.Label(text = "Pattern file name: ")
lbl_fileName.grid(row = 0, column = 0)
fileName = tk.Entry(width = 15)
fileName.grid(row = 0, column = 1)

#second row: fabric count selection
lbl_fabricCount = tk.Label(text = "Fabric count: ")
lbl_fabricCount.grid(row = 1, column = 0)
aida_types = ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]
clicked = tk.StringVar()
clicked.set("18")
fabricCount = tk.OptionMenu(window, clicked, *aida_types)
fabricCount.grid(row = 1, column = 1)

#third row: strand count selection
lbl_strands = tk.Label(text = "Number of strands: ")
lbl_strands.grid(row = 2, column = 0)
strand_options = ["1", "2", "3", "4", "5", "6"]
strandClicked = tk.StringVar()
strandClicked.set("2")
strands = tk.OptionMenu(window, strandClicked, *strand_options)
strands.grid(row = 2, column = 1)

#fourth row: status bar and go button
lbl_file = tk.Label(text = "")
lbl_file.grid(row = 3, column = 0)
btnConvert = tk.Button(
    master = window,
    text = "Analyze pattern",
    width = 17,
    height = 1,
    command = Convert_file)
btnConvert.grid(row = 3, column = 1)

window.mainloop()
