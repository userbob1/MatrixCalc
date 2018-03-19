import tkinter as tk
from Matrix_Calculator import Matrix
from copy import deepcopy
from fractions import Fraction

root = tk.Tk(className="Matrix Calculator")
variables = {}

def mat_input(inp):
# Allows a matrix to be input in the console, done by row. An empty row indicates to stop reading.
    accept = ["0","1","2","3","4","5","6","7","8","9"]
    content = []
    print(inp.splitlines())
    for line in inp.splitlines():  # inp.splitlines are rows
        row = []
        for entry in line.split(" "):  #line.split is entries
            clean = ""
            fraction = 0
            for char in entry:
                if char in accept:
                    clean += char
                elif char == "/":
                    fraction = len(clean)
                    clean += char
            if fraction > 0:
                row.append(Fraction(int(clean[:fraction]), int(clean[fraction+1:])))
            else:
                row.append(int(clean))
        content.append(row)
    return Matrix(content)


def link_var():
    # Links input with variable
    var = mat_input(var_in.get('1.0','end'))
    variables[var_out.get('1.0','end -1 c')] = var
    print(var)
    print(variables)

def solve():
    print(eval(exp_in.get('1.0','end -1 c')))

var_in = tk.Text(root, width = 32, height = 8)
set_var = tk.Button(root, text = "    =    ", command = link_var)
var_out = tk.Text(root, width = 4, height = 1)
exp_in = tk.Text(root, width = 20, height = 1)
solve = tk.Button(root, text = "Solve", command = solve)

var_in.grid(row = 0, padx = 16, pady = 16)
var_out.grid(row = 0, column = 2, padx = 16)
set_var.grid(row = 0, column = 1, pady = 16)
exp_in.grid(row = 1, column = 0, columnspan = 2, pady = 8)
solve.grid(row = 1, column = 2, padx = 18, pady = 10)


root.mainloop()
