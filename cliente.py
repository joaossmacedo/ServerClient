# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import threading
import time
import sys

def simulate_time():
    time.sleep(0.5)
    print('.', end='')
    sys.stdout.flush()
    time.sleep(0.5)
    print('.', end='')
    sys.stdout.flush()
    time.sleep(0.5)
    print('.')
    sys.stdout.flush()
    time.sleep(0.5)

# cria o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conecta o socket a porta que esta escutando
server_address = ('localhost', 10000)
print('conectado a %s porta %s\n' % server_address)
sock.connect(server_address)

print (('-' * 10) + '\nINSTRUÇÕES\n' \
      'Esse é um jogo da velha\n' \
      'O movimento escolhido deve ser passado como "(c,r)"\n' \
      'onde c é a coluna e r é a linha\n' \
      'Para finalizar o jogo digitar endgame\n\n' \
      'Para mais informações: https://en.wikipedia.org/wiki/Tic-tac-toe\n' \
      + ('-' * 10) + '\n')


while True:
    try:
        # pede os dados para o usuario
        message = raw_input('Input: ')
        if message == "endgame":
            break

        # manda os dados pro servidor
        print('--> enviando "%s"' % message)
        sock.sendall(message)

        data = sock.recv(255)
        splitted_data = data.split('///')
        data_type = splitted_data[0]

        if data_type == "TYPE: ENDGAME":
            print('<-- recebendo\n')
            print(splitted_data[1])
            print(splitted_data[2])
            break
        elif data_type == "TYPE: ERROR":
            print('<-- recebendo\n' + splitted_data[1] + '\n')
        elif data_type == "TYPE: GAME":
            print('<-- recebendo\n\n' + splitted_data[1])
            simulate_time()
            print('')
            print(splitted_data[2])

    except Exception:
        print('\nfechando socket')
        sock.close()

print('\nfechando socket')
sock.close()

