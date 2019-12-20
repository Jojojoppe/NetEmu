import sys
import socket
import threading
import signal

from tcp import TCPServer

import argparse
parser = argparse.ArgumentParser(description='NetEmu Server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--maxcon', '-n', dest='maxcon', default=10, type=int, help='maximum amount of connections on the NetEmu server')

# GLOBALS
running = True

class ThreadConnection(threading.Thread):
    def __init__(self, socket, address, port):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.port = port
        self.running = False

    def __del__(self):
        self.socket.close()

    def run(self):
        self.running = True
        print("Connection opened from %s"%self.address)
        pass

    def stop(self):
        self.running = False

def close_handler(signal, reserved):
    global running
    print("\rClosing server...")
    running = False

def main():
    global running
    args = parser.parse_args()

    print('NetEmu Server')

    # List of all connections (active and non-active)
    connections = []

    with TCPServer(args.port, args.maxcon) as server:
        while running:
            # Wait for connection and create listening thread
            try:
                csock, con_info = server.accept(1.0)
                cthread = ThreadConnection(csock, *con_info)
                cthread.start()
                connections.append(cthread)
            except socket.timeout:
                continue

        # Clean up all connections
        for conn in connections:
            if conn.running:
                conn.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()