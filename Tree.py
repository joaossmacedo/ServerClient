from __future__ import absolute_import
import copy
from itertools import ifilter


# when playing against the cpu, the player is always the player 1
PLAYER = 'x'
CPU_PLAYER = 'o'


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


# check end game situation and returns 1 for win and -1 for looses
def check_end_game(tiles):
    r = 0
    # X
    if tiles[0] == PLAYER and tiles[1] == PLAYER and tiles[2] == PLAYER:
        r = -1
    elif tiles[3] == PLAYER and tiles[4] == PLAYER and tiles[5] == PLAYER:
        r = -1
    elif tiles[6] == PLAYER and tiles[7] == PLAYER and tiles[8] == PLAYER:
        r = -1
    elif tiles[0] == PLAYER and tiles[3] == PLAYER and tiles[6] == PLAYER:
        r = -1
    elif tiles[1] == PLAYER and tiles[4] == PLAYER and tiles[7] == PLAYER:
        r = -1
    elif tiles[2] == PLAYER and tiles[5] == PLAYER and tiles[8] == PLAYER:
        r = -1

    elif tiles[0] == PLAYER and tiles[4] == PLAYER and tiles[8] == PLAYER:
        r = -1
    elif tiles[2] == PLAYER and tiles[4] == PLAYER and tiles[6] == PLAYER:
        r = -1
    # O
    elif tiles[0] == CPU_PLAYER and tiles[1] == CPU_PLAYER and tiles[2] == CPU_PLAYER:
        r = 1
    elif tiles[3] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[5] == CPU_PLAYER:
        r = 1
    elif tiles[6] == CPU_PLAYER and tiles[7] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
        r = 1

    elif tiles[0] == CPU_PLAYER and tiles[3] == CPU_PLAYER and tiles[6] == CPU_PLAYER:
        r = 1
    elif tiles[1] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[7] == CPU_PLAYER:
        r = 1
    elif tiles[2] == CPU_PLAYER and tiles[5] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
        r = 1

    elif tiles[0] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[8] == CPU_PLAYER:
        r = 1
    elif tiles[2] == CPU_PLAYER and tiles[4] == CPU_PLAYER and tiles[6] == CPU_PLAYER:
        r = 1

    return r


class Node(object):
    def __init__(self, tiles, depth):
        self.tiles = tiles
        self.depth = depth
        self.result = 0
        self.next = []

    def display(self, indent = 0):
        print(('    ' * indent) + str(self.tiles))
        for c in self.next:
            c.display(indent + 1)


class Tree(object):
    def __init__(self):
        self.root = None
        self.tree_height = 0

    # simulate all plays
    def simulate(self, init_tiles):
        self.root = Node(init_tiles, 0)
        self.__aux_simulate(self.root, CPU_PLAYER, 1)

    # auxiliary method to simulate the plays
    def __aux_simulate(self, node, player, depth):
        empty_tiles = list(ifilter(lambda x: x != PLAYER and x != CPU_PLAYER, node.tiles))

        if len(empty_tiles) <= 0:  # if all tiles are occupied
            return
        elif check_end_game(node.tiles) != 0:  # if its an end game situation
            node.result = check_end_game(node.tiles)
        else:
            # adds the next possible plays
            for i in xrange(len(empty_tiles)):
                pos = empty_tiles[i]
                new_tiles = copy.copy(node.tiles)
                new_tiles[pos] = player
                node_new_tiles = Node(new_tiles, depth)
                node.next.append(node_new_tiles)

            if player == CPU_PLAYER:
                player = PLAYER
            else:
                player = CPU_PLAYER

            for i in xrange(len(empty_tiles)):
                self.__aux_simulate(node.next[i], player, depth + 1)

    # sum all results
    def sum(self, node):
        next_sum = 0

        if node is None:
            return 0
        else:
            for i in xrange(len(node.next)):
                next_sum += self.sum(node.next[i])
            weight = factorial(self.tree_height - node.depth)
            return (weight * node.result) + next_sum

    # calculate tree height
    def calculate_tree_height(self):
        self.tree_height = self.__aux_calculate_tree_height(self.root)

    # auxiliary method to calculate the tree height
    def __aux_calculate_tree_height(self, p):
        if len(p.next) == 0:
            return 1
        else:
            return 1 + max(self.__aux_calculate_tree_height(x) for x in p.next)
