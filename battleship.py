#! /usr/bin/env python3

import os

import random
from random import randint

class Battleship():

    def __init__(self, num_turns, board_size, ship_count):

        # print (f"__init__ (num_turns: {num_turns})")

        self.num_turns = num_turns

        self.board = Battleship_Board (board_size, ship_count)

        # self.board.display()


    def play(self):

        print (f"play ()")

        for turn in range(self.num_turns):
            print("Turn:", turn + 1, "of", self.num_turns)
            print("Ships left:", len(self.board.ships))
            print()
        
            guess_coords = {}
            
            while True:
    
                row = self.get_number("Enter a row")
                column = self.get_number("Enter a column")
            
                if self.board.board[row][column] == 0:
                    break

                print("\nYou guessed that one already.")

            self.board.process_guess (row, column)

            os.system('clear')
            self.board.display_board()
            self.board.show_ships ()


    def get_number(self, prompt):

        while True:

            try:
                guess = int(input(f"{prompt}: "))
                
                if guess in range(1, self.board.number_of_rows + 1):
                    return guess-1
          
                print("\nOops, that's not even in the ocean.")
                    
            except ValueError:
                print("\nPlease enter a number")


class Battleship_Board:

    def __init__(self, length, ship_count):

        self.number_of_rows = length
        self.number_of_columns = length
        self.num_ships = ship_count

        self.board = [[0] * self.number_of_columns for x in range(self.number_of_rows)]

        self.setup_ships ()

        self.display_board ()
        self.show_ships ()


    def setup_ships (self):

        self.ships = []

        self.max_ship_size = 5
        self.min_ship_size = 2

        orientations = ["horizontal", "vertical"]

        ship_count = 0

        while ship_count < self.num_ships:
            random_size = randint (self.min_ship_size, self.max_ship_size)

            random_row = randint (0, self.number_of_rows-random_size)
            random_column  = randint (0, self.number_of_columns-random_size)

            random_orientation = random.choice(orientations)

            collision = False

            if random_orientation == "horizontal":

                for column in range (random_size):

                    for ship in self.ships:

                        if ship.test_hit (random_row, random_column + column):
                            collision = True

            else:
                for row in range (random_size):

                    for ship in self.ships:

                        if ship.test_hit (random_row+row, random_column):
                            collision = True

            if collision:
                print ("collision");
                continue

            self.ships.append (Ship (start_row=random_row, start_column=random_column, size=random_size, orientation=random_orientation))

            ship_count += 1


    def test_ships (self):

        test_board = [[' '] * self.number_of_columns for x in range(self.number_of_rows)]

        for row in range(self.number_of_rows):

            for column in range(self.number_of_columns):

                for ship in self.ships:

                    if ship.process_hit (row, column):
                        test_board [row][column] = 'x'

        self.print_board (test_board)


    def show_ships (self):

        test_board = [[' '] * self.number_of_columns for x in range(self.number_of_rows)]

        for ship in self.ships:

            if ship.orientation == 'horizontal':

                for i in range (ship.size):
                    test_board[ship.start_row][ship.start_column+i] = ship.status[i]

            if ship.orientation == 'vertical':

                for i in range (ship.size):
                    test_board[ship.start_row+i][ship.start_column] = ship.status[i]

        self.print_board (test_board)



    def process_guess (self, row, column):

        if self.board[row][column] != 0: return

        for ship in self.ships:

            if ship.hit_test (row, column):
                self.board [row][column] = 2
                return

        self.board[row][column] = 1


    def display_board (self):

        self.print_board (self.board)


    def print_board (self, board):

        print("\n  " + " ".join(str(x) for x in range(0, self.number_of_columns )))
        
        base = ord ('A')

        for r in range(self.number_of_rows):
            print(chr(base + r) + " " + " ".join(str(c) for c in board[r]))
            
        print()


class Ship:

    # ship_id = 1

    def __init__(self, start_row, start_column, size, orientation):

        self.size = size

        self.start_row = start_row
        self.start_column = start_column

        self.orientation = orientation

        self.status = [size for x in range(size)]

        # Ship.ship_id += 1


    def test_hit(self, row, column):

        if self.orientation == 'horizontal':

            if row != self.start_row: return False

            if column < self.start_column: return False

            if column > self.start_column + (self.size-1): return False

            return True


        if self.orientation == 'vertical':

            if column != self.start_column: return False

            if row < self.start_row: return False

            if row > self.start_row + (self.size-1): return False

            return True


    def process_hit(self, row, column):

        if self.orientation == 'horizontal':

            if row != self.start_row: return False

            if column < self.start_column: return False

            if column > self.start_column + (self.size-1): return False

            self.status [column-self.start_column] = 0
            return True


        if self.orientation == 'vertical':

            if column != self.start_column: return False

            if row < self.start_row: return False

            if row > self.start_row + (self.size-1): return False

            self.status [row-self.start_row] = 0
            return True


    def __repr__(self): 
        return f"(row={self.start_row}, column={self.start_column}, size={self.size}, orientation='{self.orientation}')"


game = Battleship (num_turns=40, board_size=10, ship_count=5)

game.play()
