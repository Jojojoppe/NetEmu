import sys
import socket

Timeout = socket.timeout

class TCPServer():
    def __init__(self, port, maxcon=1, flags=0):
        self.port = port
        self.maxcon = maxcon
        self.flags = flags

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
        except:
            print("Could not connect to socket")
            sys.exit(0)

    def stop(self):
        self.sock.close()

    def send(self, data):
        self.sock.send(data)

    def recv(self, bufsize):
        return self.sock.recv(bufsize)

    def recv_timeout(self, bufsize, timeout):
        self.sock.settimeout(timeout)
        try:
            dat = self.sock.recv(bufsize)
        except Timeout:
            dat = None
        return dat

    def accept(self, timeout=None):
        if timeout!=None:
            self.sock.settimeout(timeout)
        return self.sock.accept()

class TCPClient():
    def __init__(self, address, port, flags=0):
        self.address = address
        self.port = port
        self.flags = flags

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.address, self.port))
        except:
            print("Could not connect to socket")
            sys.exit(0)

    def stop(self):
        self.sock.close()

    def send(self, data):
        self.sock.send(data)

    def recv(self, bufsize):
        return self.sock.recv(bufsize)

    def recv_timeout(self, bufsize, timeout):
        self.sock.settimeout(timeout)
        try:
            dat = self.sock.recv(bufsize)
        except Timeout:
            dat = None
        return dat

