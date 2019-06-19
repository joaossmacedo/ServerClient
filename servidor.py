import socket
from TicTacToe import *
import re
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
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
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        print('\n\n')

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(255)
            if data:
                if format_regex.match(data):
                    print_board(tiles)
                    col = int(data.split(',')[0][-1])
                    row = int(data.split(',')[1][0])

                    if tiles[row * 3 + col] == PLAYER or tiles[row * 3 + col] == CPU_PLAYER\
                            or row < 0 or row > 3 or col < 0 or col > 3:
                        print('<-- sending message back to the client')
                        connection.sendall("move not available")
                    else:
                        tiles = manual_move(tiles, col, row)
                        number_of_moves += 1
                        if check_end_game(tiles, number_of_moves) == "":
                            tiles = ai_move(tiles)
                            number_of_moves += 1
                            if check_end_game(tiles, number_of_moves) == "":
                                connection.sendall(format_board(tiles))
                            else:
                                connection.sendall(format_board(tiles) + "\nEnd Game\n" + check_end_game(tiles, number_of_moves))
                        else:
                            connection.sendall(format_board(tiles) + "\nEnd Game\n" + check_end_game(tiles, number_of_moves))
                else:
                    if error_regex.match(data):
                        connection.sendall("The values passed are not between 0 and 2")
                    else:
                        connection.sendall("The data is not on the right format")
            else:
                print('\n\n')
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
