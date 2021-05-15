# This is a multithreaded server that can handle multiple clients at once.
# It handles queries from clients to find matches in wordlist.antioxidant
# It returns matches to client
#
# Usage:
#   python3 echo_server.py <server_host> <server_port>
#
# I modified echo-server-better.py which was given in class to create this program
# author: Jake McGinn
# class: CSE  3300, section 001, Spring 2021
# Source: COMP 332, Fall 2018, Wesleyan University
# Source: https://www.w3schools.com/python/python_regex.asp to learn about regex in python

import socket
import sys
import threading
import re

class EchoServer():
    # passed in wordlist here to avoid global variables and to only
    # have to read wordlist once.
    def __init__(self, server_host, server_port, wordlist):

        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.wordlist = wordlist
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        # handle any errors
        except OSError as e:
            print ('Unable to open socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for client(s) connection
        # while loop placed here so multiple clients can connect
        while True:
            try:
                # Client has connected
                [client_conn, client_addr] = server_sock.accept()
                print ('Client has connected with address: ', client_addr)

                # Create thread to serve client
                # passing in wordlist so every thread has access to it
                # This is more effcient than reading from the file every time
                thread = threading.Thread(
                        target = self.serve_content,
                        args = (client_conn, client_addr, self.wordlist))
                thread.daemon = True
                thread.start()
            # handle errors just in case
            except Exception as e:
                print ('Problem connecting / creating thread: ', e)
                if server_sock:
                    server_sock.close()
                sys.exit(1)

    def serve_content(self, client_conn, client_addr, wordlist):
        while True:
            try:
                # Receive data from client
                bin_data = client_conn.recv(1024)
                a = bin_data.decode('utf-8')
                # Make sure characters are a-z, (, ), or '
                # done for security / good practice
                whitelist = "qwertyuiopasdfghjklzxcvbnm.-()?'"
                if any(c not in whitelist for c in a):
                    print("Input character not found in whitelist. Quitting...")
                    server_sock.close()
                    sys.exit(1)
                if a == "quit":
                    print ('Disconnecting client with address', client_addr)
                    client_conn.close()
                    break
                # check for ? in client query
                if '?' in a:
                    # replace all '?' characters with '.' for regex paramater
                    q = a.replace('?', '.')
                    # words is a list of all matching words
                    words = []
                    # loop through wordlist created in main and passed to here
                    # this could be more efficent but it works instantly on my
                    # computer so I didn't see a point in further optimization
                    i = 0;
                    for word in wordlist:
                        # check for match using regex
                        x = re.fullmatch(q, word)
                        # x is empty if there is no match
                        if x:
                            # add match to words array
                            words.insert(i, x.group())
                            i = i + 1
                    # If there are matches then return a string of the array
                    # of matches
                    if i > 0:
                        client_conn.sendall(str(words).encode('utf-8'))
                    else:
                        client_conn.sendall("not found".encode('utf-8'))
                # Commented code below allows queries of wordlist without a ?
                # I commented it out because the instructions say it's not required.
                #elif a in wordlist:
                #    client_conn.sendall(bin_data)
                else:
                    client_conn.sendall("Must use ? in query".encode('utf-8'))
                # Print data from client
                print ('Server received', bin_data, 'from', client_addr)
            # handle more errors
            except Exception as e:
                print ('Problem with client input: ', e)
                client_conn.close()
                sys.exit(1)

def main():
    # Echo server socket parameters
    server_host = 'localhost'
    server_port = 50006

    # Parse command line parameters if any
    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # read wordlist into array without \n characters
    wfile = open("wordlist.txt", "r")
    wordlist = wfile.read().splitlines()
    wfile.close()

    # Create EchoServer object
    server = EchoServer(server_host, server_port, wordlist)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down")
    except Exception:
        print("Other exception")
