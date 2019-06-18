from __future__ import absolute_import
from Tree import Tree
import sys
from itertools import ifilter

# when playing against the cpu, the player is always the player 1
PLAYER = 'x'
CPU_PLAYER = 'o'


class Game(object):
    def __init__(self):
        self._number_of_moves = 0
        self.winner = 'N'
        self.tiles = range(9)

    def isMovePossible(self, col, row):
        if col < 0 or col > 2 or row < 0 or row > 2:
            return False
        if self.tiles[row * 3 + col] == CPU_PLAYER or self.tiles[row * 3 + col] == PLAYER:
            return False

        return True

    # prints the board
    def print_board(self):
        print u'\n'
        for i in range(9):
            if self.tiles[i] == PLAYER or self.tiles[i] == CPU_PLAYER:
                print ' ' + self.tiles[i] + u' ',; sys.stdout.write(u'')
            else:
                print ' - ',; sys.stdout.write(u'')
            if (i + 1) % 3 == 0:
                print ''
        print

    # movement by the player
    def manual_move(self, col, row):
        if self._number_of_moves % 2 == 0:
            self.tiles[row * 3 + col] = PLAYER
        else:
            self.tiles[row * 3 + col] = CPU_PLAYER

    # movement by the CPU
    def ai_move(self):
        print 'thinking ...',; sys.stdout.write( u'')

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
        while not self.check_end_game(self.tiles) and self._number_of_moves < 9:
            self.print_board()

            if self._number_of_moves % 2 == 0:
                col = -1
                row = -1
                while not self.isMovePossible(col, row):
                    row = int(raw_input('Select a row: '))
                    col = int(raw_input('Select a column: '))
                self.manual_move(col, row)
            else:
                self.ai_move()

            self._number_of_moves += 1
        self.print_board()

        if self.winner == PLAYER:
            print "\nCongrats you won\n"
        elif self.winner == CPU_PLAYER:
            print "\nYou lost\n"
        else:
            print "\nTIC TAC TIE\n"

    # defines if a game is over or not
    def check_end_game(self, tiles):
        r = False
        # X
        if tiles[0] == PLAYER and tiles[1] == PLAYER and tiles[2] == PLAYER:
            self.winner = PLAYER
            r = True
        elif tiles[3] == PLAYER and tiles[4] == PLAYER and tiles[5] == PLAYER:
            self.winner = PLAYER
            r = True
        elif tiles[6] == PLAYER and tiles[7] == PLAYER and tiles[8] == PLAYER:
            self.winner = PLAYER
            r = True

        elif tiles[0] == PLAYER and tiles[3] == PLAYER and tiles[6] == PLAYER:
            self.winner = PLAYER
            r = True
        elif tiles[1] == PLAYER and tiles[4] == PLAYER and tiles[7] == PLAYER:
            self.winner = PLAYER
            r = True
        elif tiles[2] == PLAYER and tiles[5] == PLAYER and tiles[8] == PLAYER:
            self.winner = PLAYER
            r = True

        elif tiles[0] == PLAYER and tiles[4] == PLAYER and tiles[8] == PLAYER:
            self.winner = PLAYER
            r = True
        elif tiles[2] == PLAYER and tiles[4] == PLAYER and tiles[6] == PLAYER:
            self.winner = PLAYER
            r = True
        # O
        elif tiles[0] == CPU_PLAYER and tiles[1] == CPU_PLAYER and tiles[2] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True
        elif tiles[3] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[5] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True
        elif tiles[6] == CPU_PLAYER and tiles[7] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True

        elif tiles[0] == CPU_PLAYER and tiles[3] == CPU_PLAYER and tiles[6] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True
        elif tiles[1] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[7] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True
        elif tiles[2] == CPU_PLAYER and tiles[5] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True

        elif tiles[0] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True
        elif tiles[2] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[6] == CPU_PLAYER:
            self.winner = CPU_PLAYER
            r = True

        return r

    # return the empty tiles
    def empty_tiles(self, tiles):
        return list(ifilter(lambda x: x != CPU_PLAYER and x != PLAYER, tiles))


game = Game()
game.play()
