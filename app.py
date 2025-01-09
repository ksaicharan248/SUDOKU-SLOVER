from flask import Flask, render_template, request, redirect, url_for, session
import random
import copy
app = Flask(__name__)
app.secret_key = 'sai'

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


def solve_puzzle(puzzle: list):
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
    return puzzle


# Generate a random Sudoku puzzle (placeholder for simplicity)
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
    puzzle = copy.deepcopy(board)
    fianl_puzzle = solve_puzzle(board)
    return puzzle, fianl_puzzle


# Solve the puzzle using backtracking



@app.route("/")
def index():
    puzzle,solved_puzzle = generate_puzzle()
    session['puzzle'] = puzzle
    session['solved_puzzle'] = solved_puzzle
    session['referrer'] = request.referrer
    return render_template("index.html", puzzle=puzzle , solved_puzzle= solved_puzzle)

@app.route("/solve", methods=["POST"])
def solve():
    print("i am here ")
    puzzle_data = request.form.getlist("cell")
    if len(puzzle_data) != 81:
        return "Error: Puzzle data must contain exactly 81 values."

    puzzle = []
    for i in range(0, 81, 9):
        row = []
        for j in range(9):
            value = puzzle_data[i + j]
            row.append(int(value) if value.strip() else 0)
        puzzle.append(row)

    solved_puzzle = solve_puzzle(puzzle)
    return render_template("solved.html", solved_puzzle=solved_puzzle)


@app.route("/show_solution")
def show_solution():
    solved_puzzle = session.get('solved_puzzle')
    return render_template("solved.html", solved_puzzle=solved_puzzle)

if __name__ == "__main__":
    app.run(debug=True)
    