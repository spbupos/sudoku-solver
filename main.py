import PySimpleGUI as gui
from time import time
from solver import SolveSudoku

def value_error():
    print("ERROR: you must input only integers from 1 to 9!")
    return None

def dict2arr(values):
    result = [[0 for i in range(9)] for j in range(9)]
    if type(values) is not dict:
        return result
    for r in range(9):
        for c in range(9):
            rc = values[str(r * 9 + c + 1)]
            if rc == '':
                result[r][c] = 0
                continue
            try:
                num = int(rc)
            except ValueError:
                return value_error()
            if num < 1 or num > 9:
                return value_error()
            result[r][c] = num
    return result

layout = [[gui.InputText(default_text='', key=str(row * 9 + col), size=(2,1)) for col in range(1,10)] for row in range(9)]

layout[0].append(gui.Button('Solve'))
layout[1].append(gui.Button('Clear'))
layout[2].append(gui.Button('Exit'))
layout.append([gui.Output(size=(30,3), key="output")])
window = gui.Window('Sudoku Solver v1.0', layout, resizable=True, finalize=True)
window.bind('<Configure>', "Configure")

while True:
    event, values = window.read()
    if event in [gui.WIN_CLOSED, "Exit"]:
        break
    if event == "Configure":
        window.refresh()

    if event == 'Solve':
        start = time()
        window['output'].Update('')
        sudoku = dict2arr(values)
        if not isinstance(sudoku, list):
            continue

        result = SolveSudoku(sudoku)
        if result == None:
            print("This sudoku isn't solvable :(")
        else:
            for i in range(81):
                window[str(i + 1)].Update(result[i // 9][i % 9])
            print("Solved succesfully in", "%.3f" % (time() - start), "secs")

    if event == "Clear":
        for i in range(81):
            window[str(i + 1)].Update('')
        window['output'].Update('')

