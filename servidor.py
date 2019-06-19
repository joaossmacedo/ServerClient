# -*- coding: utf-8 -*-
import socket
from TicTacToe import *
import re
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('conectado a %s:%s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# regular expression to check if the data received is in the right format
format_regex = re.compile('(\([0-2],[0-2]\))')
# regular expression to check if the error is on the format or in the number passed
error_regex = re.compile('(\([0-9],[0-9]\))')

while True:
    # Wait for a connection
    number_of_moves = 0
    tiles = range(9)
    print 'esperando uma conexão'
    connection, client_address = sock.accept()
    try:
        print('conexao de %s:%s\n' % client_address)

        while True:
            data = connection.recv(255)
            if data:
                if format_regex.match(data):
                    col = int(data.split(',')[0][-1])
                    row = int(data.split(',')[1][0])

                    if tiles[row * 3 + col] == PLAYER or tiles[row * 3 + col] == CPU_PLAYER\
                            or row < 0 or row > 3 or col < 0 or col > 3:
                        print '<-- movimento não é possivel'
                        connection.sendall("movimento não é possivel")
                    else:
                        tiles = manual_move(tiles, col, row)
                        print_board(tiles)
                        print '\n<-- movimento do jogador realizado\n'

                        number_of_moves += 1
                        if check_end_game(tiles, number_of_moves) == "":
                            tiles = ai_move(tiles)
                            number_of_moves += 1
                            if check_end_game(tiles, number_of_moves) == "":
                                print_board(tiles)
                                print '\n<-- movimento do computador realizado\n'
                                connection.sendall(format_board(tiles))
                            else:
                                print '\n<-- fim de jogo'
                                connection.sendall(format_board(tiles) + "End Game" + check_end_game(tiles, number_of_moves))
                        else:
                            print '\n<-- fim de jogo'
                            connection.sendall(format_board(tiles) + "End Game" + check_end_game(tiles, number_of_moves))
                else:
                    print "erro nos dados passados"
                    if error_regex.match(data):
                        connection.sendall("Os valores passados não estão entre 0 e 2")
                    else:
                        connection.sendall("Os valores passados não está no formato correto")
            else:
                print('\n\n')
                print('fim dos dados', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
