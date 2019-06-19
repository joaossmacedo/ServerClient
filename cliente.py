import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
print('\n\n')
sock.connect(server_address)
while True:
    try:
        # Send data
        message = raw_input('Input: ')
        if message == "endgame":
            break

        print('--> sending "%s"' % message)
        sock.sendall(message)

        data = sock.recv(255)
        if "End Game" in data:
            break
        print('<-- received\n\n%s' % data)

    except Exception:
        print('\n\n')
        print('closing socket')
        sock.close()

print('\n\n')
print('closing socket')
sock.close()

