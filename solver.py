from copy import deepcopy

def nums_row(row, sudoku):
    return set(sudoku[row][:])

def nums_col(col, sudoku):
    return {sudoku[r][col] for r in range(9)}

def nums_3x3(row, col, sudoku):
    r_start = 3 * (row // 3)
    c_start = 3 * (col // 3)
    return {sudoku[r_start + r][c_start + c] for r in range(3) for c in range(3)}

def avail_in_cell(row, col, sudoku):
    nums = {n for n in range(1,10)}
    # remove already existent in current row
    nums -= nums_row(row, sudoku)
    # ...and in current col
    nums -= nums_col(col, sudoku)
    # ...and in current 3x3
    nums -= nums_3x3(row, col, sudoku)
    return nums

def fail_in_row(row, sudoku):
    r = []
    for c in range(9):
        if sudoku[row][c] == 0:
            continue
        if not sudoku[row][c] in r:
            r.append(sudoku[row][c])
        else:
            return True
    return False

def fail_in_col(col, sudoku):
    c = []
    for r in range(9):
        if sudoku[r][col] == 0:
            continue
        if not sudoku[r][col] in c:
            c.append(sudoku[r][col])
        else:
            return True
    return False

def fail_in_3x3(row, col, sudoku):
    x3 = []
    r_start = 3 * (row // 3)
    c_start = 3 * (col // 3)
    for r in range(3):
        for c in range(3):
            if sudoku[r_start + r][c_start + c] == 0:
                continue
            if not sudoku[r_start + r][c_start + c] in x3:
                x3.append(sudoku[r_start + r][c_start + c])
            else:
                return True
    return False

def recursive_solver(sudoku):
    while True:
        min = None
        for r in range(9):
            for c in range(9):
                if sudoku[r][c] != 0:
                    continue
                if fail_in_row(r, sudoku) or fail_in_col(c, sudoku) or fail_in_3x3(r, c, sudoku):
                    return False
                avail = avail_in_cell(r, c, sudoku)
                avail_cnt = len(avail)
                if avail_cnt == 0:
                    return False
                if avail_cnt == 1:
                    sudoku[r][c] = avail.pop()
                if not min or avail_cnt < len(min[1]):
                    min = ((r, c), avail)
        if not min:
            return True
        elif 1 < len(min[1]):
            break
    r, c = min[0]
    for num in min[1]:
        sub_solved = deepcopy(sudoku)
        sub_solved[r][c] = num
        if recursive_solver(sub_solved):
            for row in range(9):
                for col in range(9):
                    sudoku[row][col] = sub_solved[row][col]
            return True
    return False

def SolveSudoku(sudoku):
    result = deepcopy(sudoku)
    if recursive_solver(result):
        return result
    return None

