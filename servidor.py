# -*- coding: utf-8 -*-
import socket
from TicTacToe import *
import re

# cria o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('conectado a %s:%s' % server_address)
sock.bind(server_address)

# fica ouvindo para identificar novas conexões
sock.listen(1)

# expressão regular para checar se os dados enviados pelo cliente estão corretos
error_regex = re.compile('(\([0-2],[0-2]\))')
# expressão regular para checar se o erro é no formato ou se os numeros estão
# fora do range aceitavel
type_error_regex = re.compile('(\([0-9],[0-9]\))')

while True:
    # inicializa o campo
    number_of_moves = 0
    tiles = range(9)

    # espera por uma conexão
    print('esperando uma conexão')
    # aceita a conexão do cliente
    connection, client_address = sock.accept()
    try:
        print('conexao de %s:%s\n' % client_address)

        while True:
            # recebe os dados do cliente
            data = connection.recv(255)
            # checa se foi passado alguma coisa
            if data:
                # checa se os dados passados são validos
                if error_regex.match(data):
                    # divide os dados em coluna e linha
                    col = int(data.split(',')[0][-1])
                    row = int(data.split(',')[1][0])

                    # checa se a posição escolhida já esta ocupada
                    if tiles[row * 3 + col] == PLAYER or tiles[row * 3 + col] == CPU_PLAYER:
                        # retorna o erro para o cliente
                        print('<-- movimento não é possivel')
                        connection.sendall("TYPE: ERROR///Movimento nao e possivel")
                    else:
                        # faz a movimentação do usuario
                        tiles = manual_move(tiles, col, row)
                        # copia o campo para poder retornar o campo sem o movimento do
                        # computador para o cliente
                        tiles_copy = tiles[:]
                        print(format_board(tiles))
                        print('\n<-- movimento do usuario realizado\n')

                        number_of_moves += 1

                        # checa se é fim de jogo
                        if check_end_game(tiles, number_of_moves) == "":
                            # faz a movimentação do computador
                            tiles = ai_move(tiles)
                            number_of_moves += 1

                            # checa se é fim de jogo
                            if check_end_game(tiles, number_of_moves) == "":
                                print(format_board(tiles))
                                # retorna para o cliente o campo após a jogada do usuario e o campo após a jogada do computador
                                print('\n<-- movimento do computador realizado\n')
                                connection.sendall("TYPE: GAME///" + format_board(tiles_copy) + "///" + format_board(tiles))
                            else:
                                # retorna para o cliente o campo final e a mensagem de fim de jogo
                                print('\n<-- fim de jogo')
                                connection.sendall("TYPE: ENDGAME///" + format_board(tiles) + "///" + check_end_game(tiles, number_of_moves))
                        else:
                            # retorna para o cliente o campo final e a mensagem de fim de jogo
                            print('\n<-- fim de jogo')
                            connection.sendall("TYPE: ENDGAME///" + format_board(tiles) + "///" + check_end_game(tiles, number_of_moves))
                else:
                    # retorna o erro para o cliente
                    print("erro nos dados passados")
                    if type_error_regex.match(data):
                        connection.sendall("TYPE: ERROR///Os valores passados nao estao entre 0 e 2")
                    else:
                        connection.sendall("TYPE: ERROR///Os valores passados nao estao no formato correto")
            else:
                # fecha a conexão com o cliente
                print('\n\n')
                print('fim dos dados', client_address)
                break

    finally:
        # fecha o socket caso haja algum erro
        connection.close()
