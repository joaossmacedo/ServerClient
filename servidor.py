import socket
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
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        print('\n\n')

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(255)
            if data:
                col = int(data.split(',')[0][-1])
                row = int(data.split(',')[1][0])
                pos = row * 3 + col
                print('--> col = "%s"' % col)
                print('--> row = "%s"' % row)

                return_data = data[::-1]
                print('<-- sending data back to the client')
                connection.sendall(str(pos))
            else:
                print('\n\n')
                print('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
