import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
print('\n\n')
sock.connect(server_address)

try:
    # Send data
    message = raw_input('Input: ')
    print('--> sending "%s"' % message)
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    print("teste")

    while amount_received < amount_expected:
        data = sock.recv(255)
        amount_received += len(data)
        print('<-- received "%s"' % data)

finally:
    print('\n\n')
    print('closing socket')
    sock.close()
