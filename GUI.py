"""
This is the GUI component of my Sudoku project.
It (1) visualizes a Sudoku board and (2) enables the user to play the game.
Further, it (3) incorporates button functionality to set the difficulty, go for a new game and
(4) automatically solves the board, visually displaying the backtracking algorithm.
It does all this (5) by using Object-Oriented Programming (OOP).
It encompasses everything related to the GUI using pygame.
"""

import pygame as pg
import sys
import solver_and_generator

pg.init()


class Board:
    """
    The board class allows to create a sudoku board filled with cubes, the respective squares.
    It comes with a multitude of functionality to manipulate selection, values, drawing and more.
    """

    solver_and_generator.generate_new_board()
    board = solver_and_generator.board

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[y][x], y, x, width, height) for x in range(cols)] for y in range(rows)]
        self.width = width
        self.height = height
        self.grid = None
        self.selected = None

    def update_grid(self):
        """
        Updates the grid with the cube values
        :return: None
        """
        self.grid = [[self.cubes[y][x].value for x in range(self.cols)] for y in range(self.rows)]

    def click(self, pos):
        """
        Uses the position of the mouse to return the relevant cube
        :param: pos
        :return: Tuple: position (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            sidelength = self.width / 9
            x = pos[0] // sidelength
            y = pos[1] // sidelength
            return int(x), int(y)
        else:
            return None

    def select(self, row, col):
        """
        Selects the cube by returning a boolean
        :param row: int (row of cube)
        :param col: int (column of cube)
        :return: Boolean
        """
        # Unselect all cubes
        for y in range(self.rows):
            for x in range(self.cols):
                self.cubes[y][x].selected = False

        # Select cube in question
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def set_temp(self, value):
        """
        Sets the temporary value of the cube
        :param value: int
        :return: None
        """
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def reset_temp(self):

        for y in range(self.rows):
            for x in range(self.cols):
                self.cubes[y][x].set_temp(0)

    def place(self, value):
        """
        Places a value inside a cube and
        returns if the attempt was successful (if the cube in question was empty before)
        :param value: int
        :return: Boolean
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_val(value)
            self.update_grid()

            if solver_and_generator.possible(col, row, value) and solver_and_generator.solve():
                return True
            else:
                self.cubes[row][col].set_val(0)
                self.cubes[row][col].set_temp(0)
                self.update_grid()
                return False

    def draw(self):
        """
        Draws the grid and the cubes
        :return: None
        """
        global screen
        # Draw Grid Lines
        sidelength = self.width / 9
        for y in range(self.rows + 1):
            if y % 3 == 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(screen, (0, 0, 0), (0, y * sidelength), (self.width, y * sidelength), thick)
            pg.draw.line(screen, (0, 0, 0), (y * sidelength, 0), (y * sidelength, self.height), thick)

        # Draw Cubes
        for y in range(self.rows):
            for x in range(self.cols):
                self.cubes[y][x].draw()

    def clear(self):
        """
        If the cube in question is empty (0), set the temporary value to 0
        :return: None
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def is_finished(self):
        """
        Checks if the board is full
        :return: Boolean
        """
        for y in range(self.rows):
            for x in range(self.cols):
                if self.cubes[y][x].value == 0:
                    return False
        return True

    def update_cubes(self):
        """
        Updates the board.cubes using the solver_and_generator.py board
        :return: None
        """
        for y in range(9):
            for x in range(9):
                new_val = solver_and_generator.board[y][x]
                self.cubes[y][x].set_val(new_val)

    def possible(self, y, x, n):
        """
        Checks if number n can be input into [y][x] according to Sudoku rules
        :param y: current y-value of board
        :param x: current x-value of board
        :param n: number that is being attempted to be input
        :return: Boolean
        """

        # checks if the number already exists in the current row
        for i in range(9):
            if self.grid[y][i] == n:
                return False
        # checks if the number already exists in the current column
        for i in range(9):
            if self.grid[i][x] == n:
                return False
        # checks if the number already exists in the current square
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[y0 + i][x0 + j] == n:
                    return False
        # if n does not already exist in its row, column or square, it is possible in location [y][x]
        return True

    def solve_gui(self):
        """
        Solves the board using a backtracking algorithm and
        sets the global board variable to the first possible solution
        :return: None
        """
        global board
        self.update_grid()

        # base case
        if self.is_finished():
            return True

        # recursive case
        else:
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.cubes[x][y].value == 0:
                        for n in range(1, 10):
                            if board.possible(x, y, n):
                                self.cubes[x][y].set_val(n)
                                self.update_grid()
                                self.cubes[x][y].draw_change(True)
                                pg.display.update()
                                pg.time.delay(100)

                                if board.solve_gui():
                                    return True

                                self.cubes[x][y].set_val(0)
                                self.update_grid()
                                self.cubes[x][y].draw_change(False)
                                pg.display.update()
                                pg.time.delay(100)

                        return False


class Cube:
    """
    Cubes are the constituents of board objects.
    """
    row = 9
    col = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self):
        """
        Draws the cube-values on the board
        :return: None
        """""
        global screen

        sidelength = self.width / 9
        x = self.row * sidelength
        y = self.col * sidelength

        if self.value == 0 and self.temp != 0:
            text = font.render(str(self.temp), True, (180, 180, 180))
            screen.blit(text, pg.Vector2((x + sidelength - text.get_width() + - 1, y + 3)))
        elif self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(text, pg.Vector2((x + (sidelength / 2 - text.get_width() / 2),
                                          y + (sidelength / 2 - text.get_height() / 2))))

        if self.selected:
            pg.draw.rect(screen, (255, 100, 0), (x, y, sidelength, sidelength), 3)

    def draw_change(self, correct=True):
        """
        Draws the changing cubes during the automatic backtracking solving.
        :param correct: Boolean
        :return: None
        """
        global screen

        sidelength = self.width / 9
        x = self.row * sidelength
        y = self.col * sidelength

        pg.draw.rect(screen, (255, 255, 255), (x + 3, y + 3, sidelength - 6, sidelength - 6))

        if correct:
            text = font.render(str(self.value), True, (0, 255, 0))
        else:
            text = font.render(str(self.value), True, (255, 0, 0))
        screen.blit(text, pg.Vector2((x + (sidelength / 2 - text.get_width() / 2),
                                      y + (sidelength / 2 - text.get_height() / 2))))

    def set_val(self, value):
        """
        Sets the value of a cube
        :param value: int
        :return: None
        """
        self.value = value

    def set_temp(self, value):
        """
        Sets the temporary value of a cube
        :param value: int
        :return: None
        """
        self.temp = value


class Button:
    """
    The Button class implements button creation and functions so we can work with buttons in the GUI.
    """

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False

    def draw(self, outline=None):
        """
        Draws the button in the GUI
        :param outline: Boolean (specifies if the button will have an outline)
        :return: None
        """

        global screen
        if outline:
            pg.draw.rect(screen, (0, 0, 0), (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 0)

        pg.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font_button = pg.font.SysFont('comicsans', 37)
            text = font_button.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        """
        Checks if the mouse position is over the button position
        :param pos: Current Mouse Position
        :return: Boolean
        """

        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

    def select(self):
        """
        Selects a button, used for difficulty button coloring
        :return: None
        """
        global difficulty_buttons
        for button in difficulty_buttons:
            button.color = (225, 225, 245)
            button.selected = False

        self.color = (10, 35, 185)
        self.selected = True


def draw_screen():
    """
    Draws the screen
    :return: None
    """

    screen.fill((255, 255, 255))
    board.draw()

    autosolve_button.draw(True)
    new_game_button.draw(True)


def display_lives():
    """
    Displays current lives text and icons in the GUI.
    :return: None
    """
    font_button = pg.font.SysFont('comicsans', 20)
    text = font_button.render('Remaining Lives:', True, (0, 0, 0))
    screen.blit(text, (553, 755))

    global lives
    for n in range(lives):
        screen.blit(health_icon, (563 + 50 * n, 790, 60, 60))


# Setting up global parameters
health_icon = pg.image.load('heart.png')
lives = 3

screen = pg.display.set_mode((720, 850))
font = pg.font.SysFont(name='idc', size=70)
board = Board(9, 9, 720, 720)

# initiate buttons
start_game_button = Button((225, 225, 225), 445, 730, 220, 70, "Start Game")
autosolve_button = Button((225, 225, 225), 18, 760, 220, 70, "Autosolve")
new_game_button = Button((225, 225, 225), 260, 760, 220, 70, "New Game")
# initiate difficulty buttons
difficulty1 = Button((225, 225, 245), 70, 380, 100, 60, "1")
difficulty2 = Button((225, 225, 245), 190, 380, 100, 60, "2")
difficulty3 = Button((225, 225, 245), 310, 380, 100, 60, "3")
difficulty4 = Button((225, 225, 245), 430, 380, 100, 60, "4")
difficulty5 = Button((225, 225, 245), 550, 380, 100, 60, "5")

difficulty_buttons = [difficulty1, difficulty2, difficulty3, difficulty4, difficulty5]


def setup_titlebar():
    """
    Sets up the title-bar visuals
    :return: None
    """
    # Title and Icon
    pg.display.set_caption("Sudoku Autosolver")
    icon = pg.image.load('icon.png')
    pg.display.set_icon(icon)


def write_text(text, font, color, y):
    """
    Function to write text in the GUI
    :param text: String
    :param font: pg.font.SysFont
    :param color: RGB tuple
    :param y: int (vertical position)
    :return: None
    """
    global screen

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = ((750 / 2 - textobj.get_width() / 2), y)
    screen.blit(textobj, textrect)


def main_menu():
    """
    The main menu to select difficulty and enter the game.
    :return: None
    """
    setup_titlebar()
    while True:

        # sets up the main_menu screen
        welcome_font = pg.font.SysFont('comicsans', 37, True)
        text_font = pg.font.SysFont('comicsans', 30)

        screen.fill((255, 255, 255))

        start_game_button.draw(True)
        difficulty1.draw()
        difficulty2.draw()
        difficulty3.draw()
        difficulty4.draw()
        difficulty5.draw()

        write_text("Welcome to mudandstars' Sudoku", welcome_font, (0, 0, 0), 60)
        write_text("Please select your desired level", text_font, (0, 0, 0), 250)
        write_text("of difficulty (0-5)", text_font, (0, 0, 0), 300)

        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # colors the buttons when hovering over them
            if event.type == pg.MOUSEMOTION:
                if start_game_button.is_over(pos):
                    start_game_button.color = (185, 185, 185)
                elif not start_game_button.is_over(pos):
                    start_game_button.color = (225, 225, 225)

                if difficulty1.is_over(pos) and not difficulty1.selected:
                    difficulty1.color = (100, 150, 200)
                elif not difficulty1.is_over(pos) and not difficulty1.selected:
                    difficulty1.color = (225, 225, 245)
                if difficulty2.is_over(pos) and not difficulty2.selected:
                    difficulty2.color = (100, 150, 200)
                elif not difficulty2.is_over(pos) and not difficulty2.selected:
                    difficulty2.color = (225, 225, 245)
                if difficulty3.is_over(pos) and not difficulty3.selected:
                    difficulty3.color = (100, 150, 200)
                elif not difficulty3.is_over(pos) and not difficulty3.selected:
                    difficulty3.color = (225, 225, 245)
                if difficulty4.is_over(pos) and not difficulty4.selected:
                    difficulty4.color = (100, 150, 200)
                elif not difficulty4.is_over(pos) and not difficulty4.selected:
                    difficulty4.color = (225, 225, 245)
                if difficulty5.is_over(pos) and not difficulty5.selected:
                    difficulty5.color = (100, 150, 200)
                elif not difficulty5.is_over(pos) and not difficulty5.selected:
                    difficulty5.color = (225, 225, 245)

            # functionality to enter the game using space
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    game_loop()

            # adds functionality to the buttons
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_game_button.is_over(pos):
                    game_loop()

                if difficulty1.is_over(pos):
                    solver_and_generator.difficulty = 1
                    difficulty1.select()
                if difficulty2.is_over(pos):
                    solver_and_generator.difficulty = 2
                    difficulty2.select()
                if difficulty3.is_over(pos):
                    solver_and_generator.difficulty = 3
                    difficulty3.select()
                if difficulty4.is_over(pos):
                    solver_and_generator.difficulty = 4
                    difficulty4.select()
                if difficulty5.is_over(pos):
                    solver_and_generator.difficulty = 5
                    difficulty5.select()

        pg.display.update()


def game_loop():
    """
    The game loop to set up and run the GUI
    :return: None
    """
    setup_titlebar()
    global lives
    key = None

    while True:
        draw_screen()
        display_lives()

        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # colors the buttons when hovering over them
            if event.type == pg.MOUSEMOTION:
                if autosolve_button.is_over(pos):
                    autosolve_button.color = (185, 185, 185)
                elif not autosolve_button.is_over(pos):
                    autosolve_button.color = (225, 225, 225)
                if new_game_button.is_over(pos):
                    new_game_button.color = (185, 185, 185)
                elif not new_game_button.is_over(pos):
                    new_game_button.color = (225, 225, 225)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9

                if event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pg.K_ESCAPE:
                    for button in difficulty_buttons:
                        button.color = (225, 225, 245)
                    solver_and_generator.generate_new_board()
                    board.update_cubes()
                    board.reset_temp()
                    lives = 3
                    main_menu()
                if event.key == pg.K_SPACE:
                    board.solve_gui()

                if event.key == pg.K_RETURN:
                    y, x = board.selected
                    if board.cubes[y][x].temp != 0:
                        if board.place(board.cubes[y][x].temp):
                            print("Success. You entered a correct value. ")
                        else:
                            print("Wrong. This is no possible solution. ")
                            lives -= 1
                        key = None

            if event.type == pg.MOUSEBUTTONDOWN:
                click = board.click(pos)
                if click:
                    board.select(click[0], click[1])
                    key = None

                if autosolve_button.is_over(pos):
                    board.solve_gui()
                    key = None
                if new_game_button.is_over(pos):
                    solver_and_generator.generate_new_board()
                    board.update_cubes()
                    board.reset_temp()
                    lives = 3
                    for button in difficulty_buttons:
                        button.color = (225, 225, 245)
                    main_menu()

        if lives == 0:
            print("You lost.")
            for button in difficulty_buttons:
                button.color = (225, 225, 245)
            solver_and_generator.generate_new_board()
            board.update_cubes()
            board.reset_temp()
            lives = 3
            main_menu()

        if board.selected and key:
            board.set_temp(key)

        draw_screen()
        display_lives()
        pg.display.update()


if __name__ == '__main__':
    """
    The game is run in the GUI
    """
    main_menu()
