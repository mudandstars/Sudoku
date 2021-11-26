"""
This is the Sudoku solver and generator component of my Sudoku Project.
It is capable of (1) creating entirely new Sudoku puzzles with varying difficulties and
(2) solving them for a single solution or multiple solutions.
"""

import numpy as np
from random import randint, shuffle

# initialises global board, solution counter and difficulty level
board_sample = [[7, 0, 0, 4, 0, 0, 1, 2, 0],
                [6, 0, 0, 0, 7, 5, 0, 0, 9],
                [0, 0, 0, 0, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 5],
                [0, 7, 0, 3, 0, 0, 0, 1, 2],
                [1, 2, 0, 0, 0, 7, 4, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0]]
board = []
counter = 0
difficulty = 2


def generate_empty_board():
    """
    Generates an (almost) empty 9x9 board in the global board variable
    :return: None
    """
    # initialize empty 9x9 board
    global board
    board = np.array(np.zeros((9, 9)))

    # randomly populate the grid
    populate_numbers = [i for i in range(9)]
    shuffle(populate_numbers)
    while populate_numbers:
        y = randint(0, 8)
        x = randint(0, 8)
        if board[y][x] == 0:
            board[y][x] = populate_numbers.pop()


def print_board():
    """
    Prints the current board
    :return: None
    """
    global board
    print(np.matrix(board))


def get_difficulty():
    """
    Reads user input for difficulty
    :return: None
    """
    global difficulty
    valid_values = [x for x in range(1, 6)]

    try:
        difficulty = int(input("Please enter a level of difficulty (1-5): "))
    except:
        print("Invalid value.")
        difficulty = int(input("Please enter a level of difficulty (1-5): "))

    while difficulty not in valid_values:
        try:
            difficulty = int(input("Please enter a level of difficulty from 1-5: "))
        except:
            print("Invalid value.")
            difficulty = int(input("Please enter a level of difficulty from 1-5: "))

    print(f"Thanks. Your difficulty is set to level {difficulty}.")


def check_board():
    """
    Checks if the board is full
    :return: Boolean
    """
    global board

    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                return False
    return True


def remove_numbers():
    """
    Removes numbers from the board to eventually arrive at a non-filled-in board
    The higher the difficulty int, the potentially harder to sudoku will be
    :return: None
    """
    global board
    global difficulty
    difficulty *= 10
    global counter
    counter = 0

    # while loop that removes numbers until grid has only one solution
    while difficulty > 0:

        # select a random cell that is not (already) empty
        y = randint(0, 8)
        x = randint(0, 8)
        while board[y][x] == 0:
            y = randint(0, 8)
            x = randint(0, 8)

        # save content of selected position and set it to 0
        backup = board[y][x]
        board[y][x] = 0

        # count number of solutions of the current board
        solve_multiple()

        # we want a sudoku with only exactly one solution, so if it has a different number of solutions,
        # put the last value back in
        if counter != 1:
            board[y][x] = backup
            difficulty -= 1


def possible(y, x, n):
    """
    Checks if number n can be input into [y][x] according to Sudoku rules
    :param y: current row of board
    :param x: current column of board
    :param n: number that is being attempted to be put in the board
    :return: Boolean
    """
    global board

    # checks if the number already exists in the current row
    for i in range(9):
        if board[y][i] == n:
            return False
    # checks if the number already exists in the current column
    for i in range(9):
        if board[i][x] == n:
            return False
    # checks if the number already exists in the current square
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[y0 + i][x0 + j] == n:
                return False
    # if n does not already exist in its row, column or square, it is possible in location [y][x]
    return True


def solve_multiple():
    """
    Solves the board using a backtracking algorithm and
    updates the global counter variable to the number of possible solutions
    :return: None
    """
    global board
    global counter
    counter = 0

    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        board[y][x] = n
                        solve_multiple()
                        board[y][x] = 0
                return False

    counter += 1


def solve():
    """
    Solves the board using a backtracking algorithm and sets the global board variable to the first possible solution
    :return: None
    """
    global board

    # base case
    if check_board():
        return True

    # recursive case
    else:
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    for n in range(1, 10):
                        if possible(y, x, n):
                            board[y][x] = n

                            if solve():
                                return True

                            board[y][x] = 0
                    return False


def make_board_integers():
    """
    Transforms all (float) numbers of the matrix into integers.
    :return: None
    """
    global board
    board = board.astype(int)


def generate_new_board():
    """
    Combines custom functions to create a new random board to use
    :return: None
    """
    generate_empty_board()
    solve()
    remove_numbers()
    make_board_integers()


if __name__ == "__main__":
    """
    Asks user for input to set difficulty level, then
    generates a new random boards and prints it. 
    Then proceeds to solve the board and print the solution.
    """
    get_difficulty()
    generate_new_board()
    print_board()
    solve()
    print_board()
