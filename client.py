# Client connects to server, submits query from user input.
# Prints matches to query returned by server
#
# Usage:
#   python3 echo_client.py <server_host> <server_port>
#
# I modified echo-client-better.py which was given in class to create this program
# author: Jake McGinn
# class: CSE  3300, section 001, Spring 2021
# Source: COMP 332, Fall 2018, Wesleyan University

import socket
import sys

class EchoClient():

    def __init__(self, server_host, server_port):
        self.start(server_host, server_port)

    def start(self, server_host, server_port):

        # Try to connect to echo server using TCP
        try:
            server_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((server_host, server_port))
        # print error if it cant connect
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Now client is connected
        # This while loop repeats until user types quit or server is closed
        # This allows user to input queries and recieve answers multiple times
        while True:
            try:
                print("Enter query or type quit to terminate")
                # a is stdin from user
                a = input()
                # quit if blank space
                if len(a) == 0:
                    q = "quit".encode('utf-8')
                    server_sock.sendall(q)
                    server_sock.close()
                    sys.exit(1)
                # Make sure characters in a are a-z, (, ), or '
                # This is for security / good practice.
                # any characters not in whitelist disconnects the client
                whitelist = "qwertyuiopasdfghjklzxcvbnm()-.?'"
                if any(c not in whitelist for c in a):
                    print("Input character not found in whitelist. Quitting...")
                    q = "quit".encode('utf-8')
                    server_sock.sendall(q)
                    server_sock.close()
                    sys.exit(1)
                # messages need to be encoded before they are sent
                bin_msg = a.encode('utf-8')
                # query is encoded and sent to server here
                server_sock.sendall(bin_msg)
                # close server socket after sending quit msg if client wants to quit
                if a == "quit":
                    server_sock.close()
                    sys.exit(1)
                # Get response data from server and print it
                bin_resp = server_sock.recv(1024)
                str_resp = bin_resp.decode('utf-8')
                print ('Client received', str_resp)
            # catch and handle any exceptions
            except Exception as e:
                print ('Something went wrong: ', e)
                if server_sock:
                    server_sock.close()
                sys.exit(1)


def main():

    # Echo server socket parameters
    server_host = 'localhost'
    server_port = 50006

    # Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create EchoClient object
    client = EchoClient(server_host, server_port)

if __name__ == '__main__':
    main()
