# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Tree import Tree
import sys
from itertools import ifilter

PLAYER = 'x'
CPU_PLAYER = 'o'


def is_move_possible(tiles, col, row):
    if col < 0 or col > 2 or row < 0 or row > 2:
        return False
    if tiles[row * 3 + col] == CPU_PLAYER or tiles[row * 3 + col] == PLAYER:
        return False

    return True


# prints the board
def print_board(tiles):
    for i in range(9):
        if tiles[i] == PLAYER or tiles[i] == CPU_PLAYER:
            print ' ' + tiles[i] + u' ', ;
            sys.stdout.write(u'')
        else:
            print ' - ', ;
            sys.stdout.write(u'')
        if (i + 1) % 3 == 0:
            print ''

def format_board(tiles):
    r_tiles = ""
    for i in range(9):
        if tiles[i] == PLAYER or tiles[i] == CPU_PLAYER:
            r_tiles += ' ' + tiles[i] + ' '
        else:
            r_tiles += ' - '
        if (i + 1) % 3 == 0:
            r_tiles += '\n'
    return r_tiles


# movement by the player
def manual_move(original_tiles, col, row):
    tiles = original_tiles[:]

    tiles[row * 3 + col] = PLAYER

    return tiles


# movement by the CPU
def ai_move(original_tiles):
    tiles = original_tiles[:]

    possibilities = Tree()

    # simulates all the possibilities
    possibilities.simulate(tiles)

    possibilities.calculate_tree_height()

    chances = []

    for i in range(len(empty_tiles(tiles))):
        # calculates the difference between wins and looses in each of the next plays
        chances.append(possibilities.sum(possibilities.root.next[i]))

    # identify the best chance
    best_chance = max(chances)

    best_chance_index = chances.index(best_chance)

    tiles = possibilities.root.next[best_chance_index].tiles

    return tiles


# defines if a game is over or not
def check_end_game(tiles, number_of_moves):

    # X
    if (tiles[0] == PLAYER and tiles[1] == PLAYER and tiles[2] == PLAYER) or \
            (tiles[3] == PLAYER and tiles[4] == PLAYER and tiles[5] == PLAYER) or \
            (tiles[6] == PLAYER and tiles[7] == PLAYER and tiles[8] == PLAYER) or \
            (tiles[0] == PLAYER and tiles[3] == PLAYER and tiles[6] == PLAYER) or \
            (tiles[1] == PLAYER and tiles[4] == PLAYER and tiles[7] == PLAYER) or \
            (tiles[2] == PLAYER and tiles[5] == PLAYER and tiles[8] == PLAYER) or \
            (tiles[0] == PLAYER and tiles[4] == PLAYER and tiles[8] == PLAYER) or \
            (tiles[2] == PLAYER and tiles[4] == PLAYER and tiles[6] == PLAYER):
        return "\nParabens! Voce ganhou\n"

    # O
    if (tiles[0] == CPU_PLAYER and tiles[1] == CPU_PLAYER and tiles[2] == CPU_PLAYER) or \
            (tiles[3] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[5] == CPU_PLAYER) or \
            (tiles[6] == CPU_PLAYER and tiles[7] == CPU_PLAYER and tiles[8] == CPU_PLAYER) or \
            (tiles[0] == CPU_PLAYER and tiles[3] == CPU_PLAYER and tiles[6] == CPU_PLAYER) or \
            (tiles[1] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[7] == CPU_PLAYER) or \
            (tiles[2] == CPU_PLAYER and tiles[5] == CPU_PLAYER and tiles[8] == CPU_PLAYER) or \
            (tiles[0] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[8] == CPU_PLAYER) or \
            (tiles[2] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[6] == CPU_PLAYER):
        return "\nVoce perdeu\n"

    if number_of_moves >= 9:
        return "\nVoce empatou\n"

    return ""


# return the empty tiles
def empty_tiles(tiles):
    return list(ifilter(lambda x:x != CPU_PLAYER and x != PLAYER, tiles))

