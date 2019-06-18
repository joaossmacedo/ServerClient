from __future__ import absolute_import
from Tree import Tree
import sys
from itertools import ifilter

# when playing against the cpu, the player is always the player 1
PLAYER_1 = u'x'
PLAYER_2 = u'o'


class Game(object):
    def __init__(self):
        self._number_of_moves = 0
        self.winner = u'N'
        self.tiles = range(9)

    # prints the board
    def print_board(self):
        print u'\n'
        for i in range(9):
            if self.tiles[i] == PLAYER_1 or self.tiles[i] == PLAYER_2:
                print u' ' + self.tiles[i] + u' ',; sys.stdout.write(u'')
            else:
                print u' - ',; sys.stdout.write(u'')
            if (i + 1) % 3 == 0:
                print u''
        print

    # movement by the player
    def manual_move(self):
        while True:
            while True:
                column = raw_input(u'Select a column: ')
                if u'0' <= column < u'3':
                    column = int(column)
                    break
            while True:
                line = raw_input(u'Select a line: ')
                if u'0' <= line < u'3':
                    line = int(line)
                    break
            if self.tiles[line * 3 + column] != PLAYER_2 and self.tiles[line * 3 + column] != PLAYER_1:
                break
        if self._number_of_moves % 2 == 0:
            self.tiles[line * 3 + column] = PLAYER_1
        else:
            self.tiles[line * 3 + column] = PLAYER_2

    # movement by the CPU
    def ai_move(self):
        print u'thinking ...',; sys.stdout.write( u'')

        possibilities = Tree()

        # simulates all the possibilities
        possibilities.simulate(self.tiles)

        possibilities.calculate_tree_height()

        chances = []

        for i in range(len(self.empty_tiles(self.tiles))):
            # calculates the difference between wins and looses in each of the next plays
            chances.append(possibilities.sum(possibilities.root.next[i]))

        # identify the best chance
        best_chance = max(chances)

        best_chance_index = chances.index(best_chance)

        self.tiles = possibilities.root.next[best_chance_index].tiles

    # a game
    def play(self):
        while True:
            number_of_players = raw_input(u'How many players(MAX: 2): ')
            if u'0' < number_of_players < u'3':
                number_of_players = int(number_of_players)
                break

        while not self.check_end_game(self.tiles) and self._number_of_moves < 9:
            self.print_board()
            if number_of_players == 2 or self._number_of_moves % 2 == 0:
                self.manual_move()
            else:
                self.ai_move()
            self._number_of_moves += 1
        self.print_board()

        if self.winner == PLAYER_1:
            print u"\nCongrats player X\n"
        elif self.winner == PLAYER_2:
            print u"\nCongrats player O\n"
        else:
            print u"\nTIC TAC TIE\n"

    # defines if a game is over or not
    def check_end_game(self, tiles):
        r = False
        # X
        if tiles[0] == PLAYER_1 and tiles[1] == PLAYER_1 and tiles[2] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        elif tiles[3] == PLAYER_1 and tiles[4] == PLAYER_1 and tiles[5] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        elif tiles[6] == PLAYER_1 and tiles[7] == PLAYER_1 and tiles[8] == PLAYER_1:
            self.winner = PLAYER_1
            r = True

        elif tiles[0] == PLAYER_1 and tiles[3] == PLAYER_1 and tiles[6] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        elif tiles[1] == PLAYER_1 and tiles[4] == PLAYER_1 and tiles[7] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        elif tiles[2] == PLAYER_1 and tiles[5] == PLAYER_1 and tiles[8] == PLAYER_1:
            self.winner = PLAYER_1
            r = True

        elif tiles[0] == PLAYER_1 and tiles[4] == PLAYER_1 and tiles[8] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        elif tiles[2] == PLAYER_1 and tiles[4] == PLAYER_1 and tiles[6] == PLAYER_1:
            self.winner = PLAYER_1
            r = True
        # O
        elif tiles[0] == PLAYER_2 and tiles[1] == PLAYER_2 and tiles[2] == PLAYER_2:
            self.winner = PLAYER_2
            r = True
        elif tiles[3] == PLAYER_2 and tiles[4] == PLAYER_2 and tiles[5] == PLAYER_2:
            self.winner = PLAYER_2
            r = True
        elif tiles[6] == PLAYER_2 and tiles[7] == PLAYER_2 and tiles[8] == PLAYER_2:
            self.winner = PLAYER_2
            r = True

        elif tiles[0] == PLAYER_2 and tiles[3] == PLAYER_2 and tiles[6] == PLAYER_2:
            self.winner = PLAYER_2
            r = True
        elif tiles[1] == PLAYER_2 and tiles[4] == PLAYER_2 and tiles[7] == PLAYER_2:
            self.winner = PLAYER_2
            r = True
        elif tiles[2] == PLAYER_2 and tiles[5] == PLAYER_2 and tiles[8] == PLAYER_2:
            self.winner = PLAYER_2
            r = True

        elif tiles[0] == PLAYER_2 and tiles[4] == PLAYER_2 and tiles[8] == PLAYER_2:
            self.winner = PLAYER_2
            r = True
        elif tiles[2] == PLAYER_2 and tiles[4] == PLAYER_2 and tiles[6] == PLAYER_2:
            self.winner = PLAYER_2
            r = True

        return r

    # return the empty tiles
    def empty_tiles(self, tiles):
        return list(ifilter(lambda x: x != PLAYER_2 and x != PLAYER_1, tiles))


game = Game()
game.play()
