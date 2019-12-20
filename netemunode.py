import signal
import socket
from tcp import TCPServer, TCPClient, Timeout

import argparse
parser = argparse.ArgumentParser(description='NetEmu Client')
parser.add_argument('--server', '-s', dest='ip', default='127.0.0.1', help='the ip address of the NetEmu server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--loopback', '-l', dest='loopback', default=8081, type=int, help='local port to which the client uses as loopback')
parser.add_argument('--control', '-c', dest='control', default=8082, type=int, help='local port to which the client uses as control channel')

# GLOBALS
running = True

def recv_timeout(socket, bufsize, timeout):
    socket.settimeout(timeout)
    try:
        dat = socket.recv(bufsize)
    except Timeout:
        dat = None
    return dat

def close_handler(signal, reserved):
    global running
    print("\rClosing client...")
    running = False

def main():
    global running
    args = parser.parse_args()

    print('NetEmu Client')

    # Open loopback server
    with TCPServer(args.loopback) as loopback:
        lsock, _ = loopback.accept()
    # Open control server
    with TCPServer(args.control) as control:
        csock, _ = control.accept()
    print("Applicatio layer connected")

    # Connect to server
    with TCPClient(args.ip, args.port) as server:
        pass

    while running:
        # Receive loopback data
        dat = recv_timeout(lsock, 4096, 0.1)
        # Receive control data
        dat = recv_timeout(csock, 4096, 0.1)
        # Receive data from server
        dat = recv_timeout(server.sock, 4096, 0.1)

    # Cleanup
    lsock.close()
    csock.close()
    server.stop()
    loopback.stop()
    control.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()