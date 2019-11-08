# documentation for .service files
# '>' sends something, '<' receives something and validates it against data
# use 'binary data (0|1), reads in byte (8 bits) chunks
# refer to examples for more detailed info

import getopt
import socket
import sys
import binascii


# no regard for error
def main(argv):
    opts, args = getopt.getopt(argv, "f:a:p:A:P:", ["file=", "address=", "port=", "server_address=", "server_port="])

    input_file = ''
    address = ''
    port = 0
    s_address = ''
    s_port = 0
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            input_file = arg
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-A", "server_address"):
            s_address = arg
        elif opt in ("-P", "server_port"):
            s_port = arg

    f = open(input_file, "r")
    contents = f.read()

    mode = 'null'
    data = ''

    for char in contents:
        if char == '>':
            byte_data = bytes.fromhex(data)
            if mode == 'rec':
                rec(s_address, s_port, byte_data)
            elif mode == 'snd':
                send(address, port, byte_data)
            mode = 'rec'
            data = ''
        elif char == '<':
            byte_data = bytes.fromhex(data)

            send(address, port, byte_data)

            mode = 'snd'
            data = ''
        else:
            data = data + char

    f.close()


def send(address, port, data):
    print(f"Connecting to {address}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    sock.connect(server_address)

    try:
        # Send data
        print(f"Sending {binascii.hexlify(data)}")
        sock.sendall(data)
    finally:
        print(f"Closing connection")
        sock.close()


def rec(address, port, data):
    print(f"Creating Server at {address}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    sock.bind(server_address)
    sock.listen(1)

    print(f"Waiting for connection...")

    connection, client_address = sock.accept()
    try:
        received_data = connection.recv()
        print(f"Received data from client {client_address}: {binascii.hexlify(received_data)}")
        print(f"Evaluating received data on {binascii.hexlify(data)}")

        if len(received_data) != len(data):
            print(f"Received data is not the same length, terminating")
            exit(-1)

        for r_byte, o_byte in zip(received_data, data):
            if r_byte != o_byte:
                print(f"Data is not equal, terminating")
                exit(-1)
        print("Verified data")
    finally:
        print("Closing connection")
        connection.close()


if __name__ == "__main__":
    main(sys.argv[1:])
