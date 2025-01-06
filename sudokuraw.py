#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, shuffle

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

def locate_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

def is_valid_placement(grid, cell, value):
    for row in range(9):
        if grid[row][cell[1]] == value:
            return False
    for col in range(9):
        if grid[cell[0]][col] == value:
            return False
    start_row = cell[0] - cell[0] % 3
    start_col = cell[1] - cell[1] % 3
    for row in range(3):
        for col in range(3):
            if grid[start_row + row][start_col + col] == value:
                return False
    return True

def solve_puzzle(grid):
    empty_cell = locate_empty_cell(grid)
    if not empty_cell:
        return True

    for value in range(1, 10):
        if is_valid_placement(grid, empty_cell, value):
            grid[empty_cell[0]][empty_cell[1]] = value

            if solve_puzzle(grid):
                return True

            grid[empty_cell[0]][empty_cell[1]] = 0
    return False

def create_puzzle():
    grid = [[0 for _ in range(9)] for _ in range(9)]

    for box_start in range(0, 9, 3):
        values = list(range(1, 10))
        shuffle(values)
        for row in range(3):
            for col in range(3):
                grid[box_start + row][box_start + col] = values.pop()

    def fill_remaining_cells(grid, row, col):
        if row == 9:
            return True
        if col == 9:
            return fill_remaining_cells(grid, row + 1, 0)

        if grid[row][col] != 0:
            return fill_remaining_cells(grid, row, col + 1)

        for value in range(1, 10):
            if is_valid_placement(grid, (row, col), value):
                grid[row][col] = value

                if fill_remaining_cells(grid, row, col + 1):
                    return True

        grid[row][col] = 0
        return False

    fill_remaining_cells(grid, 0, 0)

    for _ in range(randint(55, 65)):
        row, col = randint(0, 8), randint(0, 8)
        grid[row][col] = 0

    return grid

if __name__ == "__main__":
    puzzle_grid = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]
    print(puzzle_grid)
    display_puzzle(puzzle_grid)
    solve_puzzle(puzzle_grid)
    display_puzzle(puzzle_grid)
