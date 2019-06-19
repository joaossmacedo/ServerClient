import socket
from TicTacToe import *
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


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
                            print('<-- sending board back to the client')
                            connection.sendall(format_board(tiles))
                        else:
                            connection.sendall(format_board(tiles) + "\nEnd Game\n" + check_end_game(tiles, number_of_moves))
                    else:
                        connection.sendall(format_board(tiles) + "\nEnd Game\n" + check_end_game(tiles, number_of_moves))
            else:
                print('\n\n')
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
