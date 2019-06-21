# -*- coding: utf-8 -*-
from __future__ import print_function
import socket
import time
import sys
import re


def simulate_loading():
    time.sleep(0.5)
    print('.', end = '')
    sys.stdout.flush()
    time.sleep(0.5)
    print('.', end = '')
    sys.stdout.flush()
    time.sleep(0.5)
    print('.')
    sys.stdout.flush()
    time.sleep(0.5)


# cria o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
regex = re.compile("/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g")
ip = raw_input("Digite o IP do host(deixe vazio para localhost): ")
while not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) and ip != "":
    ip = raw_input("Digite o IP do host(deixe vazio para localhost): ")

# conecta o socket a porta que esta escutando
server_address = (ip, 10000)
print('conectado a %s porta %s\n' % server_address)
sock.connect(server_address)

print(('-' * 10) + '\nINSTRUÇÕES\n' \
                   'Esse é um jogo da velha\n' \
                   'O movimento escolhido deve ser passado como "(c,r)"\n' \
                   'onde c é a coluna e r é a linha\n' \
                   'Para finalizar o jogo digitar endgame\n\n' \
                   'Para mais informações: https://en.wikipedia.org/wiki/Tic-tac-toe'
                   '\n' + ('-' * 10) + '\n')

while True:
    try:
        # pede os dados para o usuario
        message = ''
        while message == '':
            message = raw_input('Input: ')
        # fecha o socket quando o input é endgame
        if message == "endgame":
            break

        # manda os dados pro servidor
        print('--> enviando "%s"' % message)
        sock.sendall(message)

        # recebe a resposta do servidor
        data = sock.recv(255)
        # divide a resposta do servidor de acordo com os divisores definidos como ///
        splitted_data = data.split('///')
        data_type = splitted_data[0]

        # trata dos 3 tipos de retorno possivel
        if data_type == "TYPE: ENDGAME":
            print('<-- recebendo\n')
            # nesse tipo de retorno o segundo item da lista contem o campo
            print(splitted_data[1])
            # o terceiro item da lista contem o resultado
            print(splitted_data[2])
            break
        elif data_type == "TYPE: ERROR":
            # nesse tipo de retorno o segundo item da lista contem o erro
            print('<-- recebendo\n' + splitted_data[1] + '\n')
        elif data_type == "TYPE: GAME":
            # nesse tipo de retorno o segundo item da lista contem o campo somente com a
            # jogada do usuario
            print('<-- recebendo\n\n' + splitted_data[1])
            # simula um loading(...)
            simulate_loading()
            print('')
            # o terceiro item da lista contem o campo após a jogada do usuario e do computador
            print(splitted_data[2])

    except Exception:
        print('\nfechando socket')
        sock.close()

print('\nfechando socket')
sock.close()
