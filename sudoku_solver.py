import pygame
import time
import random
from copy import deepcopy
from sudokutools import is_valid_placement as check_valid_move, solve_puzzle as solve_board, locate_empty_cell as find_empty_cell, create_puzzle as generate_sudoku_board

pygame.init()

class SudokuGrid:
    def __init__(self, window):
        """
        Initializes the Sudoku grid.
        """
        self.grid = generate_sudoku_board()
        self.solved_grid = deepcopy(self.grid)
        solve_board(self.solved_grid)
        self.cells = [
            [Cell(self.grid[i][j], window, i * 60, j * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window

    def render_grid(self):
        """Draws the Sudoku grid on the window."""
        for row in range(9):
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (col // 3 * 180, 0), (col // 3 * 180, 540), 4)
                if row % 3 == 0 and row != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, row // 3 * 180), (540, row // 3 * 180), 4)
                self.cells[row][col].draw_cell((0, 0, 0), 1)
                if self.cells[row][col].value != 0:
                    self.cells[row][col].display_value(self.cells[row][col].value, (21 + col * 60, 16 + row * 60), (0, 0, 0))
        pygame.draw.line(self.window, (0, 0, 0), (0, (row + 1) // 3 * 180), (540, (row + 1) // 3 * 180), 4)

    def deselect_cell(self, selected_cell):
        """Deselects all cells except the given one."""
        for row in range(9):
            for col in range(9):
                if self.cells[row][col] != selected_cell:
                    self.cells[row][col].selected = False

    def refresh_grid(self, user_inputs, incorrect_count, time_elapsed):
        """Redraws the grid with highlights, wrong attempts, and time."""
        self.window.fill((255, 255, 255))
        self.render_grid()
        for row in range(9):
            for col in range(9):
                if self.cells[col][row].selected:
                    self.cells[col][row].draw_cell((50, 205, 50), 4)
                elif self.cells[row][col].is_correct:
                    self.cells[col][row].draw_cell((34, 139, 34), 4)
                elif self.cells[row][col].is_incorrect:
                    self.cells[col][row].draw_cell((255, 0, 0), 4)
        if len(user_inputs) != 0:
            for position in user_inputs:
                self.cells[position[0]][position[1]].display_value(user_inputs[position], (21 + position[0] * 60, 16 + position[1] * 60), (128, 128, 128))
        if incorrect_count > 0:
            font = pygame.font.SysFont("Bauhaus 93", 30)
            text = font.render("X", True, (255, 0, 0))
            self.window.blit(text, (10, 554))
            font = pygame.font.SysFont("Bahnschrift", 40)
            text = font.render(str(incorrect_count), True, (0, 0, 0))
            self.window.blit(text, (32, 542))
        font = pygame.font.SysFont("Bahnschrift", 40)
        text = font.render(str(time_elapsed), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visual_solve(self, incorrect_count, time_elapsed):
        """Recursively solves the Sudoku grid with a visual effect."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        empty_cell = find_empty_cell(self.grid)
        if not empty_cell:
            return True
        for num in range(9):
            if check_valid_move(self.grid, (empty_cell[0], empty_cell[1]), num + 1):
                self.grid[empty_cell[0]][empty_cell[1]] = num + 1
                self.cells[empty_cell[0]][empty_cell[1]].value = num + 1
                self.cells[empty_cell[0]][empty_cell[1]].is_correct = True
                self.refresh_grid({}, incorrect_count, time_elapsed)
                if self.visual_solve(incorrect_count, time_elapsed):
                    return True
                self.grid[empty_cell[0]][empty_cell[1]] = 0
                self.cells[empty_cell[0]][empty_cell[1]].value = 0
                self.cells[empty_cell[0]][empty_cell[1]].is_incorrect = True
                self.cells[empty_cell[0]][empty_cell[1]].is_correct = False
                self.refresh_grid({}, incorrect_count, time_elapsed)

    def provide_hint(self, user_inputs):
        """Provides a hint by filling in a random empty cell with the correct number."""
        while True:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] == 0:
                if (col, row) in user_inputs:
                    del user_inputs[(col, row)]
                self.grid[row][col] = self.solved_grid[row][col]
                self.cells[row][col].value = self.solved_grid[row][col]
                return True
            elif self.grid == self.solved_grid:
                return False


class Cell:
    def __init__(self, value, window, x_pos, y_pos):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x_pos, y_pos, 60, 60)
        self.selected = False
        self.is_correct = False
        self.is_incorrect = False

    def draw_cell(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display_value(self, value, position, color):
        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def is_clicked(self, mouse_position):
        if self.rect.collidepoint(mouse_position):
            self.selected = True
        return self.selected


def start_game():
    screen = pygame.display.set_mode((540, 590))
    pygame.display.set_caption("Sudoku Solver")
   

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Random Grid", True, (0, 0, 0))
    screen.blit(text, (156, 290))
    pygame.display.flip()

    incorrect_count = 0
    sudoku_grid = SudokuGrid(screen)
    selected_cell = (-1, -1)
    user_inputs = {}
    solved = False
    start_time = time.time()

    while not solved:
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        if sudoku_grid.grid == sudoku_grid.solved_grid:
            solved = True

        for event in pygame.event.get():
            elapsed_time = time.time() - start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                for row in range(9):
                    for col in range(9):
                        if sudoku_grid.cells[row][col].is_clicked(mouse_position):
                            selected_cell = (row, col)
                            sudoku_grid.deselect_cell(sudoku_grid.cells[row][col])
            elif event.type == pygame.KEYDOWN:
                if sudoku_grid.grid[selected_cell[1]][selected_cell[0]] == 0 and selected_cell != (-1, -1):
                    if event.key == pygame.K_1:
                        user_inputs[selected_cell] = 1
                    if event.key == pygame.K_2:
                        user_inputs[selected_cell] = 2
                    if event.key == pygame.K_3:
                        user_inputs[selected_cell] = 3
                    if event.key == pygame.K_4:
                        user_inputs[selected_cell] = 4
                    if event.key == pygame.K_5:
                        user_inputs[selected_cell] = 5
                    if event.key == pygame.K_6:
                        user_inputs[selected_cell] = 6
                    if event.key == pygame.K_7:
                        user_inputs[selected_cell] = 7
                    if event.key == pygame.K_8:
                        user_inputs[selected_cell] = 8
                    if event.key == pygame.K_9:
                        user_inputs[selected_cell] = 9
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                        if selected_cell in user_inputs:
                            sudoku_grid.cells[selected_cell[1]][selected_cell[0]].value = 0
                            del user_inputs[selected_cell]
                    elif event.key == pygame.K_RETURN:
                        if selected_cell in user_inputs:
                            if user_inputs[selected_cell] != sudoku_grid.solved_grid[selected_cell[1]][selected_cell[0]]:
                                incorrect_count += 1
                                sudoku_grid.cells[selected_cell[1]][selected_cell[0]].value = 0
                                del user_inputs[selected_cell]
                            sudoku_grid.cells[selected_cell[1]][selected_cell[0]].value = user_inputs[selected_cell]
                            sudoku_grid.grid[selected_cell[1]][selected_cell[0]] = user_inputs[selected_cell]
                            del user_inputs[selected_cell]

                if event.key == pygame.K_h:
                    sudoku_grid.provide_hint(user_inputs)
                if event.key == pygame.K_SPACE:
                    for row in range(9):
                        for col in range(9):
                            sudoku_grid.cells[row][col].selected = False
                    user_inputs = {}
                    sudoku_grid.visual_solve(incorrect_count, formatted_time)
                    solved = True

        sudoku_grid.refresh_grid(user_inputs, incorrect_count, formatted_time)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


start_game()
pygame.quit()
