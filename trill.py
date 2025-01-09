import random


def generate_puzzle():
    """Generates a random valid Sudoku puzzle."""
    base = 3
    side = base * base

    def pattern(row, col): return (base * (row % base) + row // base + col) % side
    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))

    # Create a valid Sudoku grid
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # Remove some numbers to make it a puzzle
    squares = side * side
    empties = random.randint(40, 50)  # Number of cells to empty
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0
    print(board)
    return board


# Solve the puzzle using backtracking
def solve_puzzle(puzzle):
    """Solves the Sudoku puzzle using backtracking."""
    def is_valid(num, row, col):
        for i in range(9):
            if puzzle[row][i] == num or puzzle[i][col] == num:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if puzzle[i][j] == num:
                    return False
        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(num, i, j):
                            puzzle[i][j] = num
                            if backtrack():
                                return True
                            puzzle[i][j] = 0
                    return False
        return True

    backtrack()
    print(puzzle)
    return puzzle

board = generate_puzzle() # [[0, 0, 0, 3, 9, 0, 6, 1, 0], [0, 4, 0, 7, 0, 8, 9, 0, 2], [0, 2, 0, 1, 6, 0, 0, 7, 0], [2, 6, 0, 0, 1, 0, 7, 8, 9], [4, 5, 0, 0, 0, 0, 0, 2, 0], [0, 0, 7, 2, 0, 0, 1, 0, 5], [5, 7, 0, 0, 0, 0, 2, 0, 1], [0, 0, 8, 6, 2, 1, 0, 0, 0], [6, 0, 0, 5, 0, 0, 0, 9, 3]]

prvious_ans = [[7, 8, 5, 3, 9, 2, 6, 1, 4], [1, 4, 6, 7, 5, 8, 9, 3, 2], [3, 2, 9, 1, 6, 4, 5, 7, 8], [2, 6, 3, 4, 1, 5, 7, 8, 9], [4, 5, 1, 8, 7, 9, 3, 2, 6], [8, 9, 7, 2, 3, 6, 1, 4, 5], [5, 7, 4, 9, 8, 3, 2, 6, 1], [9, 3, 8, 6, 2, 1, 4, 5, 7], [6, 1, 2, 5, 4, 7, 8, 9, 3]]
ans = solve_puzzle(board)
if ans == prvious_ans:
    print("Correct")
else:
    print("Incorrect")


def display_puzzle(grid):
        puzzle_string = ""
        for row in range(9):
            for col in range(9):
                puzzle_string += str(grid[row][col]) + " "
                if (col + 1) % 3 == 0 and col != 0 and col + 1 != 9:
                    puzzle_string += "| "

                if col == 8:
                    puzzle_string += "\n"

                if col == 8 and (row + 1) % 3 == 0 and row + 1 != 9:
                    puzzle_string += "- - - - - - - - - - - \n"
        print(puzzle_string)
board = generate_puzzle()
display_puzzle(grid=board)
display_puzzle(grid=solve_puzzle(board))