from tcp_server import TCPServer

import argparse
parser = argparse.ArgumentParser(description='NetEmu Client')
parser.add_argument('--server', '-s', dest='ip', default='127.0.0.1', help='the ip address of the NetEmu server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--loopback', '-l', dest='loopback', default=8081, type=int, help='local port to which the client uses as loopback')

def main():
    args = parser.parse_args()

    print('NetEmu Client')

    with TCPServer(8081) as loopback:
        lsock, _ = loopback.accept()

if __name__ == '__main__':
    main()