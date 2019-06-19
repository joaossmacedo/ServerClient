# -*- coding: utf-8 -*-
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('conectado a %s porta %s\n' % server_address)
sock.connect(server_address)

print ('-' * 10) + '\nINSTRUÇÕES\n' \
      'Esse é um jogo da velha\n' \
      'O movimento escolhido deve ser passado como "(c,r)"\n' \
      'onde c é a coluna e r é a linha\n' \
      'Para finalizar o jogo digitar endgame\n\n' \
      'Para mais informações: https://en.wikipedia.org/wiki/Tic-tac-toe\n' \
      + ('-' * 10) + '\n'


while True:
    try:
        # Send data
        message = raw_input('Input: ')
        if message == "endgame":
            break

        print('--> enviando "%s"' % message)
        sock.sendall(message)

        data = sock.recv(255)
        if "End Game" in data:
            print('<-- recebendo\n')
            print data.split("End Game")[0]
            print data.split("End Game")[-1]
            break
        print('<-- recebendo\n\n%s' % data)

    except Exception:
        print '\nfechando socket'
        sock.close()

print'\nfechando socket'
sock.close()

