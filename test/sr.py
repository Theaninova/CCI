# documentation for .service files
# '>' sends something, '<' receives something and validates it against data
# use 'binary data (0|1), reads in byte (8 bits) chunks
# refer to examples for more detailed info

import getopt
import socket
import subprocess
import sys
import binascii


# no regard for error
def main(argv):
    opts, args = getopt.getopt(argv, "f:a:p:A:P:F:", ["file=", "address=", "port=", "server_address=", "server_port="])

    input_file = ''
    address = ''
    port = 0
    s_address = ''
    s_port = 0
    program_path = ''
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            input_file = arg
        elif opt in ("-F", "--program_path"):
            program_path = arg
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-A", "server_address"):
            s_address = arg
        elif opt in ("-P", "server_port"):
            s_port = int(arg)

    f = open(input_file, "r")
    contents = f.read()

    mode = 'null'
    data = ''

    for char in contents:
        if char == '>':
            mode = 'snd'
            data = ''
        elif char == '<':
            sock = setup_rec(s_address, s_port)

            mode = 'rec'
            data = ''
        elif char == '^':
            process = subprocess.Popen([program_path])
        elif char == '%':
            if data != '':
                byte_data = bytes.fromhex(data)
                if mode == 'rec':
                    rec(sock, byte_data, process)
                elif mode == 'snd':
                    send(address, port, byte_data)
        else:
            data = data + char

    f.close()
    process.terminate()


def setup_rec(address, port):
    print(f"Creating Server at {address}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (address, port)
    sock.bind(server_address)
    sock.listen(1)

    return sock


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
        print("Closing connection")
        sock.close()


def rec(sock, data, process):
    print("Waiting for connection...")

    connection, client_address = sock.accept()
    try:
        received_data = connection.recv(1024)
        print(f"Received data from client {client_address}: {binascii.hexlify(received_data)}")
        print(f"Evaluating received data on {binascii.hexlify(data)}")

        if len(received_data) != len(data):
            print("Received data is not the same length, terminating")
            process.terminate()
            exit(-1)

        for r_byte, o_byte in zip(received_data, data):
            if r_byte != o_byte:
                print("Data is not equal, terminating")
                process.terminate()
                exit(-1)
        print("Verified data")
    finally:
        print("Closing connection")
        connection.close()

if __name__ == "__main__":
    main(sys.argv[1:])
