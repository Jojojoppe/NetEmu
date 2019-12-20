import sys
import socket

class TCPServer():
    def __init__(self, port, maxcon=1):
        self.port = port
        self.maxcon = maxcon

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('localhost', self.port))
            self.sock.listen(self.maxcon)
        except ConnectionRefusedError:
            print("Could not connect to socket: connection refused")
            sys.exit(0)

    def stop(self):
        self.sock.close()

    def write(self, data):
        self.sock.send(data)

    def recv(self, bufsize):
        return self.sock.recv(bufsize)

    def accept(self, timeout=1.0):
        self.sock.settimeout(timeout)
        return self.sock.accept()